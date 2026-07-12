const express = require("express");
const axios = require("axios");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || "http://localhost:5001";
const DATA_SERVICE_URL = process.env.DATA_SERVICE_URL || "http://localhost:5002";
const FRONTEND_USER = process.env.FRONTEND_USER || "admin";
const FRONTEND_PASSWORD = process.env.FRONTEND_PASSWORD || "secret";

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

async function proxyGet(serviceUrl, path, res) {
  try {
    const response = await axios.get(`${serviceUrl}${path}`, { timeout: 6000 });
    res.json(response.data);
  } catch (err) {
    const status = err.response ? err.response.status : 503;
    res.status(status).json({
      error: "Service unreachable",
      service: serviceUrl,
      details: err.message,
    });
  }
}

async function proxyPost(serviceUrl, path, body, res) {
  try {
    const response = await axios.post(`${serviceUrl}${path}`, body, { timeout: 6000 });
    res.json(response.data);
  } catch (err) {
    const status = err.response ? err.response.status : 503;
    const data = err.response ? err.response.data : { error: "Service unreachable", details: err.message };
    res.status(status).json(data);
  }
}

app.get("/api/auth/health", (req, res) => proxyGet(AUTH_SERVICE_URL, "/health", res));
app.post("/api/auth/login", (req, res) => proxyPost(AUTH_SERVICE_URL, "/login", req.body, res));
app.post("/api/auth/validate", (req, res) => proxyPost(AUTH_SERVICE_URL, "/validate", req.body, res));

app.get("/api/data/health", (req, res) => proxyGet(DATA_SERVICE_URL, "/health", res));
app.get("/api/data/items", (req, res) => proxyGet(DATA_SERVICE_URL, "/items", res));
app.post("/api/data/items", (req, res) => proxyPost(DATA_SERVICE_URL, "/items", req.body, res));
app.delete("/api/data/items/:id", (req, res) => {
  proxyGet(DATA_SERVICE_URL, `/items/${req.params.id}`, res);
});

app.get("/api/config", (req, res) => {
  res.json({
    auth_service: AUTH_SERVICE_URL,
    data_service: DATA_SERVICE_URL,
    frontend_user: FRONTEND_USER,
  });
});

app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
  console.log(`Microservices Frontend listening on port ${PORT}`);
  console.log(`Auth Service: ${AUTH_SERVICE_URL}`);
  console.log(`Data Service: ${DATA_SERVICE_URL}`);
  console.log(`Frontend User: ${FRONTEND_USER}`);
});
