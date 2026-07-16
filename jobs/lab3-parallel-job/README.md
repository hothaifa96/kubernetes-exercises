# Lab 3: Parallel Job with Completions

## Objective
Learn how to create a Kubernetes Job that runs multiple pods in parallel to process tasks concurrently.

## Files
- `parallel-job.yml` - Kubernetes Job manifest with parallelism settings
- `parallel_processor.py` - Python script for parallel processing

## Steps

### 1. Create the Job
```bash
kubectl apply -f parallel-job.yml
```

### 2. Monitor the Job
```bash
kubectl get jobs
kubectl get pods -l app=parallel-job
```

### 3. View Logs from Different Workers
```bash
# View logs from specific pods
kubectl logs -l app=parallel-job --show-all
```

### 4. Watch Parallel Execution
```bash
watch kubectl get pods -l app=parallel-job
```

### 5. Check Job Status
```bash
kubectl describe job parallel-image-processor
```

### 6. Clean Up
```bash
kubectl delete job parallel-image-processor
kubectl delete configmap parallel-script
```

## Key Concepts
- **completions**: Number of successful pod completions required (5 in this lab)
- **parallelism**: Number of pods running in parallel (2 in this lab)
- **JOB_COMPLETION_INDEX**: Environment variable that identifies each worker
- **Parallel Processing**: Multiple workers process tasks simultaneously

## How It Works
1. Job requires 5 completions (total tasks)
2. Runs 2 pods in parallel at any time
3. Each pod processes a portion of the work
4. When a pod completes, a new one starts until 5 completions are reached
5. Each worker has a unique completion index

## Expected Behavior
- You'll see 2 pods running simultaneously
- As each pod completes, new pods start
- Total of 5 pods will complete the job
- Each worker processes independently with random processing times
