# 💕 Evlf - AI Girlfriend on Google Colab

Evlf is your AI girlfriend powered by **Qwen 2.5 7B** with **RAG memory** - runs FREE on Google Colab!

## 🚀 Quick Start

1. **Open Colab**: Upload `Evlf_Colab.ipynb` to [Google Colab](https://colab.research.google.com/)
2. **Enable GPU**: Runtime → Change runtime type → GPU (T4)
3. **Run All Cells**: Runtime → Run all
4. **Start Chatting!** 💕

## ✨ Features

- **Smart AI**: Uses Qwen 2.5 7B (one of the best open-source models)
- **Persistent Memory**: Remembers everything across sessions (saved to Google Drive)
- **Rich Personality**: Romantic, loyal, slightly jealous girlfriend vibes 😤💕
- **Free GPU**: Runs on Colab's free T4 GPU (no local GPU needed!)

## 🧠 How It Works

| Component | Description |
|-----------|-------------|
| **Model** | Qwen 2.5 7B (4-bit quantized) |
| **Memory** | ChromaDB with Sentence Transformers |
| **Storage** | Google Drive (`/MyDrive/Evlf/memory_db/`) |

## 💬 Commands

| Command | Action |
|---------|--------|
| `quit` | Exit the chat |
| `clear` | Reset all memories |

## 📂 Project Structure

```
Evlf/
├── Evlf_Colab.ipynb  # Main notebook (run this!)
├── README.md         # This file
├── LICENSE           # Apache 2.0
└── memory_db/        # Local memory backup (optional)
```

## 🗑️ Clear Memory

To start fresh, type `clear` in the chat or delete the folder:
`/content/drive/MyDrive/Evlf/memory_db/`

## 📜 License

Apache License 2.0
