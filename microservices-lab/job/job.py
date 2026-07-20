"""
Job (seeder) for the DevOps microservices lab.

A one-off task: it creates SEED_COUNT tasks in the backend and then exits
with code 0. This is the classic use case for a Kubernetes Job — run once,
complete, done. If it cannot reach the backend it exits non-zero so the Job
is marked failed and can be retried.

The backend location comes from the BACKEND_URL environment variable
(supply it via a ConfigMap).
"""
import os
import sys

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080").rstrip("/")
SEED_COUNT = int(os.getenv("SEED_COUNT", "5"))


def main():
    print(f"[job] seeding {SEED_COUNT} tasks into {BACKEND_URL}", flush=True)
    created = 0
    for i in range(1, SEED_COUNT + 1):
        try:
            resp = requests.post(
                f"{BACKEND_URL}/tasks",
                json={"title": f"Task #{i} from seeder"},
                timeout=5,
            )
            resp.raise_for_status()
            created += 1
            print(f"[job] created: {resp.json()['title']}", flush=True)
        except requests.RequestException as exc:
            print(f"[job] failed to reach backend: {exc}", file=sys.stderr, flush=True)
            sys.exit(1)

    print(f"[job] done, created {created} tasks", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
