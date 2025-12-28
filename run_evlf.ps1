#!/usr/bin/env pwsh
# PowerShell script to run Evlf with BASE model + RAG memory

Write-Host "🚀 Starting Evlf (BASE Model + Memory)" -ForegroundColor Green
Write-Host ""

# Use the venv Python which has CUDA support
& .\.venv\Scripts\python.exe inference\chat_v2.py
