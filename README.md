# Kubernetes Class Exercise

A complete minikube exercise that walks through 7 milestones:

1. Frontend and backend containerization.
2. Deploying frontend and backend in Kubernetes (plus MongoDB).
3. ClusterIP Services for all workloads.
4. Ingress to route traffic.
5. Shared storage for the backend and backups.
6. Redis connectivity using a DaemonSet.
7. A hard instructor challenge.

## What is included

- `apps/backend/` - Node/Express API that talks to MongoDB and Redis.
- `apps/frontend/` - Node/Express simple HTML UI.
- `k8s/` - Kubernetes manifests, numbered by milestone.

## Required environment variables

### Backend (`k8s/09-backend-deployment.yaml`)

| Variable       | Source in this repo                          | Purpose                         |
|----------------|----------------------------------------------|---------------------------------|
| `PORT`         | `3000` literal                               | HTTP listen port                |
| `MONGO_URI`    | `app-secrets` Secret                         | Full MongoDB connection string  |
| `REDIS_HOST`   | `app-config` ConfigMap                       | Redis service name              |
| `REDIS_PORT`   | `app-config` ConfigMap                       | Redis service port              |
| `FILE_STORE_PATH` | `"/shared/data"` literal                  | Shared PVC mount path           |

### Frontend (`k8s/11-frontend-deployment.yaml`)

| Variable       | Source in this repo                          | Purpose                         |
|----------------|----------------------------------------------|---------------------------------|
| `PORT`         | `80` literal                                 | HTTP listen port                |
| `API_BASE`     | `app-config` ConfigMap                       | Base path for API calls         |
| `APP_TITLE`    | `app-config` ConfigMap                       | Page title                      |

### MongoDB (`k8s/07-mongo-deployment.yaml`)

| Variable                      | Source in this repo     | Purpose                         |
|-------------------------------|-------------------------|---------------------------------|
| `MONGO_INITDB_ROOT_USERNAME`  | `app-secrets` Secret    | Root user                       |
| `MONGO_INITDB_ROOT_PASSWORD`  | `app-secrets` Secret    | Root password                   |
| `MONGO_INITDB_DATABASE`       | `app-config` ConfigMap  | Database created at startup     |

The MongoDB URI is already encoded in `k8s/02-secrets.yaml`:

```
mongodb://root:password123@mongo:27017/todo?authSource=admin
```

Change the password in `02-secrets.yaml` before using this for anything other than a lab.

## Deploy to minikube

1. Start minikube with the ingress addon:

```bash
minikube start --driver=
minikube addons enable ingress
```

2. Use minikube's Docker so images are available inside the cluster:

```bash
eval $(minikube docker-env) if you are running on docker driver
```

3. Build the images:

4. write k8s manifests

5. Wait for pods to be ready

6. Map the ingress host. On Linux:

```bash
minikube ip
# Add to /etc/hosts: <minikube-ip> class.local
```

On macOS/Windows with the Docker driver, run `minikube tunnel` in another terminal and then add `127.0.0.1 class.local` to `/etc/hosts`.

7. Open `http://class.local` in a browser.

## Milestones summary

1. **Two deployments** - `backend` and `frontend`. MongoDB is needed, so it is deployed in `07-mongo-deployment.yaml`.
2. **ClusterIP Services** - `10-backend-service.yaml`, `12-frontend-service.yaml`, `08-mongo-service.yaml`, and `15-redis-service.yaml`.
3. **Ingress** - `13-ingress.yaml` routes `/api` to the backend and everything else to the frontend on `class.local`.
4. **Shared storage** - `04-shared-pvc.yaml` is mounted by the backend. `05-mongo-pvc.yaml` is used by MongoDB. `06-backup-pvc.yaml` stores backups.
5. **Backup Job and CronJob** - `16-job-backup.yaml` runs a one-time copy of the shared volume into a date-named directory on the backup PVC. `17-cronjob-backup.yaml` runs the same logic daily at 02:00.
6. **Redis as a DaemonSet** - `14-redis-daemonset.yaml` runs a Redis pod on every node. `15-redis-service.yaml` exposes it to the backend.
7. **Hard exercise** - See `extra-challenge.md`.

## Useful commands

```bash
# View all pods in the namespace
kubectl get pods -n class-exercise

# Check backend health
kubectl port-forward svc/backend 3000:3000 -n class-exercise
curl http://localhost:3000/api/health

# Trigger a one-off backup manually
kubectl create -f k8s/16-job-backup.yaml

# Watch CronJob schedule
kubectl get cronjobs -n class-exercise
```

## Cleanup

```bash
kubectl delete -f k8s/
minikube delete
```
