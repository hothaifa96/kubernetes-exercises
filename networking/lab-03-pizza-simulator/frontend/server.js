const express = require("express");
const axios = require("axios");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:5000";

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

async function proxyGet(backendPath, res) {
  try {
    const response = await axios.get(`${BACKEND_URL}${backendPath}`, { timeout: 6000 });
    res.json(response.data);
  } catch (err) {
    const status = err.response ? err.response.status : 503;
    res.status(status).json({
      error: "Backend unreachable",
      backend_url: BACKEND_URL,
      details: err.message,
    });
  }
}

async function proxyPost(backendPath, body, res) {
  try {
    const response = await axios.post(`${BACKEND_URL}${backendPath}`, body, { timeout: 6000 });
    res.json(response.data);
  } catch (err) {
    const status = err.response ? err.response.status : 503;
    const data = err.response ? err.response.data : { error: "Backend unreachable", details: err.message };
    res.status(status).json(data);
  }
}

app.get("/api/info",   (req, res) => proxyGet("/api/info", res));
app.get("/api/pizzas", (req, res) => proxyGet("/api/pizzas", res));
app.get("/api/orders", (req, res) => proxyGet("/api/orders", res));
app.post("/api/order", (req, res) => proxyPost("/api/order", req.body, res));

app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
  console.log(`Pizza Frontend listening on port ${PORT}`);
  console.log(`Proxying API calls to backend: ${BACKEND_URL}`);
});
