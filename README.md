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
├── datasets/           # Training data (organized by category)
│   ├── core/          # Core persona and relationship data
│   ├── human_like/    # Human-like conversation skills
│   ├── themed/        # Themed interactions
│   └── original/      # Original training data
├── models/            # Trained models
├── scripts/           # Project scripts
│   ├── data_generation/ # Data generation scripts
│   ├── setup/         # Setup and download scripts
│   └── utils/         # Utility scripts
├── training/          # Training scripts and tools
├── inference/         # Chat interface
└── docs/              # Documentation
```

## 🚀 Training

The model is trained sequentially on the datasets using LoRA fine-tuning.

### Training Summary

- **Base Model:** `meta-llama/Llama-3.2-3B-Instruct`
- **Method:** LoRA fine-tuning with 4-bit quantization (NF4)
- **Training:** SFT (Supervised Fine-Tuning)

### Scripts Organization

The `scripts/` directory contains all utility and generation scripts:

- **`data_generation/`**: Scripts for generating training datasets
  - `generate_evlf_persona.py` - Core personality data
  - `generate_evlf_eris_background.py` - Background stories
  - `generate_user_relationship.py` - Relationship dynamics
  - `generate_xebec_personal.py` - Personal interactions
  - `generate_girlfriend_casual.py` - Casual conversations
  - `generate_human_datasets.py` - Human-like responses
  - `generate_themed_data.py` - Themed interactions
  - `generate_dataset_v2.py` - Template-based dataset generator

- **`setup/`**: Setup and initialization scripts
  - `download_model.py` - Downloads the base Llama model

- **`utils/`**: Utility scripts for data management
  - `check_dataset_sizes.py` - Validates dataset file sizes
  - `check_metrics.py` - Analyzes training metrics
  - `rebalance_datasets.py` - Balances dataset distributions

### Dataset Categories

1. **Core** (4 datasets): Evlf's persona, background, relationship with user
2. **Human-like** (9 datasets): Conversation skills, emotions, philosophy, planning
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
