
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "training"))
from datasets import load_dataset
from training.train_multi_dataset import format_instruction

dataset_path = "datasets/core/dataset_evlf_persona.jsonl"

print(f"Loading {dataset_path}...")
try:
    dataset = load_dataset("json", data_files=dataset_path, split="train")
    print(f"Loaded {len(dataset)} examples.")
except Exception as e:
    print(f"Failed to load dataset: {e}")
    exit(1)

print("Checking ALL examples...")
for i in range(len(dataset)):
    example = dataset[i]
    
    if not isinstance(example['instruction'], str):
        print(f"ERROR at index {i}: instruction is {type(example['instruction'])}")
        print(example['instruction'])
    
    if not isinstance(example['response'], str):
        print(f"ERROR at index {i}: response is {type(example['response'])}")
        print(example['response'])
        
    # Test formatting
    formatted = format_instruction(example)
    if not isinstance(formatted, str):
        print(f"ERROR at index {i}: Formatted is {type(formatted)}")
        if isinstance(formatted, list):
            print(f"  Length: {len(formatted)}")

print("Finished checking all examples.")
