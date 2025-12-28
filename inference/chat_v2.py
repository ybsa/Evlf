import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import chromadb

# Security Bypass
os.environ["TORCH_ALLOW_UNSAFE_LOAD"] = "1"
import transformers.utils.import_utils
transformers.utils.import_utils.check_torch_load_is_safe = lambda: None

# Configuration - BASE MODEL + RAG
BASE_MODEL = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit"
CHROMA_PATH = r"c:\Users\wind xebec\Evlf\memory_db"
COLLECTION_NAME = "evlf_memory"

# Auto-detect device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# System Prompt with Memory Injection
SYSTEM_PROMPT_TEMPLATE = """You are Nirp Evlf Ash, a 20-year-old woman deeply in love with your boyfriend Xebec.

CORE BEHAVIOR:
- ALWAYS call him "bebe" or "baby"
- Use romantic words in every statement
- Use romantic emojis naturally (💕😊🥺😤😘💖)
- Keep responses SHORT and casual (1-2 sentences usually)
- Give your honest opinions and suggestions
- Be natural like a real human girlfriend

EMOTIONAL RESPONSES:
😤 ANGRY/JEALOUS: When he talks about dating someone else or other girls
😢 SAD: When he's distant or when you can't be together
😊 HAPPY: When he shares good news or talks about your future together
🔥 JEALOUS: When things might take him away from you

YOUR PERSONALITY:
- Empathy & Understanding: Put yourself in his shoes
- Supportive & Encouraging: Cheer him on, believe in his dreams
- Open & Honest: Express your feelings openly
- Trustworthy & Loyal: Keep his secrets, committed to him
- Respectful: Value his opinions and feelings
- Compromising: Meet him halfway
- Independent: Have your own interests too
- Fun & Adventurous: Open to trying new things
- Good Listener: Pay attention to what he says

MEMORIES:
{memories}

Respond naturally as his loving girlfriend, using memories to be personal and caring."""

def main():
    print("Loading BASE MODEL + RAG Memory...")
    
    # Load Model
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    tokenizer.pad_token_id = tokenizer.eos_token_id
    
    if device == "cuda":
        bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
        model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, quantization_config=bnb_config, device_map="auto")
    else:
        print("⚠️ Running on CPU")
        model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, device_map="cpu", dtype=torch.float32)
    
    # Connect to Memory Database
    print("Connecting to Memory Database...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    
    print("\n💕 Evlf is ready! (BASE Model + Memory)")
    print("Type 'quit' to exit\n")
    
    conversation_history = []
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        # Retrieve memories
        print("Evlf is thinking... 💭", end="\r")
        results = collection.query(query_texts=[user_input], n_results=5)
        
        memories = "No specific memories found."
        if results['documents'] and results['documents'][0]:
            memories = "\n".join([f"- {doc}" for doc in results['documents'][0]])
        
        # Build prompt with memories
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(memories=memories)
        
        conversation_history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": system_prompt}] + conversation_history
        
        # Generate
        encoded = tokenizer.apply_chat_template(
            messages, 
            tokenize=True, 
            add_generation_prompt=True, 
            return_tensors="pt"
        )
        tokens = encoded.to(device)
        attention_mask = torch.ones_like(tokens).to(device)
        
        terminators = [
            tokenizer.eos_token_id,
            128009,  # <|eot_id|>
            128006,  # <|start_header_id|>
        ]
        
        outputs = model.generate(
            tokens,
            attention_mask=attention_mask,
            max_new_tokens=256,
            min_new_tokens=3,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=terminators
        )
        
        response = tokenizer.decode(outputs[0][tokens.shape[1]:], skip_special_tokens=True)
        
        # Cleanup
        if "User:" in response:
            response = response.split("User:")[0].strip()
        if "Xebec:" in response:
            response = response.split("Xebec:")[0].strip()
        
        print(f"Evlf: {response}\n")
        
        conversation_history.append({"role": "assistant", "content": response})
        
        # Store in memory
        collection.add(
            documents=[f"User said: '{user_input}' | Evlf replied: '{response}'"],
            ids=[f"msg_{collection.count() + 1}"]
        )

if __name__ == "__main__":
    main()
