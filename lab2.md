# Lab: Deploy a Frontend and Backend using ReplicaSets

## Objective

Learn how ReplicaSets communicate using Kubernetes Services.

---

# So...

Your company has a small web application.

The application consists of:

- Backend API
- Frontend Web UI

The frontend communicates with the backend using a Kubernetes Service.

---

# Architecture

Browser
│
▼
Frontend NodePort Service
│
▼
Frontend ReplicaSet (3 Pods)
│
▼
Backend Service (NodePort)
│
▼
Backend ReplicaSet (2 Pods)

---

# Requirements

## Backend ReplicaSet

Name

```
backend-rs
```

Replicas

```
2
```

Image

```
traefik/whoami
```

Port

```
80
```

Labels

```
app=backend
```

---

## Backend Service

Name

```
backend-service
```

Type

```
NodePort
```

Port

```
80
```

---

## Frontend ReplicaSet

Name

```
frontend-rs
```

Replicas

```
3
```

Image

```
nginxdemos/hello
```

Port

```
80
```

Labels

```
app=frontend
```

---

## Frontend NodePort Service

Name

```
frontend-service
```

Type

```
NodePort
```

Port

```
80
```

NodePort

```
30080
```

---

# Tasks

1. Create the Backend ReplicaSet.
2. Create the Backend Service.
3. Create the Frontend ReplicaSet.
4. Create the Frontend NodePort Service.
5. Verify all ReplicaSets are running.
6. Scale Backend to **4 replicas**.
7. Scale Frontend to **5 replicas**.
8. Describe both ReplicaSets.
9. Verify the Services have endpoints.
10. Open

```
http://<MINIKUBE-IP>:30080
```

or 

```
kubectl service frontend-service
```

---

# Bonus Challenge

Modify the frontend container so that it displays the backend Service name somewhere on the page (hint: use environment variables or a custom Nginx configuration).

---
