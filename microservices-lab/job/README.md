# Job (seeder)

A **one-off** task that creates a batch of tasks in the backend and then
exits. This is the textbook use case for a Kubernetes **Job**: run once,
complete, done.

- On success it exits with code `0` (Job shows `Completed`).
- If it cannot reach the backend it exits `1` (Job shows `Failed` and can retry).

## Configuration (environment variables)

| Variable      | Default                 | Purpose                          |
|---------------|-------------------------|----------------------------------|
| `BACKEND_URL` | `http://localhost:8080` | Where to reach the backend API.  |
| `SEED_COUNT`  | `5`                     | How many tasks to create.        |

## Run locally

```bash
pip install -r requirements.txt
export BACKEND_URL=http://localhost:8080
export SEED_COUNT=8
python job.py
```

## Your Kubernetes tasks

- Build and push a container image for this app.
- Write a **Job** manifest (`restartPolicy: Never` or `OnFailure`).
- Inject `BACKEND_URL` and `SEED_COUNT` from the shared **ConfigMap**.
- Run it **after** the backend is healthy, then check `kubectl get jobs`.
