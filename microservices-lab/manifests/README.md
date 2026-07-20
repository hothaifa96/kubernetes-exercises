# Manifests — YOUR WORK GOES HERE

This folder is **intentionally almost empty**. Writing the Kubernetes manifests
is the exercise. You will create every YAML file yourself.

## What you must create

Create one file per resource (or group them, your choice):

| # | File (suggested)      | Kind        | Notes                                                             |
|---|-----------------------|-------------|-------------------------------------------------------------------|
| 1 | `configmap.yaml`      | ConfigMap   | Holds shared config: `BACKEND_URL`, `APP_TITLE`, `PROCESS_LABEL`, `SEED_COUNT`. |
| 2 | `backend.yaml`        | Deployment + Service (ClusterIP) | Service **must** be named `backend`, port `8080`. Add probes on `/health`. |
| 3 | `frontend.yaml`       | Deployment + Service (**NodePort**) | Reads `BACKEND_URL` from the ConfigMap. Exposed to your browser. |
| 4 | `worker.yaml`         | Deployment  | Long-running. Try `replicas: 2`. Reads `BACKEND_URL`.             |
| 5 | `job.yaml`            | Job         | One-off seeder. `restartPolicy: OnFailure`. Reads `BACKEND_URL` + `SEED_COUNT`. |

A starter skeleton with `TODO`s is provided in **`TODO.yaml`** — open it and
fill in every `TODO`.

## Required environment wiring

Every app reads its config from environment variables. You must supply them
from the **ConfigMap** (do not hard-code values inside the Deployments).

The single most important value is **`BACKEND_URL`**. Inside the cluster the
backend is reachable at its Service DNS name:

```
BACKEND_URL = http://backend:8080
```

The frontend, worker, and job all depend on this.

## Suggested order of operations

```bash
# 1. Config first, everything else depends on it
kubectl apply -f configmap.yaml

# 2. Backend + its ClusterIP service
kubectl apply -f backend.yaml
kubectl rollout status deploy/backend

# 3. Frontend (NodePort) and worker
kubectl apply -f frontend.yaml
kubectl apply -f worker.yaml

# 4. Seed data with the Job (backend must be up first)
kubectl apply -f job.yaml
kubectl get jobs
```

## How to verify it works

- `kubectl get pods` — backend, frontend, worker are `Running`; job is `Completed`.
- `kubectl get svc` — note the frontend NodePort (e.g. `3XXXX`).
- Open `http://<node-ip>:<nodePort>` (minikube: `minikube service frontend --url`).
- Watch the dashboard: pending tasks should flip to **done** as the worker runs.
- `kubectl logs deploy/worker` — see it processing tasks.
- `kubectl logs job/<job-name>` — see the seeder output.

## Acceptance checklist

- [ ] ConfigMap holds all shared config; no values hard-coded in Deployments.
- [ ] `backend` Service is `ClusterIP` on port `8080`.
- [ ] `frontend` Service is `NodePort` and reachable from your browser.
- [ ] Frontend reads `BACKEND_URL` from the ConfigMap.
- [ ] Worker is a Deployment and marks tasks `done`.
- [ ] Job runs once, reaches `Completed`, and seeded tasks appear in the UI.
