"""
Rebalance Datasets for Natural Girlfriend Persona
Reduces academic/formal datasets and ensures relationship focus.
"""

import json
import os
import random

# Configuration
DATASETS_TO_REDUCE = {
    "datasets/human_like/dataset_philosophy.jsonl": 50,      # Keep 50 examples
    "datasets/human_like/dataset_problem_solving.jsonl": 30, # Keep 30 examples
    "datasets/human_like/dataset_advice_wisdom.jsonl": 60    # Keep 60 examples
}

def rebalance_file(filepath, target_count):
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filepath}")
        return

    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"  - Original size: {total_lines}")
    
    if total_lines <= target_count:
        print(f"  - Already small enough. Skipping.")
        return

    # Filter for relationship/emotional content if possible, otherwise random sample
    # For simplicity in this script, we'll do random sampling but prioritize shorter responses
    # which tend to be less "lecture-y"
    
    data = [json.loads(line) for line in lines]
    
    # Simple heuristic: prefer examples with "love", "feel", "you", "we" in instruction or response
    keywords = ["love", "feel", "you", "we", "relationship", "heart", "care"]
    
    priority_data = []
    other_data = []
    
    for item in data:
        text = (item['instruction'] + " " + item['response']).lower()
        if any(k in text for k in keywords):
            priority_data.append(item)
        else:
            other_data.append(item)
            
    print(f"  - Found {len(priority_data)} priority examples (containing keywords)")
    
    # Select examples
    selected = []
    
    # Take all priority ones up to target
    if len(priority_data) >= target_count:
        selected = random.sample(priority_data, target_count)
    else:
        selected = priority_data
        # Fill rest from other_data
        remaining_needed = target_count - len(selected)
        if remaining_needed > 0 and other_data:
            selected.extend(random.sample(other_data, min(len(other_data), remaining_needed)))
    
    print(f"  - Selected {len(selected)} examples")
    
    # Save back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in selected:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
    print(f"  - ✅ Saved rebalanced file.")

if __name__ == "__main__":
    print("🔄 Starting Dataset Rebalancing...")
    
    for filepath, count in DATASETS_TO_REDUCE.items():
        # Fix path for Windows if needed
        filepath = filepath.replace("/", os.sep)
        rebalance_file(filepath, count)
        
    print("\n✨ Rebalancing Complete!")
