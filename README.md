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
- `k8s/` - **You create this.** Write the manifests yourself, numbered by milestone (see below).

## Required environment variables

### Backend (`09-backend-deployment.yaml`)

| Variable          | Should come from         | Purpose                        |
| ----------------- | ------------------------ | ------------------------------ |
| `PORT`            | literal `3000`           | HTTP listen port               |
| `MONGO_URI`       | `app-secrets` Secret     | Full MongoDB connection string |
| `REDIS_HOST`      | `app-config` ConfigMap   | Redis service name             |
| `REDIS_PORT`      | `app-config` ConfigMap   | Redis service port             |
| `FILE_STORE_PATH` | literal `"/shared/data"` | Shared PVC mount path          |

### Frontend (`11-frontend-deployment.yaml`)

| Variable    | Should come from       | Purpose                 |
| ----------- | ---------------------- | ----------------------- |
| `PORT`      | literal `80`           | HTTP listen port        |
| `API_BASE`  | `app-config` ConfigMap | Base path for API calls |
| `APP_TITLE` | `app-config` ConfigMap | Page title              |

### MongoDB (`07-mongo-deployment.yaml`)

| Variable                     | Should come from       | Purpose                     |
| ---------------------------- | ---------------------- | --------------------------- |
| `MONGO_INITDB_ROOT_USERNAME` | `app-secrets` Secret   | Root user                   |
| `MONGO_INITDB_ROOT_PASSWORD` | `app-secrets` Secret   | Root password               |
| `MONGO_INITDB_DATABASE`      | `app-config` ConfigMap | Database created at startup |

Encode the MongoDB URI yourself in `02-secrets.yaml`, e.g.:

```
mongodb://root:password123@mongo:27017/todo?authSource=admin
```

Pick your own root password, base64-encode it, and use that in the Secret.

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

3. Build the images.

4. Write and apply the k8s manifests (see **Manifests you need to create** below).

5. Wait for pods to be ready.

6. Map the ingress host. On Linux:

```bash
minikube ip
# Add to /etc/hosts: <minikube-ip> class.local
```

On macOS/Windows with the Docker driver, run `minikube tunnel` in another terminal and then add `127.0.0.1 class.local` to `/etc/hosts`.

7. Open `http://class.local` in a browser.

## Manifests you need to create

Create a `k8s/` folder and write the following manifests yourself, in this order (the numbering matches the milestones):

1. **`01-namespace.yaml`** - a `Namespace` called `class-exercise`. Put every other resource in it.
2. **`02-secrets.yaml`** - a `Secret` holding the Mongo root username/password and the full `MONGO_URI`.
3. **`03-configmap.yaml`** - a `ConfigMap` holding `REDIS_HOST`, `REDIS_PORT`, `API_BASE`, `APP_TITLE`, and `MONGO_INITDB_DATABASE`.
4. **`04-shared-pvc.yaml`** - a `PersistentVolumeClaim` mounted by the backend for file storage.
5. **`05-mongo-pvc.yaml`** - a `PersistentVolumeClaim` for MongoDB's data directory.
6. **`06-backup-pvc.yaml`** - a `PersistentVolumeClaim` where backups are written.
7. **`07-mongo-deployment.yaml`** - a `Deployment` running MongoDB, using the Secret/ConfigMap values and mounting `05-mongo-pvc.yaml`.
8. **`08-mongo-service.yaml`** - a `ClusterIP` Service named `mongo` exposing port `27017`.
9. **`09-backend-deployment.yaml`** - a `Deployment` running the backend image, wired to the env vars above and mounting the shared PVC.
10. **`10-backend-service.yaml`** - a `ClusterIP` Service named `backend` exposing port `3000`.
11. **`11-frontend-deployment.yaml`** - a `Deployment` running the frontend image, wired to the env vars above.
12. **`12-frontend-service.yaml`** - a `ClusterIP` Service named `frontend` exposing port `80`.
13. **`13-ingress.yaml`** - an `Ingress` on host `class.local` routing `/api` to `backend` and `/` to `frontend`.
14. **`14-redis-daemonset.yaml`** - a `DaemonSet` running Redis on every node.
15. **`15-redis-service.yaml`** - a `ClusterIP` Service named `redis` exposing port `6379`.
16. **`16-job-backup.yaml`** - a `Job` that copies the shared PVC into a date-named directory on the backup PVC.
17. **`17-cronjob-backup.yaml`** - a `CronJob` that runs the same backup logic daily at 02:00.
18. **Milestone 7 - hard exercise** - see `extra-challenge.md` and add whatever extra manifests your chosen challenges require (e.g. `StatefulSet`, `NetworkPolicy`, `HorizontalPodAutoscaler`, TLS `Secret`).

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
