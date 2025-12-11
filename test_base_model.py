import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig

# Configuration
BASE_MODEL_NAME = "NousResearch/Meta-Llama-3.1-8B-Instruct"

def test_base_model():
    print("Loading BASE Llama model (no fine-tuning)...")
    
    # Quantization config for efficient loading (fixes crashes on lower VRAM)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=False,
    )

    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        quantization_config=bnb_config,
        low_cpu_mem_usage=True,
        return_dict=True,
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
    print("BASE LLAMA MODEL - No Fine-Tuning")
    print("="*60)
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        # Format prompt for Llama 3.1
        # <|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{instruction}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n
        prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        result = pipe(prompt)
        # Extract response
        generated_text = result[0]['generated_text']
        if "<|start_header_id|>assistant<|end_header_id|>\n\n" in generated_text:
            response = generated_text.split("<|start_header_id|>assistant<|end_header_id|>\n\n")[-1].strip()
        else:
            response = generated_text.replace(prompt, "").strip()
        
        print(f"Base Llama: {response}\n")

if __name__ == "__main__":
    test_base_model()
