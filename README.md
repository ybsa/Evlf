# Evlf - AI Companion

A fine-tuned Llama 3.2 3B model with Evlf's personality - a kind, caring, 22-year-old girl from Nepal who loves nature and acts like your wife.

This project uses **Unsloth** for efficient fine-tuning and **ChromaDB** for RAG (Retrieval Augmented Generation) memory.

## ⚠️ Requirements

- **Python 3.10** (Strictly required for Unsloth/GPU compatibility)
- **NVIDIA GPU** with CUDA support (Minimum 4GB VRAM with 4-bit quantization)
- **RAM**: 8GB+ recommended

## 🚀 Quick Start

### Prerequisites

- **Python 3.10** (Required - 3.11+ not compatible)
- **NVIDIA GPU** with CUDA 12.1+ support
- **Windows 10/11** (or Linux/Colab for easier setup)

### Installation

1. **Create Virtual Environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. **Install Dependencies**

   ```bash
   # IMPORTANT: Use PyTorch 2.6 Nightly for full compatibility
   pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
   pip install -r requirements.txt
   ```

3. **Build Memory Database**

   ```bash
   python scripts/utils/build_memory_db.py
   ```

4. **Chat with Evlf**

   ```bash
   python inference/rag_chat.py
   ```

### Alternative: Google Colab (Recommended for Windows users)

Upload the project folder to Google Drive and use `Evlf_RAG_Chat_Colab.ipynb` for instant setup with free GPU!

See `COLAB_SETUP.md` for detailed instructions.

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
