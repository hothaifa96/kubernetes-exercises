const express = require('express');

const app = express();
const PORT = process.env.PORT || 80;
const API_BASE = process.env.API_BASE || '/api';
const APP_TITLE = process.env.APP_TITLE || 'Kubernetes Class App';

app.get('/', (req, res) => {
  res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${APP_TITLE}</title>
  <style>
    body { font-family: sans-serif; margin: 2rem; background: #f8f9fa; }
    h1 { color: #333; }
    input, button { padding: 0.5rem; font-size: 1rem; }
    ul { list-style: none; padding: 0; }
    li { padding: 0.5rem; background: #fff; margin: 0.25rem 0; border-radius: 4px; }
    .status { padding: 1rem; background: #e9ecef; border-radius: 4px; margin: 1rem 0; }
  </style>
</head>
<body>
  <h1>${APP_TITLE}</h1>
  <p>API base: <strong id="apiBase"></strong></p>
  <div class="status" id="health">Loading health...</div>
  <div>
    <input id="text" type="text" placeholder="New todo item">
    <button id="add">Add</button>
    <button id="visit">Count visit</button>
  </div>
  <ul id="list"></ul>
  <p>Visits: <span id="visits">0</span></p>

  <script>
    const API = '${API_BASE}';
    document.getElementById('apiBase').textContent = API;

    async function loadHealth() {
      try {
        const r = await fetch(API + '/health');
        const data = await r.json();
        document.getElementById('health').textContent = JSON.stringify(data, null, 2);
      } catch (e) {
        document.getElementById('health').textContent = 'Health check failed: ' + e;
      }
    }

    async function loadItems() {
      try {
        const r = await fetch(API + '/items');
        const items = await r.json();
        const list = document.getElementById('list');
        list.innerHTML = items.map(i => \`<li>\${i.text} (done: \${i.done})</li>\`).join('');
      } catch (e) {
        console.error('Items load failed:', e);
      }
    }

    document.getElementById('add').onclick = async () => {
      const text = document.getElementById('text').value;
      if (!text) return;
      await fetch(API + '/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, done: false })
      });
      document.getElementById('text').value = '';
      await loadItems();
      await loadHealth();
    };

    document.getElementById('visit').onclick = async () => {
      const r = await fetch(API + '/visits');
      const data = await r.json();
      document.getElementById('visits').textContent = data.visits;
    };

    loadHealth();
    loadItems();
  </script>
</body>
</html>
`);
});

app.listen(PORT, () => console.log(`Frontend listening on port ${PORT}`));
