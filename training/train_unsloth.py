from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
import os

# Configuration
# Calculate project root (assuming script is in Evlf/training)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

MODEL_NAME = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit" # Pre-quantized for 4-bit
NEW_MODEL_NAME = "Evlf-Llama-3.2-3B-Unsloth"
DATASET_FILE = os.path.join(PROJECT_ROOT, "datasets", "core", "dataset_evlf_persona.jsonl")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "results_unsloth")
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
    if os.path.exists(DATASET_FILE):
        data_files.append(DATASET_FILE)
    
    # We will assume datasets are regenerated in ChatML format
    dataset = load_dataset("json", data_files=data_files, split="train")

    print("Starting training with optimized settings...")
    
    # 1. Setup ChatML/Llama-3 template
    from unsloth.chat_templates import get_chat_template
    tokenizer = get_chat_template(
        tokenizer,
        chat_template = "llama-3",
    )

    # 2. Define formatting function for instruction/response dataset
    def formatting_prompts_func(examples):
        instructions = examples["instruction"]
        responses    = examples["response"]
        texts = []
        for instruction, response in zip(instructions, responses):
            # Format using Llama-3 template
            # System prompt is optional, but we can add Evlf's persona here if we want consistent training
            # For now, we'll keep it simple: User -> Assistant
            conversation = [
                {"role": "user", "content": instruction},
                {"role": "assistant", "content": response},
            ]
            text = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=False)
            texts.append(text)
        return { "text" : texts, }

    trainer = SFTTrainer(
        model = model,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = MAX_SEQ_LENGTH,
        tokenizer = tokenizer,
        formatting_func = formatting_prompts_func, # Use our custom formatter
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
    

    
    trainer_stats = trainer.train()
    
    print(f"Saving model to {NEW_MODEL_NAME}...")
    model.save_pretrained(NEW_MODEL_NAME)
    tokenizer.save_pretrained(NEW_MODEL_NAME)

if __name__ == "__main__":
    train()
