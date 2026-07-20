"""
Frontend web app for the DevOps microservices lab.

It renders a small dashboard by calling the backend API.
The backend location is NOT hard-coded: it comes from the BACKEND_URL
environment variable, which you will provide via a ConfigMap.

  BACKEND_URL example (inside the cluster):  http://backend:8080
  BACKEND_URL example (local docker):        http://localhost:8080
"""
import os

import requests
from flask import Flask, render_template_string

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration (inject via ConfigMap)
# ---------------------------------------------------------------------------
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080").rstrip("/")
APP_TITLE = os.getenv("APP_TITLE", "DevOps Task Pipeline")
PORT = int(os.getenv("PORT", "8081"))

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="refresh" content="5" />
  <title>{{ title }}</title>
  <style>
    body { font-family: system-ui, sans-serif; background:#0f172a; color:#e2e8f0;
           margin:0; padding:40px; }
    .wrap { max-width:820px; margin:0 auto; }
    h1 { margin:0 0 4px; }
    .muted { color:#94a3b8; margin-bottom:24px; }
    .cards { display:flex; gap:16px; margin-bottom:28px; }
    .card { flex:1; background:#1e293b; border-radius:12px; padding:20px; text-align:center; }
    .card b { display:block; font-size:2.2em; }
    table { width:100%; border-collapse:collapse; background:#1e293b; border-radius:12px; overflow:hidden; }
    th, td { padding:12px 16px; text-align:left; border-bottom:1px solid #334155; }
    .pending { color:#fbbf24; }
    .done { color:#34d399; }
    .err { background:#7f1d1d; padding:16px; border-radius:12px; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>{{ title }}</h1>
    <p class="muted">Backend: {{ backend }} &middot; auto-refresh every 5s</p>

    {% if error %}
      <div class="err">Could not reach backend at <code>{{ backend }}</code>: {{ error }}</div>
    {% else %}
      <div class="cards">
        <div class="card"><b>{{ stats.total }}</b>Total</div>
        <div class="card"><b class="pending">{{ stats.pending }}</b>Pending</div>
        <div class="card"><b class="done">{{ stats.done }}</b>Done</div>
      </div>
      <table>
        <tr><th>#</th><th>Title</th><th>Status</th><th>Processed by</th></tr>
        {% for t in tasks %}
        <tr>
          <td>{{ t.id }}</td>
          <td>{{ t.title }}</td>
          <td class="{{ t.status }}">{{ t.status }}</td>
          <td>{{ t.processed_by or "-" }}</td>
        </tr>
        {% endfor %}
      </table>
    {% endif %}
  </div>
</body>
</html>
"""


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/")
def index():
    try:
        stats = requests.get(f"{BACKEND_URL}/stats", timeout=3).json()
        tasks = requests.get(f"{BACKEND_URL}/tasks", timeout=3).json()
        return render_template_string(
            PAGE, title=APP_TITLE, backend=BACKEND_URL,
            stats=stats, tasks=tasks, error=None,
        )
    except requests.RequestException as exc:
        return render_template_string(
            PAGE, title=APP_TITLE, backend=BACKEND_URL,
            stats=None, tasks=[], error=str(exc),
        )


if __name__ == "__main__":
    print(f"[frontend] talking to backend at {BACKEND_URL}, listening on :{PORT}")
    app.run(host="0.0.0.0", port=PORT)
