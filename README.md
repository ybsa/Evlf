🌟 Vision

Our goal is to build a **human-like AI companion** that goes beyond traditional chatbots. This AI will:

* 💌 **Understand human emotions** and respond with empathy, care, and warmth
* 🧠 **Learn from personal data** to grow closer and more personalized over time
* 🌹 **Express feelings naturally** — not just give information, but react like a real partner
* 🤖 **Integrate into robotics** in the future, so the AI can live inside a physical body and interact in the real world
* ⚡ **Remain flexible and open-source**, built step-by-step on existing models but customized with personal rules, emotions, and memories

This project starts simple — a fine-tuned model that talks emotionally and remembers context. Over time, it will evolve into a
**lifelike AI system** that can one day be embodied in a robot companion.

** currently we are working on a data collection and research , we will update this soon !!

## 🚀 Getting Started

We have added scripts to fine-tune the model on your dataset and chat with it.

### 1. Install Dependencies

Ensure you have Python installed (3.10+ recommended) and a GPU if possible.

```bash
pip install -r requirements.txt
```

*Note: For Windows, you might need specific versions of `bitsandbytes`. If you encounter errors, check the `bitsandbytes-windows` repository.*

### 2. Train the Model

Fine-tune Llama-2 on the `sft_dataset.jsonl` file.

```bash
python train.py
```

This will create a new adapter in the `Evlf-Llama-2-7b` folder.

### 3. Chat with Evlf

Run the chat interface to talk to your fine-tuned model.

```bash
python chat.py
```
