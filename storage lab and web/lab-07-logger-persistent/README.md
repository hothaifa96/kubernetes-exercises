# Lab 07 — Persistent Logger Application with PV, PVC, and StorageClass

## Objective

Deploy a Flask-based logger application to Minikube that writes logs to a persistent volume. When the pod is deleted and recreated, the logs must persist, demonstrating the value of PersistentVolumes, PersistentVolumeClaims, and StorageClasses.

This lab teaches:

- How to create a custom StorageClass in Minikube
- How to dynamically provision a PersistentVolume using a StorageClass
- How to create a PersistentVolumeClaim to request storage
- How to mount a PVC in a pod
- How to verify that data persists across pod restarts

---

## Repository Structure

```
lab-07-logger-persistent/
├── README.md              ← this file
├── app.py                 ← Flask logger API
├── requirements.txt
└── Dockerfile
```

---

## Application Overview

The logger application is a simple Flask API that:

- Accepts log messages via POST `/api/log` with `level` and `message`
- Retrieves logs via GET `/api/logs`
- Shows statistics via GET `/api/stats`
- Clears logs via POST `/api/clear`
- Writes all logs to a file at `/logs/application.log`

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check, shows log directory and file path |
| POST | `/api/log` | Write a log entry. Body: `{"level": "INFO", "message": "text"}` |
| GET | `/api/logs?lines=100` | Retrieve last N log lines |
| GET | `/api/stats` | Get log statistics (total lines, file size, level counts) |
| POST | `/api/clear` | Clear the log file |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_DIR` | Directory where log file is written | `/logs` |
| `PORT` | Port the Flask server listens on | `5000` |

---

## What You Need to Build

### Step 1 — Build and Push the Docker Image

Build the image locally, tag it, and make it available to Minikube.

```
docker build -t <your-registry>/logger-app:v1 .
```

> **Hint for Minikube:** If you're using Minikube with Docker daemon, you can load the image directly:
> ```
> minikube image load logger-app:v1
> ```
> Then use `imagePullPolicy: Never` in your deployment.

### Step 2 — Create a Custom StorageClass

Minikube comes with a default StorageClass called `standard`. For this lab, create a custom StorageClass to understand how they work.

Create a StorageClass with the following specifications:

- **Name:** `logger-storage`
- **Provisioner:** `k8s.io/minikube-hostpath`
- **Reclaim Policy:** `Retain` (so data survives PVC deletion)
- **Volume Binding Mode:** `WaitForFirstConsumer`

> **Hint:** The `WaitForFirstConsumer` mode delays volume binding until a pod using the PVC is scheduled. This is useful for topology-aware provisioning.

### Step 3 — Create a PersistentVolumeClaim

Create a PVC that requests storage from your custom StorageClass.

- **Name:** `logger-pvc`
- **Storage Request:** `1Gi`
- **Access Mode:** `ReadWriteOnce`
- **StorageClass:** `logger-storage`

> **Hint:** When you create this PVC, the StorageClass will dynamically provision a PV. Verify this with `kubectl get pv`.

### Step 4 — Deploy the Logger Application

Create a Deployment for the logger application with:

- **Replicas:** 1
- **Image:** Your logger image
- **Port:** 5000
- **Volume Mount:** Mount the PVC at `/logs`
- **Environment Variable:** Set `LOG_DIR` to `/logs`

> **Hint:** The volume mount in the container spec should reference the PVC by name in the volumes section.

### Step 5 — Create a Service

Create a Service to expose the logger application.

- **Type:** NodePort (so you can access it from your machine)
- **Port:** 5000
- **TargetPort:** 5000
- **NodePort:** Choose a port in 30000-32767

---

## Verification Steps

### 1. Apply All Manifests

Apply in order: StorageClass → PVC → Deployment → Service

```
kubectl apply -f storageclass.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 2. Verify Resources

Check that all resources are created:

```
kubectl get storageclass
kubectl get pvc
kubectl get pv
kubectl get pods
kubectl get svc
```

> **Hint:** The PVC status should be `Bound` and the PV status should be `Bound`. If the PVC is `Pending`, check the events with `kubectl describe pvc logger-pvc`.

### 3. Write Some Logs

Get the NodePort and send log entries:

