import torch
import sys

print("=" * 50)
print("PyTorch & CUDA Installation Check")
print("=" * 50)
print(f"PyTorch version: {torch.__version__}")
print(f"Python version: {sys.version}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"cuDNN version: {torch.backends.cudnn.version()}")
    print(f"Device count: {torch.cuda.device_count()}")
    print(f"Current device: {torch.cuda.current_device()}")
    print(f"Device name: {torch.cuda.get_device_name(0)}")
else:
    print("\n⚠️  CUDA is NOT available!")
    print("This could mean:")
    print("  1. PyTorch was installed without CUDA support (CPU-only version)")
    print("  2. NVIDIA drivers are not installed or outdated")
    print("  3. No CUDA-capable GPU is present")
    print("\nTo install PyTorch with CUDA, visit: https://pytorch.org/get-started/locally/")
print("=" * 50)
