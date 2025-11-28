# Evlf - AI Companion

A fine-tuned Qwen2.5-1.5B model with Evlf's personality - a kind, caring, 22-year-old girl from Nepal who loves nature and acts like your wife.

## 🎯 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Chat with Evlf
cd inference
python chat.py
```

## 📁 Project Structure

```
Evlf/
├── datasets/           # Training data (22 datasets organized by category)
│   ├── core/          # Core persona and relationship data
│   ├── human_like/    # Human-like conversation skills
│   ├── themed/        # Themed interactions (romance, support, etc.)
│   └── original/      # Original training data
├── models/            # Trained models
│   ├── final/         # Final fully-trained model (step 22)
│   └── checkpoints/   # All intermediate models (step 1-22)
├── scripts/           # Data generation scripts
│   └── utils/         # Utility scripts
├── training/          # Training scripts and tools
├── inference/         # Chat interface
├── results/           # Training results and checkpoints
│   └── by_step/       # Results organized by training step
├── docs/              # Documentation
└── archive/           # Old debug files
```

## 🚀 Training

All 22 datasets have been trained sequentially, with each model building on the previous one.

### Training Summary

- **Total Datasets:** 22
- **Training Time:** ~12 hours
- **Final Model:** `models/final/Evlf-Qwen2.5-1.5B-Final`
- **Method:** LoRA fine-tuning with 4-bit quantization
- **Epochs:** 5 for large datasets (>300 examples), 10 for small datasets

### Dataset Categories

1. **Core** (4 datasets): Evlf's persona, background, relationship with user
2. **Human-like** (9 datasets): Conversation skills, emotions, philosophy, planning, etc.
3. **Themed** (6 datasets): Daily life, identity, romance, support, emotions
4. **Original** (3 datasets): Foundation datasets

## 💬 Chat Interface

The chat interface loads the final model and provides an interactive conversation experience.

**Features:**

- Optimized generation parameters (temperature, top_p, repetition penalty)
- 512 token responses
- CPU offloading support for running alongside training

## 📊 Model Details

- **Base Model:** Qwen/Qwen2.5-1.5B-Instruct
- **Fine-tuning:** LoRA (r=16, alpha=16, dropout=0.1)
- **Quantization:** 4-bit NF4
- **Training:** SFT (Supervised Fine-Tuning) with validation

## 🛠️ Development

### Re-train a specific dataset

```bash
cd training
python train.py
```

### Train on multiple datasets

```bash
cd training
python train_multi_dataset.py
```

### Monitor training

```bash
cd training
python watch_training.py
```

## ⚠️ Requirements

- Python 3.8+
- CUDA-compatible GPU (recommended)
- 16GB+ RAM
- ~30GB disk space for models

## 📝 License

Personal use only.
