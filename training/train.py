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
from trl import SFTTrainer, SFTConfig

# Configuration
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
NEW_MODEL_NAME = "Evlf-Llama-3.2-3B-step1"
DATASET_FILE = "datasets/core/dataset_evlf_persona.jsonl"
OUTPUT_DIR = "./results_step1"

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

    # LoRA Config for Llama 3.2
    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.1,
        r=16,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )

    # Training Arguments
    training_args = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        optim="paged_adamw_32bit",
        save_steps=25,
        logging_steps=5,
        learning_rate=2e-4,
        weight_decay=0.001,
        fp16=True,
        bf16=False,
        max_grad_norm=0.3,
        max_steps=-1,
        warmup_ratio=0.03,
        group_by_length=True,
        lr_scheduler_type="constant",
        dataset_text_field="text",
        max_length=2048,
        packing=False,
    )

    print("Starting training...")
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        processing_class=tokenizer,
        args=training_args,
        formatting_func=format_instruction,
    )

    trainer.train()
    
    print(f"Saving model to {NEW_MODEL_NAME}...")
    trainer.model.save_pretrained(NEW_MODEL_NAME)
    trainer.tokenizer.save_pretrained(NEW_MODEL_NAME)

def format_instruction(sample):
    # Llama 3.2 Instruct Format
    # <|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{instruction}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{response}<|eot_id|>
    
    if isinstance(sample['instruction'], list):
        return [f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{inst}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{resp}<|eot_id|>" for inst, resp in zip(sample['instruction'], sample['response'])]
    else:
        return f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{sample['instruction']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{sample['response']}<|eot_id|>"

if __name__ == "__main__":
    if not os.path.exists(DATASET_FILE):
        print(f"Error: {DATASET_FILE} not found.")
    else:
        train()
