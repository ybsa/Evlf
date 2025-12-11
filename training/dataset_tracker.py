import os
import json
import glob
from datetime import datetime

class DatasetTracker:
    """Track which datasets have been trained and which are remaining."""
    
    TRACKER_FILE = "training_tracker.json"
    
    def __init__(self):
        self.load_tracker()
    
    def load_tracker(self):
        """Load the training tracker from file."""
        if os.path.exists(self.TRACKER_FILE):
            with open(self.TRACKER_FILE, 'r') as f:
                self.tracker = json.load(f)
        else:
            self.tracker = {
                "last_updated": None,
                "datasets": {}
            }
    
    def save_tracker(self):
        """Save the training tracker to file."""
        self.tracker["last_updated"] = datetime.now().isoformat()
        with open(self.TRACKER_FILE, 'w') as f:
            json.dump(self.tracker, f, indent=2)
    
    def get_all_datasets(self):
        """Get all available dataset files."""
        datasets = []
        
        # Search in all subdirectories
        base_dir = os.path.dirname(os.path.abspath(__file__))
        datasets_dir = os.path.join(base_dir, '..', 'datasets')
        
        for category in ['core', 'human_like', 'themed', 'original']:
            category_path = os.path.join(datasets_dir, category)
            if os.path.exists(category_path):
                for file in glob.glob(os.path.join(category_path, '*.jsonl')):
                    datasets.append({
                        'path': file,
                        'category': category,
                        'name': os.path.basename(file)
                    })
        
        return datasets
    
    def mark_trained(self, dataset_path, checkpoint_count, final_model_path=None):
        """Mark a dataset as trained."""
        self.tracker["datasets"][dataset_path] = {
            "status": "completed",
            "trained_at": datetime.now().isoformat(),
            "checkpoint_count": checkpoint_count,
            "model_path": final_model_path
        }
        self.save_tracker()
    
    def mark_in_progress(self, dataset_path):
        """Mark a dataset as currently training."""
        self.tracker["datasets"][dataset_path] = {
            "status": "in_progress",
            "started_at": datetime.now().isoformat()
        }
        self.save_tracker()
    
    def mark_failed(self, dataset_path, error):
        """Mark a dataset training as failed."""
        self.tracker["datasets"][dataset_path] = {
            "status": "failed",
            "failed_at": datetime.now().isoformat(),
            "error": str(error)
        }
        self.save_tracker()
    
    def get_training_status(self):
        """Get the status of all datasets."""
        all_datasets = self.get_all_datasets()
        
        status = {
            "completed": [],
            "in_progress": [],
            "failed": [],
            "pending": []
        }
        
        for dataset in all_datasets:
            path = dataset['path']
            if path in self.tracker["datasets"]:
                dataset_status = self.tracker["datasets"][path]["status"]
                dataset['details'] = self.tracker["datasets"][path]
                status[dataset_status].append(dataset)
            else:
                status["pending"].append(dataset)
        
        return status
    
    def display_status(self):
        """Display the training status in a nice format."""
        status = self.get_training_status()
        
        print("\n" + "=" * 70)
        print("📚 DATASET TRAINING TRACKER")
        print("=" * 70)
        
        total = sum(len(status[k]) for k in status)
        completed = len(status["completed"])
        in_progress = len(status["in_progress"])
        failed = len(status["failed"])
        pending = len(status["pending"])
        
        print(f"\n📊 Overall Progress: {completed}/{total} datasets trained")
        print(f"   ✅ Completed: {completed}")
        print(f"   🔄 In Progress: {in_progress}")
        print(f"   ❌ Failed: {failed}")
        print(f"   ⏳ Pending: {pending}")
        
        if status["completed"]:
            print("\n" + "-" * 70)
            print("✅ COMPLETED DATASETS:")
            for ds in status["completed"]:
                print(f"   • {ds['category']}/{ds['name']}")
                if 'trained_at' in ds['details']:
                    trained_time = ds['details']['trained_at'].split('T')[0]
                    print(f"     Trained: {trained_time}")
        
        if status["in_progress"]:
            print("\n" + "-" * 70)
            print("🔄 IN PROGRESS:")
            for ds in status["in_progress"]:
                print(f"   • {ds['category']}/{ds['name']}")
        
        if status["failed"]:
            print("\n" + "-" * 70)
            print("❌ FAILED:")
            for ds in status["failed"]:
                print(f"   • {ds['category']}/{ds['name']}")
                if 'error' in ds['details']:
                    print(f"     Error: {ds['details']['error'][:50]}...")
        
        if status["pending"]:
            print("\n" + "-" * 70)
            print("⏳ PENDING DATASETS:")
            for ds in status["pending"]:
                print(f"   • {ds['category']}/{ds['name']}")
        
        print("\n" + "=" * 70)
        
        return status

if __name__ == "__main__":
    tracker = DatasetTracker()
    tracker.display_status()
