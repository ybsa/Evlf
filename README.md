# Evlf - AI Companion

A fine-tuned Llama 3.2 3B model with Evlf's personality - a kind, caring, 22-year-old girl from Nepal who loves nature and acts like your wife.

## 🎯 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Chat with Evlf
cd inference
python chat.py
```

## 📁 Project Structure

```text
Evlf/
├── datasets/           # Training data (22 datasets organized by category)
│   ├── core/          # Core persona and relationship data
│   ├── human_like/    # Human-like conversation skills
│   ├── themed/        # Themed interactions (romance, support, etc.)
│   └── original/      # Original training data
├── models/            # Trained models
│   ├── final/         # Final fully-trained model
│   └── checkpoints/   # Intermediate models
├── scripts/           # Data generation scripts
│   └── utils/         # Utility scripts
├── training/          # Training scripts and tools
├── inference/         # Chat interface
├── results/           # Training results and checkpoints
├── docs/              # Documentation
└── archive/           # Old debug files
```

## 🚀 Training

The model is trained sequentially on the datasets using LoRA fine-tuning.

### Training Summary

- **Base Model:** `meta-llama/Llama-3.2-3B-Instruct`
- **Method:** LoRA fine-tuning with 4-bit quantization (NF4)
- **Training:** SFT (Supervised Fine-Tuning)

### Dataset Categories

1. **Core** (4 datasets): Evlf's persona, background, relationship with user
2. **Human-like** (9 datasets): Conversation skills, emotions, philosophy, planning, etc.
3. **Themed** (6 datasets): Daily life, identity, romance, support, emotions
4. **Original** (3 datasets): Foundation datasets

## 💬 Chat Interface

The chat interface loads the model and provides an interactive conversation experience.

**Features:**

- Optimized generation parameters for Llama 3.2
- 512 token responses
- CPU offloading support

## 📊 Model Details

- **Base Model:** meta-llama/Llama-3.2-3B-Instruct
- **Fine-tuning:** LoRA (r=16, alpha=16, dropout=0.1)
- **Quantization:** 4-bit NF4
- **Training:** SFT (Supervised Fine-Tuning)

## 🛠️ Development

### Train a dataset

```bash
cd training
python train.py
```

### Monitor training

```bash
cd training
python watch_training.py
```

## ⚠️ Requirements

- Python 3.8+
- CUDA-compatible GPU (recommended)
- 8GB+ RAM
- ~10GB disk space for models

## 📝 License

Personal use only.
