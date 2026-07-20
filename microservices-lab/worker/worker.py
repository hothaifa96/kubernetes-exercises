"""
Worker for the DevOps microservices lab.

A long-running process (deploy as a Deployment). In a loop it:
  1. Asks the backend for pending tasks.
  2. "Processes" each one (here: a short sleep) and marks it done.

The backend location comes from the BACKEND_URL environment variable
(supply it via a ConfigMap). This process never exits on its own,
which is exactly why it belongs in a Deployment rather than a Job.
"""
import os
import time

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080").rstrip("/")
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "3"))       # seconds between polls
WORKER_NAME = os.getenv("WORKER_NAME", os.getenv("HOSTNAME", "worker-1"))


def fetch_pending():
    resp = requests.get(f"{BACKEND_URL}/tasks", params={"status": "pending"}, timeout=5)
    resp.raise_for_status()
    return resp.json()


def process(task):
    # Simulate real work.
    time.sleep(0.5)
    resp = requests.post(
        f"{BACKEND_URL}/tasks/{task['id']}/process",
        json={"worker": WORKER_NAME},
        timeout=5,
    )
    resp.raise_for_status()
    print(f"[{WORKER_NAME}] processed task #{task['id']}: {task['title']}", flush=True)


def main():
    print(f"[{WORKER_NAME}] starting, backend={BACKEND_URL}, interval={POLL_INTERVAL}s", flush=True)
    while True:
        try:
            pending = fetch_pending()
            if not pending:
                print(f"[{WORKER_NAME}] no pending tasks, waiting...", flush=True)
            for task in pending:
                process(task)
        except requests.RequestException as exc:
            print(f"[{WORKER_NAME}] backend error: {exc}", flush=True)
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
