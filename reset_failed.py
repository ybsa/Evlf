import json

tracker_file = "training/training_tracker.json"

with open(tracker_file, 'r') as f:
    data = json.load(f)

# Move failed to pending (delete from datasets dict)
failed_paths = []
for path, info in data['datasets'].items():
    if info['status'] == 'failed':
        failed_paths.append(path)

for path in failed_paths:
    del data['datasets'][path]
    print(f"Reset {path}")

with open(tracker_file, 'w') as f:
    json.dump(data, f, indent=2)

print("✅ Reset all failed datasets to pending.")
