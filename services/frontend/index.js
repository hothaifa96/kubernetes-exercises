"use strict";

const http = require("http");
const os = require("os");

const SERVICE_NAME = "frontend";
const PORT = parseInt(process.env.PORT || "3000", 10);
const POD_IP = process.env.POD_IP || getLocalIP();

const BACKENDS = {
  "auth-service": process.env.AUTH_URL || "http://localhost:3001",
  "order-service": process.env.ORDERS_URL || "http://localhost:3002",
  "products-service": process.env.PRODUCTS_URL || "http://localhost:3003",
};

function getLocalIP() {
  const nets = os.networkInterfaces();
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === "IPv4" && !net.internal) {
        return net.address;
      }
    }
  }
  return "127.0.0.1";
}

function fetchReady(name, baseUrl) {
  return new Promise((resolve) => {
    const url = new URL("/ready", baseUrl);
    const mod = url.protocol === "https:" ? require("https") : http;
    const req = mod.get(url.toString(), { timeout: 3000 }, (res) => {
      let data = "";
      res.on("data", (chunk) => {
        data += chunk;
      });
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve({ service: name, status: "parse-error" });
        }
      });
    });
    req.on("error", (err) =>
      resolve({
        service: name,
        status: "unreachable",
        error: err.message,
        url: baseUrl,
      }),
    );
    req.on("timeout", () => {
      req.destroy();
      resolve({ service: name, status: "timeout", url: baseUrl });
    });
  });
}

function send(res, status, body, type) {
  const raw = typeof body === "string" ? body : JSON.stringify(body, null, 2);
  res.writeHead(status, {
    "Content-Type": type || "application/json",
    "Content-Length": Buffer.byteLength(raw),
  });
  res.end(raw);
}

function buildHTML(backendResults) {
  const rows = Object.entries(backendResults)
    .map(([name, data]) => {
      const ok = data.status === "ready";
      const color = ok ? "#16a34a" : "#dc2626";
      const badge = ok ? "✔ ready" : `✘ ${data.status}`;
      return `
      <tr>
        <td><strong>${name}</strong></td>
        <td style="color:${color}">${badge}</td>
        <td><code>${data.hostname || "—"}</code></td>
        <td><code>${data.ip || data.error || "—"}</code></td>
      </tr>`;
    })
    .join("");

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>K8s Microservices Dashboard</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Segoe UI',system-ui,sans-serif;background:#f1f5f9;color:#1e293b;min-height:100vh}
    header{background:#1e40af;color:#fff;padding:20px 32px}
    header h1{font-size:1.4rem;font-weight:700}
    header p{font-size:.85rem;opacity:.8;margin-top:4px}
    main{max-width:860px;margin:32px auto;padding:0 16px}
    .card{background:#fff;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.1);padding:24px;margin-bottom:20px}
    .card h2{font-size:1rem;font-weight:600;margin-bottom:16px;color:#475569}
    .self{display:flex;gap:24px;flex-wrap:wrap}
    .kv{flex:1;min-width:160px}
    .kv label{font-size:.75rem;color:#64748b;display:block;margin-bottom:2px}
    .kv span{font-family:monospace;font-size:.9rem;font-weight:600}
    table{width:100%;border-collapse:collapse}
    th,td{text-align:left;padding:10px 12px;border-bottom:1px solid #e2e8f0;font-size:.875rem}
    th{color:#64748b;font-weight:600;font-size:.75rem;text-transform:uppercase}
    code{background:#f1f5f9;padding:2px 6px;border-radius:4px;font-size:.8rem}
    a{color:#2563eb;text-decoration:none}a:hover{text-decoration:underline}
    .refresh{font-size:.8rem;color:#64748b;margin-top:8px}
  </style>
</head>
<body>
<header>
  <h1>Kubernetes Microservices Dashboard</h1>
  <p>Frontend aggregator — polling all backends</p>
</header>
<main>
  <div class="card">
    <h2>This Pod (frontend)</h2>
    <div class="self">
      <div class="kv"><label>Hostname</label><span>${os.hostname()}</span></div>
      <div class="kv"><label>IP</label><span>${POD_IP}</span></div>
      <div class="kv"><label>Status</label><span style="color:#16a34a">✔ ready</span></div>
    </div>
  </div>
  <div class="card">
    <h2>Backend Services</h2>
    <table>
      <thead><tr><th>Service</th><th>Status</th><th>Hostname</th><th>IP / Error</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
    <p class="refresh">Hit <a href="/ready">/ready</a> for raw JSON · refresh page to re-poll backends</p>
  </div>
</main>
</body></html>`;
}

const server = http.createServer(async (req, res) => {
  console.log(`[${SERVICE_NAME}] ${req.method} ${req.url}`);

  if (req.url === "/ready" && req.method === "GET") {
    const backendResults = {};
    await Promise.all(
      Object.entries(BACKENDS).map(async ([name, url]) => {
        backendResults[name] = await fetchReady(name, url);
      }),
    );
    send(res, 200, {
      frontend: {
        service: SERVICE_NAME,
        hostname: os.hostname(),
        ip: POD_IP,
        status: "ready",
      },
      ...backendResults,
    });
  } else if (req.url === "/" && req.method === "GET") {
    const backendResults = {};
    await Promise.all(
      Object.entries(BACKENDS).map(async ([name, url]) => {
        backendResults[name] = await fetchReady(name, url);
      }),
    );
    send(res, 200, buildHTML(backendResults), "text/html");
  } else {
    send(res, 404, { error: "Not found" });
  }
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`[${SERVICE_NAME}] Listening on 0.0.0.0:${PORT}`);
});
