from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
import os

# Configuration
MODEL_NAME = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit" # Pre-quantized for 4-bit
NEW_MODEL_NAME = "Evlf-Llama-3.2-3B-Unsloth"
DATASET_FILE = "datasets/core/dataset_evlf_persona.jsonl" # Will need to be the combined dataset eventually
OUTPUT_DIR = "./results_unsloth"
MAX_SEQ_LENGTH = 512 # Critical for 4GB VRAM

def train():
    print(f"Loading Unsloth model: {MODEL_NAME}...")
    
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = MODEL_NAME,
        max_seq_length = MAX_SEQ_LENGTH,
        dtype = None, # None = auto detection
        load_in_4bit = True,
    )

    # Add LoRA adapters
    print("Adding LoRA adapters...")
    model = FastLanguageModel.get_peft_model(
        model,
        r = 16,
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha = 16,
        lora_dropout = 0, # Should be 0 for Unsloth usually
        bias = "none",
        use_gradient_checkpointing = "unsloth", # 4x longer context window, lower VRAM
        random_state = 3407,
    )

    print(f"Loading dataset from {DATASET_FILE}...")
    # Trying to load multiple files if they exist, otherwise just the persona one for now
    data_files = []
    if os.path.exists("datasets/core/dataset_evlf_persona.jsonl"):
        data_files.append("datasets/core/dataset_evlf_persona.jsonl")
    
    # We will assume datasets are regenerated in ChatML format
    dataset = load_dataset("json", data_files=data_files, split="train")

    print("Starting training with optimized settings...")
    trainer = SFTTrainer(
        model = model,
        train_dataset = dataset,
        dataset_text_field = "text", # This might need adjustment based on ChatML, usually unsloth handles it or we preprocess
        max_seq_length = MAX_SEQ_LENGTH,
        tokenizer = tokenizer,
        args = TrainingArguments(
            per_device_train_batch_size = 1, # Critical for 4GB
            gradient_accumulation_steps = 4, # Effective batch size = 4
            warmup_steps = 10,
            max_steps = 100, # Quick run, increase for full training
            learning_rate = 2e-4,
            fp16 = not torch.cuda.is_bf16_supported(),
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 1,
            output_dir = OUTPUT_DIR,
            optim = "adamw_8bit", # Save optimizer VRAM
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
        ),
    )
    
    from unsloth.chat_templates import get_chat_template
    
    # Setup ChatML template
    tokenizer = get_chat_template(
        tokenizer,
        chat_template = "llama-3", # or "chatml"
        mapping = {"role" : "from", "content" : "value", "user" : "human", "assistant" : "gpt"}, # ShareGPT style mapping if needed, or standard
    )
    
    # We need a formatting function for ChatML input if dataset is raw JSONL (Standard HuggingFace format)
    # If dataset is {"messages": [...]}, SFTTrainer needs a slight adjustment or a formatting func.
    # Unsloth makes this easy usually. Let's assume standard 'messages' column from the new generation scripts.
    
    trainer_stats = trainer.train()
    
    print(f"Saving model to {NEW_MODEL_NAME}...")
    model.save_pretrained(NEW_MODEL_NAME)
    tokenizer.save_pretrained(NEW_MODEL_NAME)

if __name__ == "__main__":
    train()
