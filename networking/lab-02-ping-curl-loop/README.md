# Lab 02 — Containerised Network Probe: Ping & Curl Loop

## Objective

Take a provided Bash script that **continuously pings and curls a target host**, containerise it with the provided Dockerfile, push it to a registry, and deploy it inside Kubernetes alongside an Nginx workload.

The probe container must reach Nginx using the service's DNS name — passed in as an environment variable — and you must verify the traffic by reading the pod's logs.

---

## What Is Provided

| File | Purpose |
|------|---------|
| `ping-curl.sh` | Bash loop that reads `TARGET` env var and repeatedly pings and curls it |
| `Dockerfile` | Builds an Ubuntu-based image with `curl` and `ping` installed |

The script respects a single environment variable:

| Variable | Description | Default |
|----------|-------------|---------|
| `TARGET` | Hostname or IP to ping and curl | `localhost` |

---

## What You Need to Build

### 1. Build and Push the Docker Image

- Build the image from the provided `Dockerfile`.
- Tag it with your Docker Hub username or your private registry URL.
- Push it so Kubernetes can pull it during pod scheduling.

### 2. Nginx Deployment + ClusterIP Service

- Deploy Nginx (same as Lab 01, or reuse it).
- Create a ClusterIP service in front of it.
- Note the service name — that becomes the DNS hostname inside the cluster.

### 3. Network Probe Deployment

- Create a Deployment that runs **1 replica** of your custom probe image.
- Set the `TARGET` environment variable to the **DNS name of the Nginx service**.
  - Within the same namespace the DNS name is simply the service name.
  - Across namespaces it follows the pattern: `<service-name>.<namespace>.svc.cluster.local`
- The container will start probing immediately on startup.

---

## Steps

1. Build the image locally:
   ```
   docker build -t <your-registry>/<image-name>:<tag> .
   docker push <your-registry>/<image-name>:<tag>
   ```
2. Apply your Nginx deployment and service manifests.
3. Apply your probe deployment manifest.
4. Wait for pods to reach `Running`.
5. Tail the logs of the probe pod:
   ```
   kubectl logs -f <probe-pod-name>
   ```
6. Read the output.

---

## Success Flag

Your pod logs must show a repeating pattern like this:

```
========================================
  Timestamp: Mon Jul  7 09:00:00 UTC 2025
  Target: nginx-service
========================================

--- PING ---
PING nginx-service (10.96.x.x) 56(84) bytes of data.
[INFO] Ping did not get response — ClusterIP services may not respond to ICMP. This is expected.

--- CURL ---
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

> **Note on ICMP:** ClusterIP virtual IPs are implemented via iptables/eBPF rules and typically do **not** respond to ICMP echo requests. Ping showing no reply is expected and correct — it still proves DNS resolution worked. The curl output is the real proof of connectivity.

---

## Bonus Challenges

- Scale Nginx to 3 replicas. Deploy **3 replicas of the probe** as well. Observe via logs whether different probes hit different Nginx pods (you would need to customise the Nginx response per pod to tell them apart).
- Change the `TARGET` to a hostname that does not exist and observe the DNS failure in the logs.
- Point `TARGET` to a pod IP directly (not a service) and restart the Nginx pod. What happens to the probe logs?

---
