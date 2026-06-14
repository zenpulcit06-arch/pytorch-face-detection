#!/bin/bash

# install_pytorch.sh
# Auto-detects CUDA version from nvidia-smi and installs the matching PyTorch build.
# Run from inside your activated venv: bash scripts/install_pytorch.sh

set -e

echo ""
echo "================================================"
echo "  PyTorch installer for WSL2 + NVIDIA GPU"
echo "================================================"
echo ""

# --- Check nvidia-smi ---
if ! command -v nvidia-smi &> /dev/null; then
    echo "ERROR: nvidia-smi not found."
    echo ""
    echo "Fix: Install the latest NVIDIA Game Ready or Studio driver on Windows."
    echo "     Download from: https://www.nvidia.com/Download/index.aspx"
    echo "     (Install on Windows — not inside WSL. WSL2 inherits it automatically.)"
    exit 1
fi

echo "GPU info:"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
echo ""

# --- Detect CUDA version ---
CUDA_VERSION=$(nvidia-smi | grep -oP "CUDA Version: \K[0-9]+\.[0-9]+" | head -1)

if [ -z "$CUDA_VERSION" ]; then
    echo "ERROR: Could not detect CUDA version from nvidia-smi."
    echo "Please install PyTorch manually. See SETUP.md Step 5."
    exit 1
fi

echo "Detected CUDA version: $CUDA_VERSION"
CUDA_MAJOR=$(echo $CUDA_VERSION | cut -d. -f1)
CUDA_MINOR=$(echo $CUDA_VERSION | cut -d. -f2)

# --- Map CUDA version to PyTorch wheel ---
if [ "$CUDA_MAJOR" -eq 11 ] && [ "$CUDA_MINOR" -ge 8 ]; then
    WHEEL_URL="https://download.pytorch.org/whl/cu118"
    CUDA_TAG="cu118"
elif [ "$CUDA_MAJOR" -eq 12 ] && [ "$CUDA_MINOR" -le 1 ]; then
    WHEEL_URL="https://download.pytorch.org/whl/cu121"
    CUDA_TAG="cu121"
elif [ "$CUDA_MAJOR" -eq 12 ] && [ "$CUDA_MINOR" -ge 2 ]; then
    WHEEL_URL="https://download.pytorch.org/whl/cu124"
    CUDA_TAG="cu124"
else
    echo "WARNING: CUDA $CUDA_VERSION is older than 11.8."
    echo "PyTorch 2.x requires CUDA 11.8 or newer."
    echo "Please update your NVIDIA driver on Windows."
    exit 1
fi

echo "Installing PyTorch for $CUDA_TAG..."
echo "Wheel URL: $WHEEL_URL"
echo ""

pip install torch torchvision torchaudio --index-url "$WHEEL_URL"

echo ""
echo "PyTorch installed. Running quick check..."
python -c "
import torch
print(f'PyTorch version : {torch.__version__}')
print(f'CUDA available  : {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU             : {torch.cuda.get_device_name(0)}')
    print(f'CUDA version    : {torch.version.cuda}')
    t = torch.randn(3,3).cuda()
    print(f'Tensor on GPU   : {t.device}')
    print()
    print('All good! PyTorch can see your GPU.')
else:
    print()
    print('WARNING: CUDA not available in PyTorch even though nvidia-smi works.')
    print('Try: pip install torch torchvision --index-url $WHEEL_URL --force-reinstall')
"
