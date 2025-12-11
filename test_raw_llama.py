"""
Test the raw Llama-3.1-8B model (before fine-tuning)
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# Configuration
MODEL_NAME = "NousResearch/Meta-Llama-3.1-8B-Instruct"

print("Loading raw Llama-3.1-8B model...")

# 4-bit quantization for 4GB GPU
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    offload_folder="offload",
    torch_dtype=torch.float16,
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

print("\n✨ Raw Llama-3.1-8B is ready! (Type 'quit' to exit)")
print("-" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["quit", "exit"]:
        break

    # Llama 3 chat format
    prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
    
    # Extract response
    if "<|start_header_id|>assistant<|end_header_id|>\n\n" in generated_text:
        response = generated_text.split("<|start_header_id|>assistant<|end_header_id|>\n\n")[-1]
        response = response.replace("<|eot_id|>", "").strip()
    else:
        response = generated_text.replace(prompt, "").strip()
    
    print(f"\nLlama: {response}")

print("\n👋 Goodbye!")
