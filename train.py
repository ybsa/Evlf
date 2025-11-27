import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig
from trl import SFTTrainer

# Configuration
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct" # Open model, fits in 4GB VRAM
NEW_MODEL_NAME = "Evlf-Qwen2.5-1.5B"
DATASET_FILE = "datasets/original/sft_dataset.jsonl"
OUTPUT_DIR = "./results"

def train():
    print(f"Loading dataset from {DATASET_FILE}...")
    dataset = load_dataset("json", data_files=DATASET_FILE, split="train")

    # Quantization config for efficient training
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=False,
    )

    print(f"Loading model {MODEL_NAME}...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    # Qwen sometimes needs specific pad token handling if eos is not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # LoRA Config
    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.1,
        r=16, # Reduced r for memory
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )

    # Training Arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=1, # Lowest batch size for 4GB VRAM
        gradient_accumulation_steps=4, # Accumulate gradients to simulate larger batch
        optim="paged_adamw_32bit",
        save_steps=25,
        logging_steps=5,
        learning_rate=2e-4,
        weight_decay=0.001,
        fp16=False,
        bf16=False,
        max_grad_norm=0.3,
        max_steps=-1,
        warmup_ratio=0.03,
        group_by_length=True,
        lr_scheduler_type="constant",
    )

    print("Starting training...")
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="text", # We need to format the dataset first!
        max_seq_length=None,
        tokenizer=tokenizer,
        args=training_args,
        packing=False,
        formatting_func=format_instruction,
    )

    trainer.train()
    
    print(f"Saving model to {NEW_MODEL_NAME}...")
    trainer.model.save_pretrained(NEW_MODEL_NAME)
    trainer.tokenizer.save_pretrained(NEW_MODEL_NAME)

def format_instruction(sample):
    # Format: <|im_start|>user\n{instruction}<|im_end|>\n<|im_start|>assistant\n{response}<|im_end|>
    return [f"<|im_start|>user\n{row['instruction']}<|im_end|>\n<|im_start|>assistant\n{row['response']}<|im_end|>" for row in sample]

if __name__ == "__main__":
    # Check if dataset exists
    if not os.path.exists(DATASET_FILE):
        print(f"Error: {DATASET_FILE} not found.")
    else:
        train()
