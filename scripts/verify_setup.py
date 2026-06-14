"""
verify_setup.py
Run this after setup to confirm every dependency is installed and the GPU is accessible.
Usage: python scripts/verify_setup.py
"""

import sys

RESET  = "\033[0m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"

def ok(label, value=""):
    tag = f"{GREEN}✓{RESET}"
    print(f"  {tag}  {label:<20} {value}")

def fail(label, reason=""):
    tag = f"{RED}✗{RESET}"
    print(f"  {tag}  {label:<20} {RED}{reason}{RESET}")

def warn(label, reason=""):
    tag = f"{YELLOW}!{RESET}"
    print(f"  {tag}  {label:<20} {YELLOW}{reason}{RESET}")

print()
print(f"{BOLD}Checking setup...{RESET}")
print()

errors = 0

# --- Python version ---
major, minor = sys.version_info[:2]
ver = f"{major}.{minor}.{sys.version_info[2]}"
if major == 3 and minor >= 9:
    ok("Python", ver)
else:
    fail("Python", f"{ver} — need 3.9+")
    errors += 1

# --- PyTorch ---
try:
    import torch
    ok("PyTorch", torch.__version__)
except ImportError:
    fail("PyTorch", "not installed — run: bash scripts/install_pytorch.sh")
    errors += 1

# --- CUDA ---
try:
    import torch
    if torch.cuda.is_available():
        gpu = torch.cuda.get_device_name(0)
        cuda_ver = torch.version.cuda
        ok("CUDA", f"{cuda_ver} — {gpu}")
        # Quick tensor test on GPU
        try:
            t = torch.randn(100, 100).cuda()
            _ = (t @ t).cpu()
            ok("GPU compute", "matrix multiply OK")
        except Exception as e:
            fail("GPU compute", str(e))
            errors += 1
    else:
        warn("CUDA", "not available — CPU only (training will be slow)")
except Exception as e:
    fail("CUDA check", str(e))
    errors += 1

# --- torchvision ---
try:
    import torchvision
    ok("torchvision", torchvision.__version__)
except ImportError:
    fail("torchvision", "not installed")
    errors += 1

# --- numpy ---
try:
    import numpy as np
    ok("numpy", np.__version__)
except ImportError:
    fail("numpy", "not installed")
    errors += 1

# --- OpenCV ---
try:
    import cv2
    ok("opencv-python", cv2.__version__)
except ImportError:
    fail("opencv-python", "not installed — pip install opencv-python")
    errors += 1

# --- matplotlib ---
try:
    import matplotlib
    ok("matplotlib", matplotlib.__version__)
except ImportError:
    fail("matplotlib", "not installed")
    errors += 1

# --- Pillow ---
try:
    from PIL import Image
    import PIL
    ok("Pillow", PIL.__version__)
except ImportError:
    fail("Pillow", "not installed")
    errors += 1

# --- tqdm ---
try:
    import tqdm
    ok("tqdm", tqdm.__version__)
except ImportError:
    fail("tqdm", "not installed")
    errors += 1

# --- albumentations ---
try:
    import albumentations
    ok("albumentations", albumentations.__version__)
except ImportError:
    fail("albumentations", "not installed")
    errors += 1

# --- Jupyter kernel ---
try:
    import ipykernel
    ok("ipykernel", ipykernel.__version__)
except ImportError:
    warn("ipykernel", "not installed — run: pip install ipykernel")

print()

if errors == 0:
    print(f"{GREEN}{BOLD}All checks passed. You are ready to go!{RESET}")
    print(f"Launch Jupyter with: {BOLD}jupyter notebook --no-browser --port=8888{RESET}")
else:
    print(f"{RED}{BOLD}{errors} check(s) failed. Fix the issues above and re-run.{RESET}")
    sys.exit(1)

print()
