# Lab 05 — Microservices Architecture with ConfigMaps and Secrets

## Objective

Deploy a three-tier microservices application to Minikube consisting of:

- **Frontend** — Node.js/Express server (`npm start`), port **3000**
- **Auth Service** — Python/Flask, port **5001**
- **Data Service** — Python/Flask, port **5002**

The frontend communicates with both microservices. All microservice configuration (except passwords) must be injected via ConfigMaps. All passwords and secret keys must be injected via Secrets.

This lab is intentionally challenging. You must figure out how to:

- Wire three services together using Kubernetes DNS
- Inject configuration from ConfigMaps
- Inject secrets from Secrets
- Expose the application externally via NodePort
- Handle service discovery across namespaces if you choose to use them

---

## Repository Structure

```
lab-05-microservices/
├── README.md              ← this file
├── frontend/
│   ├── server.js          ← Express proxy server
│   ├── public/
│   │   └── index.html     ← Single-page dashboard
│   ├── package.json
│   └── Dockerfile
├── auth-service/
│   ├── app.py             ← Flask auth microservice
│   ├── requirements.txt
│   └── Dockerfile
└── data-service/
    ├── app.py             ← Flask data microservice
    ├── requirements.txt
    └── Dockerfile
```

---

## Ports

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | Node.js/Express web server |
| Auth Service | 5001 | Flask authentication API |
| Data Service | 5002 | Flask data management API |

---

## Environment Variables

### Frontend

| Variable | Description | Source |
|----------|-------------|--------|
| `PORT` | Port the Express server listens on | ConfigMap |
| `AUTH_SERVICE_URL` | Full URL of the auth service (e.g., `http://auth-service:5001`) | ConfigMap |
| `DATA_SERVICE_URL` | Full URL of the data service (e.g., `http://data-service:5002`) | ConfigMap |
| `FRONTEND_USER` | Username for the frontend (displayed in UI) | ConfigMap |
| `FRONTEND_PASSWORD` | Password for the frontend (displayed in UI for verification) | Secret |

### Auth Service

| Variable | Description | Source |
|----------|-------------|--------|
| `AUTH_SECRET_KEY` | Secret key for token signing (must match data service) | Secret |
| `AUTH_USER` | Username for authentication | ConfigMap |
| `AUTH_PASSWORD` | Password for authentication | Secret |
| `TOKEN_EXPIRY_HOURS` | Token validity period in hours | ConfigMap |

### Data Service

| Variable | Description | Source |
|----------|-------------|--------|
| `AUTH_SECRET_KEY` | Secret key for token validation (must match auth service) | Secret |

---

## Secrets — Values to Use

Create a Secret with the following keys and values:

| Key | Value |
|-----|-------|
| `frontend-password` | `LabPass2025!` |
| `auth-password` | `AuthSecret2025!` |
| `auth-secret-key` | `MicroservicesLabSecretKey2025` |

> **Hint:** The same `auth-secret-key` value must be used by both the auth service and the data service for token validation to work.

---

## ConfigMap — Values to Use

Create a ConfigMap with the following keys and values:

| Key | Value |
|-----|-------|
| `frontend-port` | `3000` |
| `auth-service-url` | `http://auth-service:5001` |
| `data-service-url` | `http://data-service:5002` |
| `frontend-user` | `labadmin` |
| `auth-user` | `admin` |
| `token-expiry-hours` | `24` |

---

## What You Need to Build

### Step 1 — Build and Push Docker Images

Build all three images locally, tag them, and push them to a registry your Minikube cluster can pull from.

```
docker build -t <your-registry>/microservices-frontend:v1 ./frontend
docker build -t <your-registry>/microservices-auth:v1    ./auth-service
docker build -t <your-registry>/microservices-data:v1    ./data-service

docker push <your-registry>/microservices-frontend:v1
docker push <your-registry>/microservices-auth:v1
docker push <your-registry>/microservices-data:v1
```

> **Hint:** If you're using Minikube with Docker daemon, you can use `minikube image load` instead of pushing to a registry.

