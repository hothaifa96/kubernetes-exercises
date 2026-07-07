# Lab 03 — Three-Tier App: Pizza Order Simulator

## Objective

Deploy a full three-tier web application inside Kubernetes and wire all three tiers together using Kubernetes Services, environment variables, and ConfigMaps.

The app is a **Pizza Order Simulator**:

- **Frontend** — Node.js / Express server (`npm start`), port **3000**  
  Shows the pizza menu, a customer order form, and a live cluster status panel.  
  The status panel displays:
  - The **backend pod name** that served the last request
  - The **backend pod IP**
  - Whether the **database is connected or not**

- **Backend** — Python / Flask API server, port **5000**  
  Handles the menu and order logic.  
  Reads its own pod identity from environment variables you must inject via the Kubernetes **Downward API**.

- **Database** — MongoDB, port **27017**  
  Stores all placed orders.

---

## Repository Structure

```
lab-03-pizza-simulator/
├── README.md              ← this file
├── frontend/
│   ├── server.js          ← Express server + API proxy
│   ├── public/
│   │   └── index.html     ← Single-page UI
│   ├── package.json
│   └── Dockerfile
└── backend/
    ├── app.py             ← Flask REST API
    ├── requirements.txt
    └── Dockerfile
```

---

## Environment Variables

### Frontend

| Variable | Description | Example |
|----------|-------------|---------|
| `BACKEND_URL` | Full URL of the backend service | `http://pizza-backend:5000` |
| `PORT` | Port the Express server listens on | `3000` |

### Backend

| Variable | Description | Example |
|----------|-------------|---------|
| `POD_NAME` | Name of the running pod — **must come from the Downward API** | `pizza-backend-abc-xyz` |
| `POD_IP` | IP of the running pod — **must come from the Downward API** | `10.244.1.7` |
| `MONGO_URI` | MongoDB connection string | `mongodb://pizza-db:27017` |
| `DB_NAME` | Database name inside MongoDB | `pizzadb` |

> **POD_NAME and POD_IP must be populated using Kubernetes Downward API field references** (`fieldRef`), not hardcoded values. If they are hardcoded every backend pod will report the same identity, and you will not be able to observe how traffic is distributed when you scale up.

---

## What You Need to Build

This lab provides **all source code and Dockerfiles**. You must build and push the images, then write and apply all Kubernetes manifests from scratch.

### Step 1 — Build and push Docker images

Build both images locally, tag them, and push them to a container registry your cluster can pull from (Docker Hub, GitHub Container Registry, or a local registry).

```
docker build -t <your-registry>/pizza-frontend:v1 ./frontend
docker build -t <your-registry>/pizza-backend:v1  ./backend

docker push <your-registry>/pizza-frontend:v1
docker push <your-registry>/pizza-backend:v1
```

### Step 2 — Create a dedicated Namespace

All resources for this lab must live in a single namespace.  
Create it first. Name it something meaningful — for example `pizza`.

### Step 3 — Write the Kubernetes Manifests

You must create manifests for the following resources. All resources must be in the namespace you created.

---

#### 3a. MongoDB

- **Deployment** — 1 replica of the official `mongo` image (any recent tag).
- **Service (ClusterIP)** — expose port `27017`. This service name becomes the hostname in the backend's `MONGO_URI`.

No persistent volume is required for this lab, but you should understand why data is lost when the pod restarts.

---

#### 3b. Backend (Flask)

- **Deployment** — 2 replicas of your backend image.
- Set the following environment variables in the pod spec:
  - `POD_NAME` — use a `fieldRef` to inject `metadata.name`
  - `POD_IP`   — use a `fieldRef` to inject `status.podIP`
  - `MONGO_URI` — point to the MongoDB service you created
  - `DB_NAME`   — choose a database name
- **Service (ClusterIP)** — expose port `5000`. This service name becomes the value of `BACKEND_URL` in the frontend.

---

#### 3c. Frontend (Node.js)

- **Deployment** — 1 replica of your frontend image.
- Set the `BACKEND_URL` environment variable to the URL of the backend ClusterIP service.
- **Service (NodePort)** — expose port `3000` via a NodePort so you can open the UI from your browser.

---

#### 3d. Optional — ConfigMap

- Instead of hardcoding values like `MONGO_URI` and `BACKEND_URL` directly in each Deployment, extract them into a ConfigMap and reference the ConfigMap keys using `envFrom` or `valueFrom.configMapKeyRef`.
- This simulates how real teams manage environment-specific configuration without changing the image.

---

## Testing Your Deployment

1. Get the NodePort assigned to the frontend service.
2. Open `http://<node-ip>:<node-port>` in your browser.
3. You should see the Pizza Order Simulator UI.
4. Check the **Cluster Status** panel at the top:
   - **Backend Pod Name** — should show a real pod name like `pizza-backend-6d4f9-xrz2p`
   - **Backend Pod IP**   — should show a real pod IP like `10.244.1.7`
   - **Database**         — should show **Connected** if MongoDB is running and reachable
5. Select a pizza, enter your name, and place an order.
6. The order should appear in the **Recent Orders** table below the form, with the pod name and IP that handled it.

---

## Scale Experiment

Once everything is working:

1. Scale the backend Deployment to **5 replicas**.
2. Place several orders in quick succession.
3. Observe the **"Served by Pod"** column in the orders table.

**Question:** Do you see different pod names and IPs appearing? Why or why not?  
**Question:** What is distributing traffic across the backend pods?

---

## Success Criteria

| Check | Expected |
|-------|----------|
| Frontend loads in browser | ✓ Pizza menu appears |
| Status panel shows pod name | ✓ Real pod name, not `unknown-pod` |
| Status panel shows pod IP | ✓ A `10.x.x.x` cluster IP, not `unknown-ip` |
| Database status is green | ✓ `Connected` |
| Order persists after page refresh | ✓ Order appears in Recent Orders table |

---
