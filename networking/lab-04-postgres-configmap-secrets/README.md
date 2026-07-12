# Lab 04 — PostgreSQL with ConfigMap, Secrets, and Resource Limits

## Objective

Deploy a PostgreSQL database inside Kubernetes using a ConfigMap for configuration, a Secret for credentials, and enforce resource limits on the pod. Expose the database via a Service and make it accessible from outside the cluster using NodePort.

This lab focuses on:

- Using **ConfigMaps** to inject configuration without changing the image
- Using **Secrets** to securely store sensitive data (passwords)
- Setting **resource requests and limits** to control pod resource usage
- Exposing internal services via **NodePort** for external access

---

## Provided Information

### Image

Use the official PostgreSQL image: `postgres:16-alpine`

### Ports

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 5432 | Default PostgreSQL port |

### Required Environment Variables

| Variable | Description | Source |
|----------|-------------|--------|
| `POSTGRES_DB` | Name of the database to create | ConfigMap |
| `POSTGRES_USER` | Username for the database | Secret |
| `POSTGRES_PASSWORD` | Password for the user | Secret |
| `PGDATA` | Location of the database files | ConfigMap (optional, but recommended for persistence) |

### Resource Requirements

Set the following resource constraints on the PostgreSQL pod:

| Resource | Request | Limit |
|----------|---------|-------|
| CPU | 250m | 500m |
| Memory | 256Mi | 512Mi |

> **Hint:** PostgreSQL is memory-intensive. If you set the memory limit too low, the OOMKiller may terminate the pod. The values above are minimal for a lab environment.

### Service Requirements

- Create a **ClusterIP** service for internal cluster access
- Create a **NodePort** service for external access (or use a single service with type NodePort)
- Target port: 5432
- Choose a NodePort in the range 30000-32767

---

## What You Need to Build

### 1. ConfigMap

Create a ConfigMap that contains:

- `POSTGRES_DB`: Set this to `labdb`
- `PGDATA`: Set this to `/var/lib/postgresql/data/pgdata`

> **Hint:** The ConfigMap should be referenced in the deployment using `valueFrom.configMapKeyRef` or `envFrom`.

### 2. Secret

Create a Secret that contains:

- `POSTGRES_USER`: Set this to `labuser`
- `POSTGRES_PASSWORD`: Set this to `SecurePass123!`

> **Hint:** Secrets can be created from literals, files, or string data. For this lab, create it from literal values using `kubectl create secret generic`.

### 3. Deployment

Create a Deployment for PostgreSQL with:

- 1 replica
- The `postgres:16-alpine` image
- Environment variables injected from the ConfigMap and Secret
- Resource requests and limits as specified above
- A label selector that matches your service

> **Hint:** When injecting from ConfigMap/Secret, you can use `envFrom` to inject all keys, or `valueFrom` for specific keys. For passwords, always use `valueFrom.secretKeyRef` to avoid exposing the secret in the deployment spec.

### 4. Services

Create two services:

- **ClusterIP Service**: For internal access within the cluster
  - Name: `postgres-internal`
  - Port: 5432
  - TargetPort: 5432

- **NodePort Service**: For external access from your machine
  - Name: `postgres-external`
  - Port: 5432
  - TargetPort: 5432
  - NodePort: Choose a port in 30000-32767

> **Hint:** You can also create a single service with type `NodePort` that serves both purposes. The decision is yours.

---

## Verification Steps

1. Apply all manifests in order: ConfigMap → Secret → Deployment → Services
2. Verify the pod is running and not in a CrashLoopBackOff state:
   ```
   kubectl get pods
   kubectl describe pod <postgres-pod-name>
   ```
3. Check the pod's resource usage:
   ```
   kubectl top pod <postgres-pod-name>
   ```
4. Verify the services are created:
   ```
   kubectl get svc
   ```
5. Test internal connectivity by creating a temporary pod and connecting to the ClusterIP service:
   ```
   kubectl run pg-client --image=postgres:16-alpine --rm -it --restart=Never -- psql -h postgres-internal -U labuser -d labdb
   ```
   When prompted, enter the password: `SecurePass123!`
6. Test external connectivity using the NodePort:
   ```
   psql -h <minikube-ip> -p <nodeport> -U labuser -d labdb
   ```
   To get minikube IP: `minikube ip`

---

## Success Criteria

| Check | Expected |
|-------|----------|
| Pod is running | ✓ Pod status is `Running` |
| Resource limits applied | ✓ Pod has CPU/memory requests and limits |
| ConfigMap injected | ✓ `POSTGRES_DB` and `PGDATA` are set correctly |
| Secret injected | ✓ `POSTGRES_USER` and `POSTGRES_PASSWORD` are set correctly |
| ClusterIP service works | ✓ Can connect from another pod in the cluster |
| NodePort service works | ✓ Can connect from your host machine |
| Database is accessible | ✓ Can run SQL commands in psql |

---

## Bonus Challenges

1. **Persistent Volume**: Add a PersistentVolumeClaim and mount it to `/var/lib/postgresql/data` to persist data across pod restarts.
2. **Init Container**: Use an init container to wait for the database to be ready before the main container starts.
3. **Readiness Probe**: Add a readiness probe that runs `pg_isready` to ensure the pod is only marked ready when PostgreSQL can accept connections.
4. **Liveness Probe**: Add a liveness probe that checks if the database process is running.
5. **Multiple Databases**: Extend the ConfigMap to create multiple databases and users on startup using a custom init script.

---

## Concepts to Understand After This Lab

- The difference between ConfigMaps and Secrets, and when to use each
- How to inject ConfigMap/Secret values as environment variables
- Why resource requests and limits are important for cluster stability
- The difference between ClusterIP and NodePort service types
- How Kubernetes handles external access via NodePort
- The trade-offs between ephemeral storage (default) and persistent volumes
- How to verify that secrets are not exposed in pod specs or logs
