# Lab 3: Scheduled Reporting CronJob

## Objective
Learn how to create a CronJob that generates scheduled reports with system and service metrics.

## Key Concepts
- **schedule**: Runs every Monday at 9 AM (0 9 * * 1)
- **concurrencyPolicy: Allow**: Allows overlapping job executions
- **successfulJobsHistoryLimit: 5**: Keeps last 5 successful reports
- **Environment Variables**: Configure report behavior
- **Report Generation**: Collects metrics and generates structured reports

## Configuration Options
- `REPORT_TYPE`: Type of report (weekly, daily, monthly)
- `EMAIL_RECIPIENT`: Email address for report delivery
- `REPORT_FORMAT`: Output format (json, csv, html)

## What It Does
The CronJob:
1. Collects system-wide metrics (CPU, memory, requests)
2. Gathers per-service metrics (response time, uptime, errors)
3. Generates a comprehensive report
4. Saves report to persistent storage
5. Provides health status and recommendations

## Report Contents
- **System Metrics**: Total requests, errors, cluster resources
- **Service Metrics**: Per-service performance data
- **Summary**: Health status, issues, warnings
- **Recommendations**: Actionable insights

## Expected Output
Each execution will:
- Display report configuration
- Show system metrics collection
- List service performance data
- Generate and save report
- Provide summary and recommendations

## Use Cases
- Weekly performance reports
- Monthly capacity planning
- Daily health summaries
- SLA compliance reporting
- Cost optimization analysis
