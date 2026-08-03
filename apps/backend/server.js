const express = require('express');
const mongoose = require('mongoose');
const redis = require('redis');
const fs = require('fs');
const path = require('path');

const app = express();

const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/todo';
const REDIS_HOST = process.env.REDIS_HOST || 'redis';
const REDIS_PORT = parseInt(process.env.REDIS_PORT || '6379', 10);
const FILE_STORE = process.env.FILE_STORE_PATH || '/shared/data';

app.use(express.json());

if (!fs.existsSync(FILE_STORE)) {
  fs.mkdirSync(FILE_STORE, { recursive: true });
}

const itemSchema = new mongoose.Schema({
  text: String,
  done: { type: Boolean, default: false },
  createdAt: { type: Date, default: Date.now }
});
const Item = mongoose.model('Item', itemSchema);

const redisClient = redis.createClient({
  socket: { host: REDIS_HOST, port: REDIS_PORT }
});
redisClient.on('error', err => console.error('Redis error:', err));
redisClient.connect().catch(() => {});

app.get('/api/health', async (req, res) => {
  const mongoOk = mongoose.connection.readyState === 1;
  const redisOk = redisClient.isReady;
  res.json({
    status: mongoOk && redisOk ? 'ok' : 'degraded',
    mongo: mongoOk,
    redis: redisOk
  });
});

app.get('/api/items', async (req, res) => {
  const items = await Item.find().sort({ createdAt: -1 });
  res.json(items);
});

app.post('/api/items', async (req, res) => {
  const item = await Item.create({
    text: req.body.text,
    done: !!req.body.done
  });
  if (redisClient.isReady) {
    await redisClient.incr('item_count');
  }
  res.json(item);
});

app.get('/api/visits', async (req, res) => {
  let count = 0;
  if (redisClient.isReady) {
    count = await redisClient.incr('visits');
  }
  res.json({ visits: Number(count) });
});

app.post('/api/files/:name', (req, res) => {
  const filePath = path.join(FILE_STORE, req.params.name);
  fs.writeFileSync(filePath, req.body.content || '');
  res.json({ saved: req.params.name });
});

app.get('/api/files/:name', (req, res) => {
  const filePath = path.join(FILE_STORE, req.params.name);
  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: 'not found' });
  }
  res.send(fs.readFileSync(filePath, 'utf8'));
});

async function start() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log('Connected to MongoDB');
  } catch (e) {
    console.error('MongoDB connection failed:', e.message);
  }
  app.listen(PORT, () => console.log(`Backend listening on port ${PORT}`));
}
start();
