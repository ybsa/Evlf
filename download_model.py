from huggingface_hub import snapshot_download
import os

MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"

print(f"🚀 Starting download for: {MODEL_NAME}")
print("This will download ~6GB. Please wait...")

try:
    path = snapshot_download(
        repo_id=MODEL_NAME,
        resume_download=True,
        local_files_only=False
    )
    print(f"\n✅ Download COMPLETE! Model stored at:\n{path}")
except Exception as e:
    print(f"\n❌ Download Failed: {e}")
