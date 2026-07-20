"""
Backend API for the DevOps microservices lab.

A tiny in-memory "task pipeline" service:
  - The Job seeds tasks (status = "pending").
  - The Worker fetches pending tasks and marks them "done".
  - The Frontend reads tasks and stats to display them.

Configuration is read from environment variables so it can be supplied
by a Kubernetes ConfigMap. Nothing is hard-coded.
"""
import os
import threading
from datetime import datetime, timezone

from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration (inject these via a ConfigMap in Kubernetes)
# ---------------------------------------------------------------------------
APP_TITLE = os.getenv("APP_TITLE", "DevOps Task Pipeline")
PROCESS_LABEL = os.getenv("PROCESS_LABEL", "processed")  # tag added by the worker
PORT = int(os.getenv("PORT", "8080"))

# ---------------------------------------------------------------------------
# In-memory store (fine for a lab; a real service would use a database)
# ---------------------------------------------------------------------------
_lock = threading.Lock()
_tasks = {}          # id -> task dict
_next_id = 1


def _now():
    return datetime.now(timezone.utc).isoformat()


@app.route("/health")
def health():
    """Liveness/readiness probe target."""
    return jsonify({"status": "ok", "app": APP_TITLE})


@app.route("/tasks", methods=["GET"])
def list_tasks():
    """List tasks, optionally filtered by ?status=pending|done."""
    status = request.args.get("status")
    with _lock:
        tasks = list(_tasks.values())
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a task. Body: {"title": "..."}. Used by the Job."""
    global _next_id
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    with _lock:
        task = {
            "id": _next_id,
            "title": title,
            "status": "pending",
            "processed_by": None,
            "created_at": _now(),
            "updated_at": _now(),
        }
        _tasks[_next_id] = task
        _next_id += 1
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>/process", methods=["POST"])
def process_task(task_id):
    """Mark a task as done. Body: {"worker": "worker-name"}. Used by the Worker."""
    data = request.get_json(silent=True) or {}
    worker = data.get("worker", "unknown-worker")
    with _lock:
        task = _tasks.get(task_id)
        if not task:
            return jsonify({"error": "not found"}), 404
        task["status"] = "done"
        task["processed_by"] = f"{worker} ({PROCESS_LABEL})"
        task["updated_at"] = _now()
    return jsonify(task)


@app.route("/stats")
def stats():
    """Aggregate counts, handy for the frontend dashboard."""
    with _lock:
        tasks = list(_tasks.values())
    pending = sum(1 for t in tasks if t["status"] == "pending")
    done = sum(1 for t in tasks if t["status"] == "done")
    return jsonify({
        "app": APP_TITLE,
        "total": len(tasks),
        "pending": pending,
        "done": done,
    })


if __name__ == "__main__":
    print(f"[backend] '{APP_TITLE}' listening on :{PORT}")
    app.run(host="0.0.0.0", port=PORT)
