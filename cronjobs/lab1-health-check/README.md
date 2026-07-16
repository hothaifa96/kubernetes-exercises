# Lab 1: Health Check CronJob

## Objective
Learn how to create a CronJob that performs periodic health checks on services.


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
