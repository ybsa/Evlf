import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import sys

# Add project root to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.append(PROJECT_ROOT)

def validate_checkpoint():
    print("🔍 Scanning for checkpoints...")
    
    # Check both potential output directories
    search_dirs = [
        os.path.join(PROJECT_ROOT, "training", "results_custom"),
        os.path.join(PROJECT_ROOT, "training", "results_transformers")
    ]
    
    all_checkpoints = []
    
    for results_dir in search_dirs:
        if os.path.exists(results_dir):
            checkpoints = [
                (d, os.path.join(results_dir, d)) 
                for d in os.listdir(results_dir) 
                if d.startswith("checkpoint-")
            ]
            all_checkpoints.extend(checkpoints)
    
    if not all_checkpoints:
        print("❌ No checkpoints found in any results directory!")
        return

    # Sort by number (checkpoint-50, checkpoint-100...)
    # x[0] is the folder name like "checkpoint-350"
    sorted_checkpoints = sorted(all_checkpoints, key=lambda x: int(x[0].split("-")[1]))
    
    print(f"\nFound {len(sorted_checkpoints)} checkpoints:")
    for name, path in sorted_checkpoints:
        print(f" - {name} ({os.path.basename(os.path.dirname(path))})")

    # Pick the latest
    latest_name, latest_path = sorted_checkpoints[-1]
    
    print(f"\n� Validating Latest Checkpoint: {latest_name}")
    print(f"📂 Path: {latest_path}\n")

    # Load Model
    print("Loading model... (This takes ~30s)")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    model = AutoModelForCausalLM.from_pretrained(
        latest_path,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(latest_path)

    # Test Prompts
    test_prompts = [
        "Hey Evlf, how are you feeling?",
        "What do you think about me?",
        "I had a bad day at work."
    ]

    print("\n✨ Generating Responses:\n" + "="*50)

    for prompt in test_prompts:
        messages = [
            {"role": "user", "content": prompt}
        ]
        inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True).to("cuda")
        
        outputs = model.generate(
            inputs, 
            max_new_tokens=100, 
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response = tokenizer.decode(outputs[0][inputs.shape[-1]:], skip_special_tokens=True)
        print(f"\nUser: {prompt}")
        print(f"Evlf: {response}")
    
    print("\n" + "="*50)
    print("✅ Validation Complete!")

if __name__ == "__main__":
    validate_checkpoint()
