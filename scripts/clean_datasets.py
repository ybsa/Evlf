import os
import json
import re
import random

# Configuration
DATASET_DIR = r"c:\Users\wind xebec\Evlf\datasets"
EMOJI_KEEP_PROB = 0.4  # Only keep emojis 40% of the time (60% reduction)
UNICODE_EMOJI_REGEX = re.compile(r'[^\w\s,!.?\'"-]') # Rough regex for non-text characters (mostly emojis)

def clean_text(text):
    """Normalize text for duplicate checking (lowercase, strip punct)."""
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

def strip_emojis(text):
    """Remove emojis from text."""
    return UNICODE_EMOJI_REGEX.sub('', text).strip()

def process_file(file_path):
    print(f"Processing: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    unique_instructions = set()
    cleaned_lines = []
    
    original_count = len(lines)
    
    for line in lines:
        if not line.strip(): continue
        
        try:
            data = json.loads(line)
            instruction = data.get("instruction", "")
            response = data.get("response", "")
            
            # 1. Deduplication
            norm_instr = clean_text(instruction)
            if norm_instr in unique_instructions:
                continue # Skip duplicate
            unique_instructions.add(norm_instr)
            
            # 2. Emoji Reduction (for Response only)
            if random.random() > EMOJI_KEEP_PROB:
                # Remove emojis to teach normal speech
                response = strip_emojis(response)
                # If stripping emojis made it empty or just whitespace, keep original or skip
                if not response.strip():
                    response = data.get("response", "") # Revert if empty
            
            # Reconstruct
            new_entry = {"instruction": instruction, "response": response}
            cleaned_lines.append(json.dumps(new_entry))
            
        except json.JSONDecodeError:
            continue
            
    final_count = len(cleaned_lines)
    removed = original_count - final_count
    print(f"  - Original: {original_count}, Final: {final_count}, Removed: {removed}")
    
    # Overwrite valid file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(cleaned_lines))

def main():
    print("🧹 Starting Dataset Cleanup...")
    print(f"Emoji Retention Rate: {EMOJI_KEEP_PROB * 100}%")
    
    for root, dirs, files in os.walk(DATASET_DIR):
        for file in files:
            if file.endswith(".jsonl"):
                full_path = os.path.join(root, file)
                process_file(full_path)
                
    print("\n✨ Cleanup Complete!")

if __name__ == "__main__":
    main()
