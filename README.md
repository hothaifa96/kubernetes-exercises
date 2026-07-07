# Kubernetes Networking Labs

A progressive series of hands-on labs covering every layer of Kubernetes networking —
from two containers sharing a localhost to a full microservices architecture with sidecars,
ConfigMaps, Secrets, and DNS-based service discovery.

---

## Lab Overview

| Lab   | File                                        | Concept                                                                       |
| ----- | ------------------------------------------- | ----------------------------------------------------------------------------- |
| **1** | `networking/01-container-to-container.yaml` | Containers in the same Pod share one network namespace → talk via `localhost` |
| **2** | `networking/02-pod-to-pod.yaml`             | Pods get unique cluster IPs → direct pod-to-pod (and why it's fragile)        |
| **3** | `networking/03-clusterip.yaml`              | ClusterIP Service → stable VIP, load-balances across replicas                 |
| **4** | `networking/04-nodeport.yaml`               | NodePort Service → expose a Deployment to external traffic                    |
| **5** | `networking/05-dns-discovery.yaml`          | CoreDNS → call services by short name and FQDN                                |
| **6** | `networking/06-microservices/`              | 4 microservices + sidecar loggers + frontend with ConfigMap & Secret          |

---

## Prerequisites

- A running Kubernetes cluster (minikube, kind, k3d, or cloud)
- `kubectl` configured

---

## Lab 1 — Container-to-Container (Same Pod)

```bash
kubectl apply -f networking/01-container-to-container.yaml

# Watch the client call the server via localhost
kubectl logs -f multi-container-pod -c client

# Prove both containers share the same IP
kubectl exec multi-container-pod -c server -- hostname -i
kubectl exec multi-container-pod -c client -- hostname -i

kubectl delete -f networking/01-container-to-container.yaml
```

**Key concept:** All containers in a Pod share one network namespace.
The `client` container calls `http://localhost:80` — the `server` container answers.

---

## Lab 2 — Pod-to-Pod (No Service)

```bash
kubectl apply -f networking/02-pod-to-pod.yaml

# Step 1: get pod-a's IP
kubectl get pod pod-a -o wide

# Step 2: exec into pod-b and call pod-a by IP
kubectl exec -it pod-b -- sh
# inside: curl http://<POD_A_IP>:80

# Step 3: delete and re-create pod-a, watch the IP change
kubectl delete pod pod-a
kubectl apply -f networking/02-pod-to-pod.yaml
kubectl get pod pod-a -o wide   # ← new IP!

kubectl delete -f networking/02-pod-to-pod.yaml
```

**Key concept:** Pod IPs are ephemeral. Direct IP communication breaks on restarts → use Services.

---

## Lab 3 — ClusterIP Service

```bash
kubectl apply -f networking/03-clusterip.yaml

# Watch load-balanced requests in real time
kubectl logs -f curl-client

# Inspect the stable VIP
kubectl get svc backend-clusterip
kubectl get endpoints backend-clusterip

# Scale and watch new endpoints appear
kubectl scale deployment backend --replicas=5
kubectl get endpoints backend-clusterip

kubectl delete -f networking/03-clusterip.yaml
```

**Key concept:** ClusterIP assigns a VIP that never changes and routes to healthy Pods.

---

## Lab 4 — NodePort Service

```bash
kubectl apply -f networking/04-nodeport.yaml

kubectl get svc backend-nodeport   # PORT(S): 80:30080/TCP

# minikube
curl $(minikube service backend-nodeport --url)

# kubeadm / cloud
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[0].address}')
curl http://${NODE_IP}:30080

kubectl delete -f networking/04-nodeport.yaml
```

**Key concept:** NodePort opens a static port on every node for external access.

---

## Lab 5 — DNS Service Discovery

```bash
kubectl apply -f networking/05-dns-discovery.yaml

# All four forms resolve to the same ClusterIP:
kubectl exec -it dns-client -- sh

# Inside the pod:
nslookup echo-server
nslookup echo-server.default
nslookup echo-server.default.svc.cluster.local
wget -qO- http://echo-server
wget -qO- http://echo-server.default.svc.cluster.local

# See the search domains that make short names work:
cat /etc/resolv.conf

kubectl delete -f networking/05-dns-discovery.yaml
```

**Key concept:** CoreDNS gives every Service a DNS record.
`<service>.<namespace>.svc.cluster.local` is the fully-qualified domain name (FQDN).

---

## Lab 6 — Microservices Architecture

### Architecture

```
External ──► NodePort :30090
                 │
         frontend-svc (NodePort)
                 │
     ┌───────────▼────────────────────────────────┐
     │        frontend Deployment (2 replicas)      │
     │  ConfigMap: APP_ENV, backend URLs            │
     │  Secret:    API_KEY, JWT_SECRET              │
     │  DownwardAPI: POD_IP                         │
     └────────────────────────────────────────────┘
          │            │             │           │
          ▼            ▼             ▼           ▼
     order-service  orders-service  products  notifications
         (1 Pod)      (1 Pod)      (1 Pod)    (1 Pod)
            │              │            │           │
       ┌────┴────┐    ┌────┴────┐  ┌───┴───┐  ┌───┴────┐
       │app│lgr  │    │app│lgr  │  │app│lgr│  │app│lgr │
       └─────────┘    └─────────┘  └───────┘  └────────┘
           ↑                ↑           ↑           ↑
        sidecar logger pattern: each Pod has a logger container
        tailing /var/log/app/access.log via shared emptyDir
```

### Deploy

```bash
cd networking/06-microservices/

kubectl apply -f 01-scripts-configmap.yaml
kubectl apply -f 02-secret.yaml
kubectl apply -f 03-order-service.yaml
kubectl apply -f 04-orders-service.yaml
kubectl apply -f 05-products-service.yaml
kubectl apply -f 06-notifications-service.yaml
kubectl apply -f 07-frontend.yaml

# or apply everything at once:
kubectl apply -f .
```

### Wait for all Pods to be Ready

```bash
kubectl get pods -l lab=06-microservices -w
```

### Hit the /ready Endpoint (see all Pod IPs)

```bash
# port-forward (works on all cluster types)
kubectl port-forward svc/frontend-svc 8090:8080
curl http://localhost:8090/ready | python3 -m json.tool

# minikube
curl $(minikube service frontend-svc --url)/ready

# kubeadm / cloud
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[0].address}')
curl http://${NODE_IP}:30090/ready
```

**Expected response:**

```json
{
  "frontend": {
    "service": "frontend",
    "pod_ip": "10.x.x.x",
    "status": "ready"
  },
  "order": {
    "service": "order-service",
    "pod_ip": "10.x.x.x",
    "status": "ready"
  },
  "orders": {
    "service": "orders-service",
    "pod_ip": "10.x.x.x",
    "status": "ready"
  },
  "products": {
    "service": "products-service",
    "pod_ip": "10.x.x.x",
    "status": "ready"
  },
  "notifications": {
    "service": "notifications-service",
    "pod_ip": "10.x.x.x",
    "status": "ready"
  }
}
```

### Observe the Logger Sidecar Pattern

```bash
# View both containers in the order-service pod:
kubectl get pod -l app=order-service

# App container stdout:
kubectl logs -l app=order-service -c app

# Logger sidecar reading the same access.log:
kubectl logs -l app=order-service -c logger

# Trigger some traffic then watch the logger sidecar pick it up:
kubectl port-forward svc/order-service 8081:8080 &
curl http://localhost:8081/ready
kubectl logs -l app=order-service -c logger
```

### Inspect ConfigMap and Secret in Action

```bash
# See the full ConfigMap:
kubectl get configmap frontend-config -o yaml

# See the secret (values are base64):
kubectl get secret app-secret -o yaml

# Decode a secret value:
kubectl get secret app-secret -o jsonpath='{.data.API_KEY}' | base64 -d

# Verify env vars are injected into the frontend pod:
kubectl exec -it $(kubectl get pod -l app=frontend -o name | head -1) -- env | grep -E "APP_ENV|API_KEY|_URL"
```

### Cleanup

```bash
kubectl delete -f networking/06-microservices/
```

---

## File Structure

```
networking/
├── 01-container-to-container.yaml   # Lab 1: localhost in a pod
├── 02-pod-to-pod.yaml               # Lab 2: direct pod IP (no service)
├── 03-clusterip.yaml                # Lab 3: ClusterIP service
├── 04-nodeport.yaml                 # Lab 4: NodePort service
├── 05-dns-discovery.yaml            # Lab 5: DNS names & FQDN
└── 06-microservices/
    ├── 01-scripts-configmap.yaml    # Python server scripts (server.py, frontend.py)
    ├── 02-secret.yaml               # API_KEY and JWT_SECRET
    ├── 03-order-service.yaml         # order  Deployment (app + logger sidecar) + ClusterIP
    ├── 04-orders-service.yaml       # orders Deployment + ClusterIP
    ├── 05-products-service.yaml     # products Deployment + ClusterIP
    ├── 06-notifications-service.yaml# notifications Deployment + ClusterIP
    └── 07-frontend.yaml             # frontend ConfigMap + Deployment + NodePort
```
