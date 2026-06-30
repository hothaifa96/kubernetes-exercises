# Lab: Deploy MongoDB and Mongo Express using ReplicaSets

## Objective

In this lab you will learn how to:

- Create ReplicaSets
- Use labels and selectors
- Configure environment variables
- Expose an application using a NodePort Service
- Allow one application to communicate with another using a Kubernetes Service

---

# So...

Your company wants to deploy a MongoDB database along with a Mongo Express web interface.

Mongo Express should connect to MongoDB using a Kubernetes Service.

Your task is to deploy both applications using ReplicaSets.

---

# Architecture

Browser
│
▼
NodePort Service
│
▼
Mongo Express ReplicaSet (2 Pods)
│
▼
Mongo Service (NodePort)
│
▼
Mongo ReplicaSet (1 Pod)

---

# Requirements

## MongoDB ReplicaSet

ReplicaSet Name

```
mongo-rs
```

Replicas

```
1
```

Image

```
mongo:7
```

Container Port

```
27017
```

Environment Variables

```
MONGO_INITDB_ROOT_USERNAME=

MONGO_INITDB_ROOT_PASSWORD=
```

---

## Mongo Service

Name

```
mongo-service
```

Type

```
NodePort
```

Port

```
27017
```

---

## Mongo Express ReplicaSet

ReplicaSet Name

```
mongo-express-rs
```

Replicas

```
2
```

Image

```
mongo-express:latest
```

Container Port

```
8081
```

Environment Variables

```
ME_CONFIG_MONGODB_ADMINUSERNAME=

ME_CONFIG_MONGODB_ADMINPASSWORD=

ME_CONFIG_MONGODB_SERVER=

ME_CONFIG_BASICAUTH_USERNAME=

ME_CONFIG_BASICAUTH_PASSWORD=

```

---

## Mongo Express Service

Name

```
mongo-express-service
```

Type

```
NodePort
```

Port

```
8081
```

NodePort

```
30081
```

---

# Tasks

1. Create the MongoDB ReplicaSet.
2. Create the MongoDB ClusterIP Service.
3. Verify MongoDB is running.
4. Create the Mongo Express ReplicaSet.
5. Create the Mongo Express NodePort Service.
6. Verify both ReplicaSets.
7. Scale Mongo Express to **4 replicas**.
8. Scale Mongo Express back to **2 replicas**.
9. Open:

```
http://<MINIKUBE-IP>:30081
```
or use :
```
kubectl service mongo-express-service
```

10. Verify Mongo Express successfully connects to MongoDB.

---

