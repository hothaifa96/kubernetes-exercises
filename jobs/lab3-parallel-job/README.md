# Lab 3: Parallel Job with Completions


## Steps

### 1. Create the Job
### 2. Monitor the Job
### 3. View Logs from Different Workers
```bash

kubectl logs -l app=parallel-job --show-all
```

### 4. Watch Parallel Execution
```bash
watch kubectl get pods -l app=parallel-job
```

### 5. Check Job Status

## Key Concepts
- **completions**: Number of successful pod completions required (5 in this lab)
- **parallelism**: Number of pods running in parallel (2 in this lab)
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
