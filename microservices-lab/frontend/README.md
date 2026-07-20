# Frontend

A small web dashboard that shows the tasks and live stats from the backend.
The page auto-refreshes every 5 seconds so you can watch the worker chew
through the queue.

## Key idea: the backend URL is configurable

The frontend does **not** know where the backend is. It reads the
`BACKEND_URL` environment variable. This is the main thing you will wire up
with a **ConfigMap** in Kubernetes.

- Inside the cluster: `BACKEND_URL = http://backend:8080`
- Local docker/host:  `BACKEND_URL = http://localhost:8080`

## Configuration (environment variables)

| Variable      | Default                 | Purpose                              |
|---------------|-------------------------|--------------------------------------|
| `BACKEND_URL` | `http://localhost:8080` | Where to reach the backend API.      |
| `APP_TITLE`   | `DevOps Task Pipeline`  | Page heading.                        |
| `PORT`        | `8081`                  | Port the web server listens on.      |

## Run locally

```bash
pip install -r requirements.txt
# point it at a running backend:
export BACKEND_URL=http://localhost:8080
python app.py
# open http://localhost:8081
```

## Your Kubernetes tasks

- Build and push a container image for this app.
- Write a **Deployment** for it.
- Expose it to the **outside world** with a **NodePort** Service.
- Inject `BACKEND_URL` from the shared **ConfigMap** (value: `http://backend:8080`).
- Confirm you can open the NodePort in your browser and see the tasks.