```
export NODEPORT=$(kubectl get svc logger-service -o jsonpath='{.spec.ports[0].nodePort}')
export MINIKUBE_IP=$(minikube ip)

curl -X POST http://$MINIKUBE_IP:$NODEPORT/api/log \
  -H "Content-Type: application/json" \
  -d '{"level": "INFO", "message": "First log entry"}'

curl -X POST http://$MINIKUBE_IP:$NODEPORT/api/log \
  -H "Content-Type: application/json" \
  -d '{"level": "ERROR", "message": "Something went wrong"}'

curl -X POST http://$MINIKUBE_IP:$NODEPORT/api/log \
  -H "Content-Type: application/json" \
  -d '{"level": "DEBUG", "message": "Debugging info"}'
```

### 4. Retrieve Logs

```
curl http://$MINIKUBE_IP:$NODEPORT/api/logs
```

You should see all three log entries.

### 5. Check Statistics

```
curl http://$MINIKUBE_IP:$NODEPORT/api/stats
```

You should see the count of log entries by level.

### 6. **The Persistence Test — Delete the Pod**

This is the critical step that proves persistence works.

```
kubectl delete pod -l app=logger
```

Wait for the new pod to be created and reach `Running` state.

### 7. Verify Logs Persist

Retrieve the logs again:

```
curl http://$MINIKUBE_IP:$NODEPORT/api/logs
```

**Success Criteria:** The logs from step 4 must still be present. If they are gone, the PVC was not properly mounted or the reclaim policy was wrong.

### 8. Check Statistics Again

```
curl http://$MINIKUBE_IP:$NODEPORT/api/stats
```

The `total_lines` count should be the same as before the pod deletion.

---

## Success Criteria

| Check | Expected |
|-------|----------|
| StorageClass created | ✓ `logger-storage` exists in `kubectl get sc` |
| PVC bound | ✓ `logger-pvc` status is `Bound` |
| PV provisioned | ✓ A PV exists and is bound to the PVC |
| Pod running | ✓ Logger pod is `Running` |
| Logs written | ✓ Can write and retrieve log entries |
| **Logs persist after pod deletion** | ✓ Logs remain after pod is recreated |
| PVC remains after pod deletion | ✓ PVC is still `Bound` to the same PV |

---

## Troubleshooting

### PVC Stays in Pending State

- Check events: `kubectl describe pvc logger-pvc`
- Verify the StorageClass exists: `kubectl get sc`
- Ensure the StorageClass name in the PVC matches exactly

### Pod Crashes with Permission Denied

- The hostPath provisioner may have permission issues. Try changing the reclaim policy to `Delete` and recreate.

### Logs Disappear After Pod Restart

- Verify the PVC is mounted: `kubectl describe pod <logger-pod>` should show the volume mount
- Check the `LOG_DIR` environment variable is set to `/logs`
- Ensure the PVC is still bound: `kubectl get pvc`

### Cannot Access Service from Host

- Verify the NodePort: `kubectl get svc`
- Check Minikube is running: `minikube status`
- Try using `minikube service logger-service --url` to get the correct URL

---

## Bonus Challenges

1. **Multiple Pods, Shared Storage:** Deploy 2 replicas of the logger. Can both write to the same PVC? Why or why not? (Hint: `ReadWriteOnce` vs `ReadWriteMany`)

2. **StorageClass Comparison:** Create a second StorageClass with `reclaimPolicy: Delete`. Create a second PVC using it. Compare what happens when you delete each PVC.

3. **Log Rotation:** Modify the application to implement log rotation when the file exceeds a certain size. Test that the PVC handles this correctly.

4. **Backup Strategy:** Implement a backup strategy by creating a second pod that mounts the same PVC and copies the log file to another location.

5. **Prometheus Integration:** Add Prometheus metrics to the logger application to track log rates by level.

---

## Concepts to Understand After This Lab

- The lifecycle relationship between StorageClass, PV, and PVC
- How dynamic provisioning works and when it's triggered
- The difference between `Retain` and `Delete` reclaim policies
- Why `ReadWriteOnce` limits mounting to a single node
- How volume binding modes affect scheduling (`Immediate` vs `WaitForFirstConsumer`)
- How to verify that data persists across pod restarts
- The role of the provisioner in creating actual storage
- Why separating storage from compute is important for stateful applications