### Step 2 — Create ConfigMap and Secret

Create the ConfigMap and Secret with the exact keys and values specified above.

> **Hint:** You can create them from literals using `kubectl create configmap` and `kubectl create secret generic`, or from YAML files. The choice is yours.

### Step 3 — Write Kubernetes Manifests

You must create manifests for the following resources. All resources must be in a single namespace (create one first, e.g., `microservices`).

---

#### 3a. Auth Service

- **Deployment** — 2 replicas of your auth service image
- Inject environment variables from the ConfigMap and Secret
- **Service (ClusterIP)** — expose port 5001
  - Name: `auth-service` (this becomes the DNS hostname)

> **Hint:** The service name must match the hostname used in the ConfigMap's `auth-service-url`.

---

#### 3b. Data Service

- **Deployment** — 2 replicas of your data service image
- Inject the `AUTH_SECRET_KEY` from the Secret
- **Service (ClusterIP)** — expose port 5002
  - Name: `data-service` (this becomes the DNS hostname)

> **Hint:** The service name must match the hostname used in the ConfigMap's `data-service-url`.

---

#### 3c. Frontend

- **Deployment** — 1 replica of your frontend image
- Inject all environment variables from the ConfigMap and Secret
- **Service (NodePort)** — expose port 3000
  - Choose a NodePort in the range 30000-32767

> **Hint:** The frontend uses the service URLs from the ConfigMap to reach the microservices. If the services are in the same namespace, short DNS names work. If in different namespaces, use `<service-name>.<namespace>.svc.cluster.local`.

---

## Verification Steps

1. Apply all manifests in order: ConfigMap → Secret → Auth Service → Data Service → Frontend
2. Verify all pods are running:
   ```
   kubectl get pods -n microservices
   ```
3. Verify all services are created:
   ```
   kubectl get svc -n microservices
   ```
4. Get the NodePort assigned to the frontend:
   ```
   kubectl get svc frontend -n microservices
   ```
5. Open the application in your browser:
   ```
   http://<minikube-ip>:<nodeport>
   ```
   To get minikube IP: `minikube ip`
6. Check the status panel at the top — both services should show "Online"
7. Log in using the credentials:
   - Username: `admin` (from ConfigMap)
   - Password: `AuthSecret2025!` (from Secret)
8. After logging in, you should see the data items and be able to add/delete them

---

## Success Criteria

| Check | Expected |
|-------|----------|
| All pods running | ✓ 3 deployments, all pods in `Running` state |
| ConfigMap injected | ✓ Environment variables from ConfigMap are set |
| Secret injected | ✓ Passwords and secret keys from Secret are set |
| Services discoverable | ✓ Frontend can reach both microservices via DNS |
| Auth service works | ✓ Can log in with credentials from ConfigMap/Secret |
| Data service works | ✓ Can view, add, and delete items after login |
| External access | ✓ Application accessible via NodePort from browser |

---

## Bonus Challenges

1. **Namespace Isolation**: Deploy the microservices in one namespace and the frontend in another. Update the ConfigMap to use fully qualified DNS names (`<service-name>.<namespace>.svc.cluster.local`).
2. **Health Probes**: Add readiness and liveness probes to all three services.
3. **Resource Limits**: Set resource requests and limits on all deployments.
4. **Horizontal Pod Autoscaling**: Configure HPA for the auth and data services based on CPU usage.
5. **Ingress**: Replace the NodePort with an Ingress resource using the NGINX Ingress Controller.

---

## Concepts to Understand After This Lab

- How microservices communicate via Kubernetes DNS
- The difference between ConfigMaps and Secrets, and when to use each
- How to inject ConfigMap/Secret values as environment variables
- How service discovery works within and across namespaces
- The role of NodePort in exposing services externally
- Why secrets should never be committed to source control
- How to verify that secrets are correctly injected without exposing them in logs
- The trade-offs between using short DNS names vs fully qualified domain names
- How to debug service-to-service communication issues
