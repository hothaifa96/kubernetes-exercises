# Lab 01 — Pod-to-Pod Communication: Nginx & Ubuntu

## Objective

Deploy two workloads inside a Kubernetes cluster — an **Nginx web server** and an **Ubuntu** container — then prove that one pod can reach the other over the cluster network.

The success flag is: curling Nginx from the Ubuntu pod and seeing the **"Welcome to nginx!"** HTML page printed in your terminal.

---

## Do You Need a Service?

**Yes.** Here is why.

When a pod is deleted and rescheduled, Kubernetes assigns it a new IP address. If Ubuntu tried to reach Nginx directly by pod IP, the connection would break every time the Nginx pod restarted.

A **Service** gives Nginx a stable virtual IP and a DNS name that never changes. Kubernetes' internal DNS (CoreDNS) resolves `<service-name>` to that stable IP, so Ubuntu can always find Nginx by name — regardless of pod churn.

### Which service type?

Use a **ClusterIP** service.

- ClusterIP is the default type.
- It exposes the service on a cluster-internal IP — reachable by any pod inside the cluster, but not from outside.
- No external access is needed here: Ubuntu and Nginx live in the same cluster, so ClusterIP is the right and most minimal choice.

---

## What You Need to Build

### 1. Nginx Deployment

- Use the official `nginx` image (any stable tag).
- Run **3 replicas** so you can observe traffic being distributed across pods later.
- Nginx listens on port **80** by default.

### 2. Nginx ClusterIP Service

- Expose the Nginx deployment on port **80**.
- Choose a clear, lowercase name for the service (you will use this name as the DNS hostname when you curl from Ubuntu).
- Target the Nginx pods using a label selector that matches your deployment.

### 3. Ubuntu Deployment

- Use the `ubuntu:22.04` image.
- Run **1 replica**.
- The container must be kept alive. Ubuntu's default command exits immediately — override it with a command that sleeps indefinitely so the pod stays in `Running` state.
- You do **not** need a service for Ubuntu; nothing needs to connect *to* it.

---

## Steps

1. Apply your manifests and wait for all pods to reach `Running` status.
2. List your pods and note the names of the Ubuntu and Nginx pods.
3. Open a shell session **inside the Ubuntu pod**.
4. From inside that shell, use `curl` to make an HTTP request to the Nginx service using its DNS name.
5. Read the output.

---

## Success Flag

Your terminal must display something like this:

```
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

If you see the **"Welcome to nginx!"** title in the HTML response, the lab is complete.

---
