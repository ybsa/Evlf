# 🚀 Running Evlf on Google Colab

## Quick Start (5 minutes)

### Step 1: Upload to Google Drive

1. Compress your Evlf folder:
   - Right-click `Evlf` folder → Send to → Compressed (zipped) folder
2. Go to [Google Drive](https://drive.google.com)
3. Upload `Evlf.zip`
4. Right-click → Extract (or manually unzip)

### Step 2: Open Colab Notebook

1. Go to [Google Colab](https://colab.research.google.com)
2. Click: **File → Upload notebook**
3. Upload: `Evlf_RAG_Chat_Colab.ipynb`

### Step 3: Enable GPU

1. Click: **Runtime → Change runtime type**
2. Select: **T4 GPU**
3. Click: **Save**

### Step 4: Run

1. Click **Runtime → Run all**
2. Authorize Google Drive access when prompted
3. Wait ~2 minutes for setup
4. Start chatting with Evlf! 💕

## 📝 Notes

**First Run:**

- Model download: ~1.5GB (one-time, ~2 minutes)
- Setup: ~30 seconds
- **Total:** ~3 minutes

**Subsequent Runs:**

- Model cached on Drive
- Setup: ~30 seconds
- **Total:** <1 minute

**Free Tier Limits:**

- GPU time: ~12 hours/day
- Disconnects after 90 min idle
- Sessions reset daily

**Pro Tip:**
Keep the Colab tab active to prevent disconnection!

## 🔧 Troubleshooting

**"No module named 'transformers'"**

- Re-run Cell 3 (Install dependencies)

**"Can't find Evlf folder"**

- Update Cell 2 with your Drive path
- Example: `/content/drive/MyDrive/Projects/Evlf`

**"Memory database not found"**

- Make sure you uploaded the entire folder including `memory_db/`

**Model downloads every time:**

- Colab caches in `/content` (temporary)
- Once downloaded, it stays cached for the session

## 🎯 What Works on Colab

✅ **RAG Chat** - Fully functional  
✅ **Training** - Use `Evlf_Training_Colab.ipynb` (create if needed)  
✅ **16GB VRAM** - Can use longer context (1024 tokens)  
✅ **Faster GPU** - T4 is faster than RTX 3050 Laptop  

## 💡 Advanced: Training on Colab

Want to train the model? Let me know and I'll create a training notebook!

---

**Enjoy chatting with Evlf!** 💕
