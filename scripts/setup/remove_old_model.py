from huggingface_hub import scan_cache_dir
import shutil
import os

OLD_MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"

def remove_old_model():
    print(f"Scanning for old model: {OLD_MODEL_ID}...")
    
    try:
        hf_cache_info = scan_cache_dir()
        
        found = False
        for repo in hf_cache_info.repos:
            if repo.repo_id == OLD_MODEL_ID:
                print(f"Found {repo.repo_id} in cache using {repo.size_on_disk_str}")
                print(f"Path: {repo.repo_path}")
                
                # We can't use hf_cache_info.delete_revisions easily in script without CLI interaction simulation or internal methods,
                # but we can just remove the directory if we are sure.
                # A safer way via library is generally preferred if available, but manual deletion of the repo folder in cache works standardly.
                
                confirm = input(f"Are you sure you want to delete {repo.repo_path}? (y/n): ")
                if confirm.lower() == 'y':
                    print("Deleting...")
                    shutil.rmtree(repo.repo_path)
                    print("✅ Deleted from cache.")
                else:
                    print("Skipped deletion.")
                found = True
                break
        
        if not found:
            print(f"Model {OLD_MODEL_ID} not found in Hugging Face cache.")
            
    except Exception as e:
        print(f"Error scanning/deleting cache: {e}")

    # Also check local models folder
    local_path = "models"
    if os.path.exists(local_path):
        print(f"\nChecking local 'models' folder...")
        # We don't know exactly what's here, so just listing
        files = os.listdir(local_path)
        if not files:
            print("Local 'models' folder is empty.")
        else:
            print(f"Found files in 'models': {files}")
            print("Please manually delete valid files if they are the old model.")

if __name__ == "__main__":
    # Auto-confirm for this specific execution context since user asked for it
    # We will monkeypatch input to always return 'y' for this script run
    import builtins
    builtins.input = lambda _: 'y'
    
    remove_old_model()
