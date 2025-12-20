import json
import os

def check_sizes():
    with open('training_tracker.json', 'r') as f:
        data = json.load(f)
    
    pending = [k for k, v in data['datasets'].items() if v.get('status') != 'completed']
    
    print("Pending Datasets and Sizes:")
    for path in pending:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            print(f"{path}: {lines} lines")
        else:
            print(f"{path}: File not found")

if __name__ == "__main__":
    check_sizes()
