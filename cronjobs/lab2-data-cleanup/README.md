# Lab 2: Data Cleanup CronJob

## Objective
Learn how to create a CronJob that performs automated data cleanup tasks, removing old files based on age.

## Key Concepts
- **schedule**: Runs daily at 2 AM (0 2 * * *)
- **concurrencyPolicy: Forbid**: Prevents overlapping job executions
- **Environment Variables**: Configure cleanup behavior (CLEANUP_DAYS, DRY_RUN)
- **emptyDir Volume**: Temporary storage for sample data
- **ConfigMap**: Stores the cleanup script

## Configuration Options
- `CLEANUP_DAYS`: Number of days to keep files (default: 7)
- `DRY_RUN`: Set to "true" to simulate cleanup without deleting

## What It Does
The CronJob:
1. Generates sample data files with various ages
2. Scans the data directory
3. Identifies files older than the retention period
4. Deletes old files (or simulates deletion in dry-run mode)
5. Reports cleanup statistics

## Expected Output
Each execution will:
- Display cleanup configuration
- Show sample data generation
- List files to be deleted
- Report cleanup statistics
- Show total size freed

## Use Cases
- Log file cleanup
- Temporary file removal
- Database backup cleanup
- Cache management
- Old data archival
