#!/usr/bin/env pwsh
# PowerShell script to run Evlf inference with the fine-tuned model using CUDA

Write-Host "🚀 Starting Evlf Chat (Fine-tuned Model with CUDA)" -ForegroundColor Cyan
Write-Host ""

# Use the venv Python which has CUDA support
& .\.venv\Scripts\python.exe inference\chat.py
