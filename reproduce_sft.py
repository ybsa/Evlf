
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "training"))
from datasets import Dataset
from trl import SFTTrainer, SFTConfig
from transformers import AutoTokenizer

# Dummy dataset
data = {
    "instruction": ["Hello", "Hi"],
    "response": ["World", "There"]
}
dataset = Dataset.from_dict(data)

# Dummy tokenizer
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def format_instruction(sample):
    if isinstance(sample['instruction'], list):
        print(f"DEBUG: Batched input. Len: {len(sample['instruction'])}")
        return [f"{i} {r}" for i, r in zip(sample['instruction'], sample['response'])]
    else:
        print(f"DEBUG: Single input.")
        return f"{sample['instruction']} {sample['response']}"

training_args = SFTConfig(
    output_dir="tmp_test_sft",
    max_length=128,
    packing=False,
    # dataset_text_field="text", # Intentionally commented out
)

print("Initializing SFTTrainer...")
trainer = SFTTrainer(
    model=model_name,
    train_dataset=dataset,
    args=training_args,
    formatting_func=format_instruction,
    processing_class=tokenizer,
)

print("Training (dry run)...")
print("SFTTrainer init complete.")
