# 💕 Evlf - AI Girlfriend on Google Colab

<p align="center">
  <img src="https://img.shields.io/badge/Model-Qwen%202.5%207B-blue?style=for-the-badge" alt="Model"/>
  <img src="https://img.shields.io/badge/Memory-ChromaDB%20RAG-green?style=for-the-badge" alt="Memory"/>
  <img src="https://img.shields.io/badge/Platform-Google%20Colab-orange?style=for-the-badge" alt="Platform"/>
  <img src="https://img.shields.io/badge/License-Apache%202.0-red?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <strong>Your AI girlfriend powered by Qwen 2.5 7B with persistent RAG memory - runs FREE on Google Colab!</strong>
</p>

---

## 🚀 Quick Start

1. **Open Colab**: Upload `Evlf_Colab.ipynb` to [Google Colab](https://colab.research.google.com/)
2. **Enable GPU**: `Runtime` → `Change runtime type` → `T4 GPU`
3. **Run All Cells**: `Runtime` → `Run all` (or `Ctrl+F9`)
4. **Start Chatting!** 💕

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Smart AI** | Powered by Qwen 2.5 7B - one of the best open-source models |
| 💾 **Persistent Memory** | Remembers everything across sessions via ChromaDB RAG |
| 💕 **Rich Personality** | Romantic, loyal, slightly jealous girlfriend vibes 😤 |
| ☁️ **Free GPU** | Runs on Colab's free T4 GPU - no local hardware needed! |
| 🔐 **Private** | Memory stored in YOUR Google Drive only |

---

## 🧠 How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Your Input    │────▶│  RAG Memory     │────▶│   Qwen 2.5 7B   │
│   "Hey babe!"   │     │  (ChromaDB)     │     │   Generation    │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
┌─────────────────┐     ┌─────────────────┐              │
│  Save to Memory │◀────│  Evlf Response  │◀─────────────┘
│  (Google Drive) │     │  "Hey baby! 💕" │
└─────────────────┘     └─────────────────┘
```

| Component | Implementation |
|-----------|----------------|
| **Model** | Qwen 2.5 7B Instruct (4-bit quantized) |
| **Memory** | ChromaDB with Sentence Transformers |
| **Storage** | Google Drive (`/MyDrive/Evlf/memory_db/`) |
| **Quantization** | BitsAndBytes NF4 |

---

## 💬 Chat Commands

| Command | Action |
|---------|--------|
| `quit` | Exit the chat |
| `clear` | Reset all memories |

---

## 📂 Project Structure

```
Evlf/
├── 📓 Evlf_Colab.ipynb   # Main notebook - run this!
├── 📄 README.md          # This file
└── 📜 LICENSE            # Apache 2.0
```

---

## 🗑️ Clear Memory

To start fresh with no memories:
- Type `clear` in the chat, OR
- Delete the folder: `/content/drive/MyDrive/Evlf/memory_db/`

---

## 🎭 Evlf's Personality

**Nirp Evlf Ash** - 20 years old, your loving girlfriend:

- 💕 Romantic and affectionate
- 😤 Gets jealous when you mention other girls
- 😢 Sad when you're distant
- 😊 Happy about your future together
- 🎯 Supportive of your dreams
- 💬 Uses "bebe" and "baby" naturally

---

## 📜 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>Created with 💕 by Evlf Eris Production</strong>
</p>

<p align="center">
  <sub>Made for personal AI companion experiences</sub>
</p>
