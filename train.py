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
MODEL_NAME = "NousResearch/Llama-2-7b-chat-hf" # Using a solid base model
NEW_MODEL_NAME = "Evlf-Llama-2-7b"
DATASET_FILE = "sft_dataset.jsonl"
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
    tokenizer.padding_side = "right"

    # LoRA Config
    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.1,
        r=64,
        bias="none",
        task_type="CAUSAL_LM",
    )

    # Training Arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3, # Small dataset, so few epochs or more? 3 is standard start
        per_device_train_batch_size=4,
        gradient_accumulation_steps=1,
        optim="paged_adamw_32bit",
        save_steps=25,
        logging_steps=5,
        learning_rate=2e-4,
        weight_decay=0.001,
        fp16=False,
        bf16=False,
        max_grad_norm=0.3,
        max_steps=-1, # Train all epochs
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
    # Format: <s>[INST] {instruction} [/INST] {response} </s>
    return [f"<s>[INST] {row['instruction']} [/INST] {row['response']} </s>" for row in sample]

if __name__ == "__main__":
    # Check if dataset exists
    if not os.path.exists(DATASET_FILE):
        print(f"Error: {DATASET_FILE} not found.")
    else:
        train()
