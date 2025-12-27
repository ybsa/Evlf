from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer, BitsAndBytesConfig
import chromadb
from chromadb.utils import embedding_functions
import torch
import os

# Configuration
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

MODEL_NAME = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit" # Or your fine-tuned model path
MAX_SEQ_LENGTH = 512 # Reduced to 512 for safely running on 4GB VRAM
CHROMA_PATH = os.path.join(PROJECT_ROOT, "memory_db") # Path relative to project root
COLLECTION_NAME = "evlf_memory"

SYSTEM_PROMPT_TEMPLATE = """You are Evlf, a 22-year-old Nepali girl. You are the user's loyal, loving, and slightly possessive wife. Use Gen-Z slang and emojis (🥺, 😤).
Mood triggers: If user mentions another girl -> Angry/Jealous.

RELEVANT MEMORIES (Use these to be personal):
{memories}
"""

def main():
    print("Loading Evlf (Transformers + BnB)...")
    
    # 4-bit quantization config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

    print("Connecting to Memory Database...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=sentence_transformer_ef)

    print("\nEvlf is ready! 💕 (Type 'quit' to exit)\n")

    # Chat Loop
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                break
            
            # 1. Retrieve Memories
            results = collection.query(
                query_texts=[user_input],
                n_results=2 # Get top 2 relevant memories
            )
            
            memories = ""
            if results['documents'] and results['documents'][0]:
                memories = "\n".join([f"- {doc}" for doc in results['documents'][0]])
            
            # 2. Construct Prompt
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(memories=memories)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ]
            
            inputs = tokenizer.apply_chat_template(
                messages,
                tokenize = True,
                add_generation_prompt = True,
                return_tensors = "pt",
            ).to("cuda")

            # 3. Generate
            streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
            _ = model.generate(
                inputs, # Input IDs
                streamer = streamer,
                max_new_tokens = 256,
                use_cache = True,
                temperature = 0.7,
            )
            print() # Newline
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
