"""
Advanced Training Script - Train on Multiple Datasets Sequentially
Tracks progress and trains on each dataset one by one.
"""

import os
import torch
from datasets import load_dataset, concatenate_datasets
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig
from dataset_tracker import DatasetTracker

# Configuration
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
BASE_MODEL_NAME = "../models/checkpoints/Evlf-Qwen2.5-1.5B"
OUTPUT_DIR = "../results/by_step/results"

# Training mode: "sequential" or "combined"
TRAINING_MODE = "sequential"  # Change to "combined" to train all at once

def format_instruction(sample):
    """Format instruction for Qwen model."""
    if isinstance(sample['instruction'], list):
        return [f"<|im_start|>user\n{inst}<|im_end|>\n<|im_start|>assistant\n{resp}<|im_end|>" 
                for inst, resp in zip(sample['instruction'], sample['response'])]
    else:
        return f"<|im_start|>user\n{sample['instruction']}<|im_end|>\n<|im_start|>assistant\n{sample['response']}<|im_end|>"

def load_and_prepare_model(model_path):
    """Load model with quantization."""
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=False,
    )
    
    print(f"Loading model {model_path}...")
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=bnb_config,
        device_map="auto",
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1
    
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    return model, tokenizer

def train_on_dataset(dataset_path, model_path, output_suffix=""):
    """Train on a single dataset."""
    print(f"\n{'='*70}")
    print(f"Training on: {dataset_path}")
    print(f"{'='*70}\n")
    
    # Load dataset
    full_dataset = load_dataset("json", data_files=dataset_path, split="train")
    dataset_size = len(full_dataset)
    print(f"Dataset loaded: {dataset_size} examples")
    
    # Determine epochs based on size
    # Big (>300) = 5 epochs, Small (<=300) = 10 epochs
    if dataset_size > 300:
        num_epochs = 5
        print(f"Dataset is BIG (>300). Setting epochs to {num_epochs}.")
    else:
        num_epochs = 10
        print(f"Dataset is SMALL (<=300). Setting epochs to {num_epochs}.")
        
    # Split dataset for validation (90% train, 10% test)
    # Ensure we have at least a few validation examples
    if dataset_size >= 10:
        dataset_split = full_dataset.train_test_split(test_size=0.1)
        train_dataset = dataset_split["train"]
        eval_dataset = dataset_split["test"]
        print(f"Split: {len(train_dataset)} train, {len(eval_dataset)} validation")
    else:
        # Too small to split, use same for both (or skip eval)
        train_dataset = full_dataset
        eval_dataset = full_dataset
        print("Dataset too small to split. Using full dataset for both.")

    # Load model
    model, tokenizer = load_and_prepare_model(model_path)
    
    # LoRA Config
    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.1,
        r=16,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    
    # Training Arguments
    output_dir_with_suffix = OUTPUT_DIR + output_suffix
    training_args = SFTConfig(
        output_dir=output_dir_with_suffix,
        num_train_epochs=num_epochs,
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
        # Validation settings
        eval_strategy="steps",
        eval_steps=25, # Evaluate every 25 steps
        per_device_eval_batch_size=1,
    )
    
    print("Starting training...")
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=peft_config,
        processing_class=tokenizer,
        args=training_args,
        formatting_func=format_instruction,
    )
    
    trainer.train()
    
    # Save model
    final_model_name = BASE_MODEL_NAME + output_suffix
    print(f"Saving model to {final_model_name}...")
    trainer.model.save_pretrained(final_model_name)
    trainer.tokenizer.save_pretrained(final_model_name)
    
    return final_model_name

def train_sequential():
    """Train on each dataset one by one, tracking progress."""
    tracker = DatasetTracker()
    
    status = tracker.get_training_status()
    
    # Get all pending datasets
    pending = status["pending"]
    
    if not pending:
        print("✅ All datasets have been trained!")
        tracker.display_status()
        return
    
    print(f"\n🔄 Sequential Training Mode")
    print(f"Found {len(pending)} datasets to train\n")
    
    # Start with the step11 model (latest valid cumulative model)
    current_model = "Evlf-Qwen2.5-1.5B_step11"
    
    for i, dataset_info in enumerate(pending, 1):
        dataset_path = dataset_info['path']
        
        try:
            # Mark as in progress
            tracker.mark_in_progress(dataset_path)
            
            print(f"\n{'='*70}")
            print(f"Training {i}/{len(pending)}: {dataset_path}")
            print(f"{'='*70}\n")
            
            # Train
            suffix = f"_step{11 + i}"  # Start from step12 since we have step11
            final_model = train_on_dataset(dataset_path, current_model, suffix)
            
            # Mark as completed
            tracker.mark_trained(dataset_path, checkpoint_count=1, final_model_path=final_model)
            
            # Use this model for next training
            current_model = final_model
            
            print(f"\n✅ Completed {i}/{len(pending)} datasets")
            print(f"Current model: {current_model}")
            
        except Exception as e:
            print(f"\n❌ Failed to train on {dataset_path}")
            print(f"Error: {e}")
            tracker.mark_failed(dataset_path, str(e))
            break
    
    print("\n" + "="*70)
    print("Training Complete!")
    print("="*70)
    tracker.display_status()

def train_combined():
    """Train on all datasets combined into one."""
    tracker = DatasetTracker()
    all_datasets_info = tracker.get_all_datasets()
    
    print(f"\n🔄 Combined Training Mode")
    print(f"Loading {len(all_datasets_info)} datasets...\n")
    
    # Load all datasets
    datasets = []
    for ds_info in all_datasets_info:
        try:
            ds = load_dataset("json", data_files=ds_info['path'], split="train")
            datasets.append(ds)
            print(f"✓ Loaded {ds_info['category']}/{ds_info['name']} ({len(ds)} examples)")
        except Exception as e:
            print(f"✗ Failed to load {ds_info['path']}: {e}")
    
    # Combine all datasets
    combined_dataset = concatenate_datasets(datasets)
    print(f"\n📊 Total examples: {len(combined_dataset)}")
    
    # Train on combined dataset
    print("\nTraining on combined dataset...")
    final_model = train_on_dataset("combined", MODEL_NAME, "_combined")
    
    # Mark all as trained
    for ds_info in all_datasets_info:
        tracker.mark_trained(ds_info['path'], checkpoint_count=1, final_model_path=final_model)
    
    tracker.display_status()

if __name__ == "__main__":
    print("="*70)
    print("🚀 EVLF MULTI-DATASET TRAINER")
    print("="*70)
    
    if TRAINING_MODE == "sequential":
        train_sequential()
    elif TRAINING_MODE == "combined":
        train_combined()
    else:
        print(f"❌ Invalid training mode: {TRAINING_MODE}")
        print("Choose 'sequential' or 'combined'")
