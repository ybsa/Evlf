import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
)
from peft import PeftModel

# Configuration
BASE_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_MODEL_NAME = "Evlf-Qwen2.5-1.5B"

def chat():
    print("Loading model...")
    # Load base model
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        low_cpu_mem_usage=True,
        return_dict=True,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    
    # Load adapter
    try:
        model = PeftModel.from_pretrained(base_model, ADAPTER_MODEL_NAME)
        model = model.merge_and_unload() # Merge for faster inference
        print("Evlf adapter loaded successfully.")
    except Exception as e:
        print(f"Could not load adapter: {e}")
        print("Running with base model only.")
        model = base_model

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    pipe = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=200,
    )

    print("\nEvlf AI is ready! (Type 'quit' to exit)")
    print("-" * 50)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        # Format prompt for Qwen
        prompt = f"<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
        
        result = pipe(prompt)
        generated_text = result[0]['generated_text']
        
        # Extract response
        response = generated_text.replace(prompt, "").strip()
        
        print(f"Evlf: {response}")

if __name__ == "__main__":
    chat()
