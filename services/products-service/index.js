'use strict';

const http = require('http');
const os   = require('os');

const SERVICE_NAME = process.env.SERVICE_NAME || 'products-service';
const PORT         = parseInt(process.env.PORT || '3003', 10);
const POD_IP       = process.env.POD_IP || getLocalIP();

function getLocalIP() {
  const nets = os.networkInterfaces();
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === 'IPv4' && !net.internal) {
        return net.address;
      }
    }
  }
  return '127.0.0.1';
}

const SAMPLE_PRODUCTS = [
  { id: 'prod-001', name: 'Kubernetes in Action',  price: 49.99, stock: 12 },
  { id: 'prod-002', name: 'Docker Deep Dive',       price: 39.99, stock: 8  },
  { id: 'prod-003', name: 'Cloud Native Patterns',  price: 44.99, stock: 20 },
];

function send(res, status, body, type) {
  const raw = typeof body === 'string' ? body : JSON.stringify(body, null, 2);
  res.writeHead(status, {
    'Content-Type':   type || 'application/json',
    'Content-Length': Buffer.byteLength(raw),
  });
  res.end(raw);
}

const server = http.createServer((req, res) => {
  console.log(`[${SERVICE_NAME}] ${req.method} ${req.url}`);

  if (req.url === '/ready' && req.method === 'GET') {
    send(res, 200, {
      service:  SERVICE_NAME,
      hostname: os.hostname(),
      ip:       POD_IP,
      status:   'ready',
    });

  } else if (req.url === '/api/products' && req.method === 'GET') {
    send(res, 200, { service: SERVICE_NAME, products: SAMPLE_PRODUCTS });

  } else if (req.url === '/' && req.method === 'GET') {
    send(res, 200, `Hello from ${SERVICE_NAME}!\n`, 'text/plain');

  } else {
    send(res, 404, { error: 'Not found' });
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`[${SERVICE_NAME}] Listening on 0.0.0.0:${PORT}`);
});
