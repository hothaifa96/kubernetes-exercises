# Lab 2: Python Job with Data Processing

- `data_processor.py` - Python script for data processing

## Steps

### 1. Create the Job
### 2. Monitor the Job
### 3. View Job Logs
### 4. Check Job Status
### 5. Clean Up

- **ConfigMap**: Stores the Python script as configuration data
- **Volume Mount**: Mounts the ConfigMap as a file in the container
- **Python Container**: Uses Python 3.11 slim image for efficient execution
- **Data Processing**: Demonstrates generating, processing, and analyzing data

## What the Script Does
1. Generates 10 sample data records with random values
2. Processes each record and calculates statistics
3. Outputs total value and average
4. Displays results in JSON format

## Expected Output
The job will:
- Generate random data records
- Process and display each record
- Calculate and show statistics
- Output final results in JSON format


think of how can we save all the script in a config map and run it from the script !
search the web for it :)