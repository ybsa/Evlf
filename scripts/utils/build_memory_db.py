import chromadb
from chromadb.utils import embedding_functions
import json
import os

# Configuration
CHROMA_PATH = "memory_db"
COLLECTION_NAME = "evlf_memory"
DATA_FILES = [
    "datasets/core/dataset_xebec_personal.jsonl",
    "datasets/core/dataset_user_relationship.jsonl"
]

def build_memory_db():
    print("Initializing ChromaDB for RAG Memory...")
    
    # Initialize Persistent Client
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # Use standard Sentence Transformers for embeddings
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Get or Create Collection
    # We delete existing one to rebuild fresh from datasets
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except ValueError:
        pass
        
    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=sentence_transformer_ef
    )
    
    # Load Data and Embed
    documents = []
    metadatas = []
    ids = []
    
    count = 0
    for filename in DATA_FILES:
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found, skipping...")
            continue
            
        print(f"Processing {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    # Extract User Instruction and Assistant Response for context
                    # ChatML format: messages list
                    user_msg = ""
                    assistant_msg = ""
                    
                    if "messages" in entry:
                        for msg in entry["messages"]:
                            if msg["role"] == "user":
                                user_msg = msg["content"]
                            elif msg["role"] == "assistant":
                                assistant_msg = msg["content"]
                    elif "instruction" in entry and "response" in entry:
                        user_msg = entry["instruction"]
                        assistant_msg = entry["response"]
                    
                    if user_msg and assistant_msg:
                        # We embed the "Fact" or "Memory" which is the combination
                        memory_text = f"User asked: {user_msg} | Evlf replied: {assistant_msg}"
                        
                        documents.append(memory_text)
                        metadatas.append({"source": filename, "type": "memory"})
                        ids.append(f"mem_{count}")
                        count += 1
                        
                except json.JSONDecodeError:
                    continue

    if documents:
        print(f"Adding {len(documents)} memories to ChromaDB...")
        # Add in batches if needed, but for small datasets this is fine
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Successfully built memory database with {count} entries!")
        print(f"Database saved to: {os.path.abspath(CHROMA_PATH)}")
    else:
        print("❌ No data found to build memory!")

if __name__ == "__main__":
    build_memory_db()
