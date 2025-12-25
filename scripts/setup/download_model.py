from huggingface_hub import snapshot_download
import os

# Using the 4-bit quantized version for Unsloth
MODEL_NAME = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit"

print(f"🚀 Starting download for: {MODEL_NAME}")
print("This will download the 4-bit quantized model (smaller and faster). Please wait...")

try:
    path = snapshot_download(
        repo_id=MODEL_NAME,
        resume_download=True,
        local_files_only=False
    )
    print(f"\n✅ Download COMPLETE! Model stored at:\n{path}")
except Exception as e:
    print(f"\n❌ Download Failed: {e}")
