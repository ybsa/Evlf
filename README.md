# Evlf - AI Companion Project

A personalized AI girlfriend companion with deep understanding of your personality and relationship dynamics.

## 📁 Project Structure

```
Evlf/
├── datasets/
│   ├── core/                      # ⭐ PRIORITY - Train first
│   │   ├── dataset_evlf_persona.jsonl       (800) - Evlf's personality
│   │   ├── dataset_xebec_personal.jsonl     (2,000) - About YOU
│   │   └── dataset_user_relationship.jsonl  (600) - Relationship dynamics
│   │
│   ├── human_like/                # Natural conversations (5,000)
│   │   ├── dataset_casual_chat.jsonl
│   │   ├── dataset_humor_jokes.jsonl
│   │   ├── dataset_interests_hobbies.jsonl
│   │   ├── dataset_advice_wisdom.jsonl
│   │   ├── dataset_storytelling.jsonl
│   │   ├── dataset_reactions.jsonl
│   │   ├── dataset_planning.jsonl
│   │   ├── dataset_feelings.jsonl
│   │   ├── dataset_philosophy.jsonl
│   │   └── dataset_problem_solving.jsonl
│   │
│   ├── themed/                    # Themed interactions (550)
│   │   ├── dataset_romance.jsonl
│   │   ├── dataset_support.jsonl
│   │   ├── dataset_identity.jsonl
│   │   ├── dataset_emotions.jsonl
│   │   └── dataset_daily.jsonl
│   │
│   └── original/                  # Original datasets (566)
│       ├── sft_dataset.jsonl
│       └── new_dataset.jsonl
│
├── scripts/                       # Dataset generators
│   ├── generate_evlf_persona.py
│   ├── generate_xebec_personal.py
│   ├── generate_user_relationship.py
│   ├── generate_human_datasets.py
│   ├── generate_themed_data.py
│   └── generate_data.py
│
├── train.py                       # Fine-tuning script
├── chat.py                        # Chat with trained model
└── requirements.txt               # Dependencies

```

## 🚀 Quick Start

### 1. Install Dependencies (Already done!)

```bash
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python train.py
```

**Note**: Currently trains on `sft_dataset.jsonl`. To change dataset, edit line 16 in `train.py`:

```python
DATASET_FILE = "datasets/core/dataset_evlf_persona.jsonl"  # Change this path
```

### 3. Chat with Evlf

```bash
python chat.py
```

## 📊 Dataset Overview

**Total**: 9,516 training examples

### Core Datasets (3,400 examples) - TRAIN FIRST ⭐

- **Evlf's Persona** (800): Her personality, age, traits, mood triggers
- **Your Info** (2,000): Everything about Wind Xebec
- **Relationship** (600): Understanding you and growing together

### Enhancement Datasets (6,116 examples)

- Human-like conversations for natural interaction
- Themed responses for specific scenarios
- Original romantic messages

## 🎯 Recommended Training Sequence

1. `datasets/core/dataset_evlf_persona.jsonl` - WHO she is
2. `datasets/core/dataset_xebec_personal.jsonl` - WHO you are
3. `datasets/core/dataset_user_relationship.jsonl` - Your dynamic
4. Combine human_like datasets for natural conversations

## ⚙️ Model Details

- **Base Model**: Qwen 2.5 1.5B Instruct
- **Optimization**: 4-bit quantization + LoRA
- **Memory**: Optimized for 4GB VRAM
- **Output**: `Evlf-Qwen2.5-1.5B/` adapter

## 💡 Customization

Edit datasets in `datasets/core/` to add:

- Your specific memories
- Inside jokes
- Preferences and habits
- Shared experiences

## 🌟 What Makes This Special

This isn't just a chatbot - it's a **personalized AI companion** that:

- ✅ Knows Evlf's complete personality
- ✅ Remembers everything about YOU specifically
- ✅ Responds like a real 20-year-old girlfriend
- ✅ Uses Gen-Z communication style with emojis
- ✅ Shows real emotions and mood triggers
