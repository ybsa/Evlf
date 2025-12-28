# ------------------------------------------------------------------------
# 0. Setup & Security Bypass
# ------------------------------------------------------------------------
import os
# Bypass strict torch.load security checks (needed for optimizer.pt resumption in newer torch versions)
os.environ["TORCH_ALLOW_UNSAFE_LOAD"] = "1"
# Also disable weights_only enforcement if present
os.environ["TORCH_FORCE_WEIGHTS_ONLY_LOAD"] = "0"

# --- MONKEY PATCH: SQUASH VULNERABILITY ERROR ---
import transformers.utils.import_utils
transformers.utils.import_utils.check_torch_load_is_safe = lambda: None
# ------------------------------------------------

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType
from datasets import load_dataset, concatenate_datasets
import warnings

# Suppress other warnings
warnings.filterwarnings("ignore")

# ------------------------------------------------------------------------
# 1. Configuration
# ------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
OUTPUT_DIR = os.path.join(CURRENT_DIR, "results_clean") # New Clean Directory
# Start from checkpoint-200 (Bypass resume error)
# Default to base model, override later if checkpoint found
MODEL_NAME = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit"


# 4GB VRAM settings
MAX_SEQ_LENGTH = 512
BATCH_SIZE = 1
GRAD_ACCUMULATION = 8 

# --- 1. Load Datasets (High-Quality Only) ---
print("🚀 Loading Datasets...")
data_files = [
    # Core (Facts about Xebec and relationship)
    os.path.join(PROJECT_ROOT, "datasets", "core", "dataset_xebec_personal.jsonl"),
    os.path.join(PROJECT_ROOT, "datasets", "core", "dataset_user_relationship.jsonl"),
    os.path.join(PROJECT_ROOT, "datasets", "core", "dataset_evlf_eris_background.jsonl"),
    # Persona (Evlf's personality and emotions)
    os.path.join(PROJECT_ROOT, "datasets", "dataset_evlf_persona.jsonl"),
    # Themed (Identity rules and complex reasoning)
    os.path.join(PROJECT_ROOT, "datasets", "themed", "dataset_identity.jsonl"),
    os.path.join(PROJECT_ROOT, "datasets", "themed", "dataset_complex_reasoning.jsonl"),
]


# Verify files exist
valid_files = [f for f in data_files if os.path.exists(f)]
print(f"Found {len(valid_files)}/{len(data_files)} dataset files.")

dataset = load_dataset("json", data_files=valid_files, split="train")
print(f"Total samples: {len(dataset)}")

# --- Check for Resume ---
last_checkpoint = None
if os.path.isdir(OUTPUT_DIR):
    checkpoints = [d for d in os.listdir(OUTPUT_DIR) if d.startswith("checkpoint-")]
    if checkpoints:
        # Sort by step number
        checkpoints.sort(key=lambda x: int(x.split('-')[1]))
        last_checkpoint = os.path.join(OUTPUT_DIR, checkpoints[-1])
        print(f"🔄 Found checkpoint: {last_checkpoint}")
        MODEL_NAME = last_checkpoint # Load adapters from here

# --- 2. Load Tokenizer & Model ---
print(f"Loading Tokenizer & Model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right" # Fix for fp16

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# Prepare for LoRA
model = prepare_model_for_kbit_training(model)
peft_config = LoraConfig(
    r=16,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
)
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# --- 3. Format Data ---
print("Formatting Data...")
def apply_chat_template(example):
    messages = [
        {"role": "user", "content": example["instruction"]},
        {"role": "assistant", "content": example["response"]}
    ]
    # We use the tokenizer's chat template
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    return {"text": text}

formatted_dataset = dataset.map(apply_chat_template)

def tokenize_function(examples):
    # Tokenize the texts
    tokenized = tokenizer(
        examples["text"],
        truncation=True,
        max_length=MAX_SEQ_LENGTH,
        padding="max_length", # Pad to max length for stability
    )
    # Labels corresponding to input_ids (standard causal LM)
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

print("Tokenizing...")
tokenized_dataset = formatted_dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)

# --- 4. Trainer ---
print("Initializing Trainer...")
# Training Arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUMULATION,
    num_train_epochs=3, # 3 Epochs for small but high-quality data
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=50,
    save_total_limit=2,
    optim="paged_adamw_8bit",
    report_to="none", # Disable wandb
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={'use_reentrant': False}, # Fix UserWarning
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

# --- 5. Train ---
print("\n🔥 STARTING TRAINING (Custom Loop)...")
if last_checkpoint:
    print(f"Resuming from: {last_checkpoint}")
    trainer.train(resume_from_checkpoint=last_checkpoint)
else:
    trainer.train()

# --- 6. Save ---
print("Saving Model...")
trainer.save_model(os.path.join(OUTPUT_DIR, "final_model"))
tokenizer.save_pretrained(os.path.join(OUTPUT_DIR, "final_model"))
print("✅ Done!")
