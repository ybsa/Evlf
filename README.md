# Evlf - AI Companion

A fine-tuned Llama 3.2 3B model with Evlf's personality - a kind, caring, 22-year-old girl from Nepal who loves nature and acts like your wife.

This project uses **Unsloth** for efficient fine-tuning and **ChromaDB** for RAG (Retrieval Augmented Generation) memory.

## ⚠️ Requirements

- **Python 3.10** (Strictly required for Unsloth/GPU compatibility)
- **NVIDIA GPU** with CUDA support (Minimum 4GB VRAM with 4-bit quantization)
- **RAM**: 8GB+ recommended

## 🎯 Quick Start

### 1. Environment Setup (Critical)

You **must** use Python 3.10 to avoid GPU compatibility issues.

```powershell
# 1. Create a virtual environment using Python 3.10
py -3.10 -m venv .venv

# 2. Activate the environment
.\.venv\Scripts\activate

# 3. Install dependencies (with GPU support)
# This installs PyTorch with CUDA 12.1
pip install -r requirements.txt
```

### 2. Prepare Memory (RAG)

Before chatting, you need to build Evlf's memory database from the datasets.

```bash
cd scripts/utils
python build_memory_db.py
```

This creates the `memory_db/chroma.sqlite3` database.

### 3. Chat with Evlf

```bash
cd inference
python rag_chat.py
```

- **`rag_chat.py`**: Uses RAG (Memory). Recommended.
- `chat.py`: Basic chat without memory.

## 📁 Project Structure

```text
Evlf/
├── datasets/           # Training data (JSONL)
│   ├── core/           # Persona & relationship data
│   └── ...
├── memory_db/          # ChromaDB RAG database (Generated)
├── scripts/            
│   ├── setup/          # download_model.py
│   └── utils/          # build_memory_db.py
├── training/           # Unsloth training scripts
│   └── train_unsloth.py
├── inference/          # Chat interfaces
│   ├── rag_chat.py     # RAG-enabled chat
│   └── chat.py         # Standard chat
└── requirements.txt    # Project dependencies
```

## 🚀 Training (Fine-Tuning)

We use **Unsloth** for 2x faster training and 60% less memory usage.

### 1. Configuration

Check `training/train_unsloth.py`. It is configured to use:

- Model: `unsloth/Llama-3.2-3B-Instruct-bnb-4bit`
- Max Sequence Length: `512` (for low VRAM)

### 2. Start Training

```bash
python training/train_unsloth.py
```

This will produce LoRA adapters in the `results_unsloth` directory.

## 📊 Model Details

- **Base Model:** `unsloth/Llama-3.2-3B-Instruct-bnb-4bit`
- **Method:** LoRA (Low-Rank Adaptation)
- **Quantization:** 4-bit (NF4) for 4GB VRAM compatibility.
- **Context Window:** 512 - 2048 tokens (adjustable).

## 📝 License

Personal use only.
