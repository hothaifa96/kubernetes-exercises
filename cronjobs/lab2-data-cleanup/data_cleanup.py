import os
import json
import time
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample data for cleanup demonstration"""
    data_dir = "/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Create sample files with different ages
    for i in range(20):
        filename = f"data_{i}.json"
        filepath = os.path.join(data_dir, filename)
        
        # Random age between 1-30 days
        age_days = random.randint(1, 30)
        created_date = datetime.now() - timedelta(days=age_days)
        
        data = {
            "id": i,
            "created_at": created_date.isoformat(),
            "content": f"Sample data record {i}",
            "size": random.randint(100, 1000)
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f)
        
        # Set file modification time
        import stat
        ts = created_date.timestamp()
        os.utime(filepath, (ts, ts))

def cleanup_old_files(data_dir, days_to_keep, dry_run):
    """Clean up files older than specified days"""
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    files_deleted = []
    files_kept = []
    total_size_freed = 0
    
    print(f"Scanning directory: {data_dir}")
    print(f"Cutoff date: {cutoff_date.isoformat()}")
    print(f"Days to keep: {days_to_keep}")
    print(f"Dry run: {dry_run}")
    print()
    
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} does not exist")
        return files_deleted, files_kept, total_size_freed
    
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        
        if os.path.isfile(filepath):
            # Get file modification time
            mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            file_size = os.path.getsize(filepath)
            
            if mod_time < cutoff_date:
                if not dry_run:
                    os.remove(filepath)
                    total_size_freed += file_size
                
                files_deleted.append({
                    "filename": filename,
                    "modified_date": mod_time.isoformat(),
                    "size": file_size
                })
            else:
                files_kept.append({
                    "filename": filename,
                    "modified_date": mod_time.isoformat(),
                    "size": file_size
                })
    
    return files_deleted, files_kept, total_size_freed

def main():
    print("=" * 60)
    print("Data Cleanup CronJob - Backend")
    print("=" * 60)
    print()
    
    cleanup_days = int(os.environ.get('CLEANUP_DAYS', '7'))
    dry_run = os.environ.get('DRY_RUN', 'false').lower() == 'true'
    data_dir = "/data"
    
    print(f"Starting data cleanup at {datetime.now().isoformat()}")
    print()
    
    # Generate sample data for demonstration
    print("1. Generating sample data...")
    generate_sample_data()
    print(f"   Sample data created in {data_dir}")
    print()
    
    # Perform cleanup
    print("2. Performing cleanup...")
    files_deleted, files_kept, size_freed = cleanup_old_files(
        data_dir, cleanup_days, dry_run
    )
    print()
    
    # Display results
    print("3. Cleanup Results:")
    print(f"   Files deleted: {len(files_deleted)}")
    print(f"   Files kept: {len(files_kept)}")
    print(f"   Size freed: {size_freed} bytes")
    print()
    
    if files_deleted:
        print("4. Deleted Files:")
        for f in files_deleted[:5]:  # Show first 5
            print(f"   - {f['filename']} (modified: {f['modified_date']})")
        if len(files_deleted) > 5:
            print(f"   ... and {len(files_deleted) - 5} more")
    
    print()
    print("=" * 60)
    print("Data cleanup completed!")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    exit(main())
