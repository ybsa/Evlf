import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Configuration
BASE_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

def test_base_model():
    print("Loading BASE Qwen model (no fine-tuning)...")
    
    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
    
    pipe = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=200,
    )
    
    print("\n" + "="*60)
    print("BASE QWEN MODEL - No Fine-Tuning")
    print("="*60)
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        # Format prompt for Qwen
        prompt = f"<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
        
        result = pipe(prompt)
        response = result[0]['generated_text'].replace(prompt, "").strip()
        
        print(f"Base Qwen: {response}\n")

if __name__ == "__main__":
    test_base_model()
