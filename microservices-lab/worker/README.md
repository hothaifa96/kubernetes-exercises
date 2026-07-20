# Worker

A **long-running** background process. It loops forever:

1. Ask the backend for `pending` tasks.
2. "Process" each one (a short sleep) and mark it `done`.
3. Sleep, then repeat.

Because it never finishes on its own, it belongs in a **Deployment**
(not a Job). Scale it up and watch multiple workers share the load.

## Configuration (environment variables)

| Variable        | Default                    | Purpose                                   |
|-----------------|----------------------------|-------------------------------------------|
| `BACKEND_URL`   | `http://localhost:8080`    | Where to reach the backend API.           |
| `POLL_INTERVAL` | `3`                        | Seconds to wait between polls.            |
| `WORKER_NAME`   | `$HOSTNAME` or `worker-1`  | Label recorded on each processed task.    |

> Tip: leaving `WORKER_NAME` unset lets it default to the pod hostname, so
> each replica identifies itself automatically.

## Run locally

```bash
pip install -r requirements.txt
export BACKEND_URL=http://localhost:8080
python worker.py
```

## Your Kubernetes tasks

- Build and push a container image for this app.
- Write a **Deployment** (try `replicas: 2` to see load sharing).
- Inject `BACKEND_URL` from the shared **ConfigMap**.
- No Service is needed — the worker only makes outbound calls.
