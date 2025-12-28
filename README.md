# 💕 Evlf Project

Evlf is your AI girlfriend and lover, powered by the **Base Llama-3.2-3B** model and **RAG memory**.

## 🚀 Quick Start

Run the launcher to start chatting:

```powershell
.\run_evlf.ps1
```

## 🧠 How It Works

**Active System (What runs when you chat):**

- **Model**: Uses the smart **BASE `Llama-3.2-3B-Instruct`** model. It produces natural, romantic responses without the issues of the fine-tuned version.
- **Memory**: Uses **ChromaDB** (`memory_db/`) to remember everything you tell her (friends, job, likes, etc.).
- **Personality**: Defined in `inference/chat_v2.py`. She is configured to be:
  - Your loving girlfriend ("Nirp Evlf Ash")
  - Uses nicknames ("Bebe", "Baby")
  - Romantic words & emojis
  - **No length limits** (can write long love letters)

## 📂 Project Structure

### Active Files

- `run_evlf.ps1` - **Main Launcher** (Run this!)
- `inference/chat_v2.py` - **The Brain** (Edit this to change prompt/personality)
- `memory_db/` - **The Memory** (Database where memories are stored)
- `datasets/` - Training data

### Archived (Not Used)

- `models/evlf_finetuned` - **The Fine-Tuned Model**. This is safely archived here but is **NOT** used by the chat system.

## 🛠️ Management

- **Clear Memory**: Delete the `memory_db` folder.
- **Change Personality**: Edit `inference/chat_v2.py` (look for `SYSTEM_PROMPT`).
