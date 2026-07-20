# Backend API

A tiny in-memory REST API that stores "tasks" and moves them through a
pipeline. It is the **central service** — the frontend, worker, and job all
talk to it.

## What it does

- Holds a list of tasks in memory.
- Lets the **Job** create tasks (`status = pending`).
- Lets the **Worker** mark tasks as `done`.
- Lets the **Frontend** read tasks and aggregate stats.

## Configuration (environment variables)

These are read from the environment so you can supply them from a **ConfigMap**.

| Variable        | Default               | Purpose                                        |
|-----------------|-----------------------|------------------------------------------------|
| `APP_TITLE`     | `DevOps Task Pipeline`| Display name returned by the API.              |
| `PROCESS_LABEL` | `processed`           | Tag the worker attaches when finishing a task. |
| `PORT`          | `8080`                | Port the API listens on.                       |

## API

| Method | Path                     | Used by  | Description                        |
|--------|--------------------------|----------|------------------------------------|
| GET    | `/health`                | probes   | Health check.                      |
| GET    | `/tasks`                 | frontend | List tasks. `?status=pending\|done`|
| POST   | `/tasks`                 | job      | Create a task `{"title": "..."}`.  |
| POST   | `/tasks/{id}/process`    | worker   | Mark task done `{"worker": "..."}`.|
| GET    | `/stats`                 | frontend | Totals: total / pending / done.    |

## Run locally

```bash
pip install -r requirements.txt
python app.py
# in another terminal:
curl localhost:8080/health
curl -X POST localhost:8080/tasks -H 'Content-Type: application/json' -d '{"title":"hello"}'
curl localhost:8080/tasks
```

## Your Kubernetes tasks

- Build and push a container image for this app.
- Write a **Deployment** for it.
- Expose it **inside the cluster** with a `ClusterIP` **Service** named `backend`
  on port `8080` (the other components will reach it at `http://backend:8080`).
- Feed `APP_TITLE` and `PROCESS_LABEL` from a **ConfigMap**.
- Add `livenessProbe` / `readinessProbe` pointing at `/health`.
