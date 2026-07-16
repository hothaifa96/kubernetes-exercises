# Lab 1: Health Check CronJob

## Objective
Learn how to create a CronJob that performs periodic health checks on services.

## Files
- `cronjob-health.yml` - Kubernetes CronJob manifest
- `health_check.py` - Python backend script for health checks

## Steps

### 1. Create the CronJob
```bash
kubectl apply -f cronjob-health.yml
```

### 2. Monitor the CronJob
```bash
kubectl get cronjobs
kubectl get jobs
kubectl get pods
```

### 3. View Logs from Latest Job
```bash
# Get the latest job
kubectl get jobs --sort-by=.metadata.creationTimestamp

# View logs
kubectl logs -l app=health-check --tail=-1
```

### 4. Check CronJob Status
```bash
kubectl describe cronjob health-check-cronjob
```

### 5. Clean Up
```bash
kubectl delete cronjob health-check-cronjob
```

## Key Concepts
- **schedule**: Cron expression defining when to run (*/5 * * * * = every 5 minutes)
- **successfulJobsHistoryLimit**: Keep only 3 successful job histories
- **failedJobsHistoryLimit**: Keep only 1 failed job history
- **jobTemplate**: Template for the Job that the CronJob creates

## Schedule Format
```
* * * * *
│ │ │ │ │
│ │ │ │ └─ Day of week (0-6, Sunday=0)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

## What It Does
The CronJob:
- Runs every 5 minutes
- Checks Google accessibility
- Checks Kubernetes API connectivity
- Performs DNS resolution tests
- Outputs health check results

## Expected Output
Each execution will:
- Display start time
- Check HTTP services
- Verify DNS resolution
- Show health check summary
- Display completion time
