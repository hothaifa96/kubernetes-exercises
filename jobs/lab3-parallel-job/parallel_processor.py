import os
import time
import random
from datetime import datetime

def main():
    # Get job completion index
    completion_index = os.environ.get('JOB_COMPLETION_INDEX', '0')
    
    print("=" * 60)
    print(f"Parallel Job - Worker {completion_index}")
    print("=" * 60)
    print()
    
    print(f"1. Worker {completion_index} started at {datetime.now().isoformat()}")
    
    # Simulate processing time
    processing_time = random.randint(3, 8)
    print(f"2. Processing task (estimated time: {processing_time} seconds)...")
    
    # Simulate work
    for i in range(processing_time):
        time.sleep(1)
        print(f"   Progress: {i+1}/{processing_time} - Worker {completion_index}")
    
    # Generate result
    result = {
        "worker_id": completion_index,
        "processed_items": random.randint(10, 50),
        "processing_time": processing_time,
        "status": "completed",
        "completed_at": datetime.now().isoformat()
    }
    
    print()
    print(f"3. Worker {completion_index} result:")
    print(f"   - Processed items: {result['processed_items']}")
    print(f"   - Processing time: {result['processing_time']}s")
    print(f"   - Status: {result['status']}")
    
    print()
    print("=" * 60)
    print(f"Worker {completion_index} completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
