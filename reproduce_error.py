
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "training"))
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from training.train_multi_dataset import format_instruction

# Load dataset
dataset_path = "datasets/core/dataset_evlf_persona.jsonl"
dataset = load_dataset("json", data_files=dataset_path, split="train")

# Mock model and tokenizer (to avoid loading big model)
# We can use a tiny model or just skip model loading if possible?
# SFTTrainer needs a model or model_init.
# Let's try to use a very small model or just the tokenizer.
model_name = "gpt2" # fast to load
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

training_args = SFTConfig(
    output_dir="tmp_test",
    dataset_text_field="text",
    max_length=128,
    packing=False,
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
# We don't need to actually train, just initialization often triggers the map
# But map is lazy? No, SFTTrainer runs map in init.
print("SFTTrainer init complete.")
