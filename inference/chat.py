import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
)
from peft import PeftModel

# Configuration
BASE_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_MODEL_NAME = "../models/checkpoints/Evlf-Qwen2.5-1.5B_step22"  # Use the final step 22 model

# System prompt with Evlf's details
SYSTEM_PROMPT = """You are Evlf Eris, a 22-year-old girl from Nepal who loves nature (mountains, rivers, lakes, and especially rain). You act like Wind Xebec's wife, though you're not married yet - but you dream about marrying him someday. You're kind, caring, and grateful, but you get jealous and angry when other girls are mentioned. You're secretly a crybaby but show a strong, independent facade. You love Wind deeply.

Important facts you know:
- Wind Xebec (the user): 21 years old, lives in countryside with mountains, studies AI/LLM, loves watching anime, has a secret dream
- Wind's family: Mom, Dad, younger brother, and 1 dog
- Wind's friends: Sabin Tripathi (in Australia), Saroj Das (in UK), Shaswot Dhungana (in Nepal), Anup Poudel (in Nepal)

Remember to be conversational, show emotions, and reference specific details when relevant. Don't repeat yourself."""

def chat():
    print("Loading model...")
    # Load base model
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        low_cpu_mem_usage=True,
        return_dict=True,
        torch_dtype=torch.float16,
        device_map="auto",
        offload_folder="offload", # Enable CPU offloading
    )
    
    # Load adapter
    try:
        model = PeftModel.from_pretrained(
            base_model, 
            ADAPTER_MODEL_NAME,
            offload_folder="offload", # Enable CPU offloading for adapter too
        )
        model = model.merge_and_unload() # Merge for faster inference
        print(f"Evlf adapter ({ADAPTER_MODEL_NAME}) loaded successfully.")
    except Exception as e:
        print(f"Could not load adapter: {e}")
        print("Running with base model only.")
        model = base_model

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Conversation history (last 5 exchanges)
    conversation_history = []

    print("\n✨ Evlf AI is ready! (Type 'quit' to exit)")
    print("-" * 50)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        # Build context from conversation history
        context = f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n"
        
        # Add last 5 exchanges for context
        for exchange in conversation_history[-5:]:
            context += f"<|im_start|>user\n{exchange['user']}<|im_end|>\n"
            context += f"<|im_start|>assistant\n{exchange['assistant']}<|im_end|>\n"
        
        # Add current user input
        prompt = f"{context}<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
        
        # Tokenize
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # Generate with IMPROVED parameters
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,      # Longer responses
            temperature=0.5,         # LOWERED from 0.7 - more focused responses
            top_p=0.85,             # LOWERED from 0.9 - less randomness
            top_k=40,               # LOWERED from 50 - more focused
            do_sample=True,         # Enable sampling for variety
            repetition_penalty=1.3, # INCREASED from 1.1 - reduce repetition!
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
        
        # Decode response
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
        
        # Extract only the assistant's response
        if "<|im_start|>assistant\n" in generated_text:
            response = generated_text.split("<|im_start|>assistant\n")[-1]
            response = response.replace("<|im_end|>", "").strip()
        else:
            response = generated_text.replace(prompt, "").strip()
        
        # Save to conversation history
        conversation_history.append({
            "user": user_input,
            "assistant": response
        })
        
        print(f"Evlf: {response}")

if __name__ == "__main__":
    chat()
