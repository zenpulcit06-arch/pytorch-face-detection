# Setup Guide — WSL2 + Windows 11 + NVIDIA GPU

Follow this exactly, top to bottom. Every command is meant to run inside **WSL2 Ubuntu terminal**.

---

## Step 1 — Check your NVIDIA driver and CUDA

Open WSL2 terminal and run:

```bash
nvidia-smi
```

You should see a table showing your GPU. Look for the line:
```
CUDA Version: XX.X
```

> **If nvidia-smi is not found**: Your NVIDIA driver is not set up for WSL2.
> Download and install the latest Game Ready or Studio driver from https://www.nvidia.com/Download/index.aspx
> (Install on Windows — it automatically enables WSL2 GPU support. Do NOT install a Linux CUDA driver inside WSL.)

Note down your CUDA version — you need it in Step 4.

---

## Step 2 — Make sure WSL2 Ubuntu is up to date

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git curl wget unzip
```

---

## Step 3 — Clone the repo

```bash
# Go to your preferred folder, e.g. home directory
cd ~

git clone https://github.com/YOUR_USERNAME/pytorch-face-detection.git
cd pytorch-face-detection
```

> If you haven't created the GitHub repo yet, just create the folder manually:
> ```bash
> mkdir ~/pytorch-face-detection && cd ~/pytorch-face-detection
> ```

---

## Step 4 — Create and activate a Python venv

```bash
# Create venv inside the project folder
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt should now show (venv) at the start
# Every command from here runs inside this venv
```

> **Important**: You need to run `source venv/bin/activate` every time you open a new WSL terminal.
> Or add an alias — see the tip at the bottom of this file.

---

## Step 5 — Install PyTorch with CUDA

Pick the command that matches your CUDA version from Step 1:

**CUDA 11.8**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**CUDA 12.1**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**CUDA 12.4 or newer**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

**Not sure / want to auto-detect**
```bash
# Run this helper script — it detects your CUDA version and installs the right PyTorch
bash scripts/install_pytorch.sh
```

---

## Step 6 — Install remaining dependencies

```bash
pip install -r requirements.txt
```

---

## Step 7 — Install and configure Jupyter for WSL2

```bash
pip install jupyter ipykernel

# Register your venv as a Jupyter kernel
python -m ipykernel install --user --name pytorch-face --display-name "PyTorch Face (venv)"
```

### Launching Jupyter from WSL2

WSL2 doesn't have a browser, so you need to copy the URL to your Windows browser:

```bash
jupyter notebook --no-browser --port=8888
```

You will see output like:
```
http://localhost:8888/?token=abc123...
```

Copy that URL and paste it into your **Windows browser** (Chrome / Edge). It works because WSL2 forwards localhost ports to Windows automatically.

> **Tip — add an alias so you don't type this every time:**
> ```bash
> echo 'alias jnb="jupyter notebook --no-browser --port=8888"' >> ~/.bashrc
> source ~/.bashrc
> # Now just type: jnb
> ```

---

## Step 8 — Verify everything works

```bash
python scripts/verify_setup.py
```

Expected output:
```
✓ Python      3.x.x
✓ PyTorch     2.x.x
✓ CUDA        available — GeForce RTX XXXX
✓ torchvision 0.x.x
✓ numpy       1.x.x
✓ cv2         4.x.x
✓ matplotlib  3.x.x
All checks passed. You are ready to go!
```

---

## Useful WSL2 tips

### Access your project from Windows Explorer
Your WSL2 files are at:
```
\\wsl$\Ubuntu\home\YOUR_USERNAME\pytorch-face-detection
```

### Access Windows files from WSL2
Your Windows C: drive is mounted at `/mnt/c/` inside WSL2.

### Recommended alias block — add to ~/.bashrc
```bash
# Activate project venv
alias facevenv="cd ~/pytorch-face-detection && source venv/bin/activate"

# Launch Jupyter
alias jnb="jupyter notebook --no-browser --port=8888"

# Combined: activate + launch
alias facelab="facevenv && jnb"
```

Apply with: `source ~/.bashrc`

---

## Common issues

| Problem | Fix |
|---------|-----|
| `nvidia-smi` not found | Install/update NVIDIA driver on Windows (not inside WSL) |
| `CUDA not available` in PyTorch | Reinstall PyTorch with the correct `--index-url` for your CUDA version |
| Jupyter URL doesn't open | Make sure you copied the full URL including the token |
| `pip: command not found` | Run `source venv/bin/activate` first |
| Packages installed but not found | Check you're in the venv — prompt should show `(venv)` |
| Slow file I/O on datasets | Keep the `data/` folder inside WSL filesystem (`~/`), not on `/mnt/c/` |

> **Last point is important for training speed**: accessing files through `/mnt/c/` in WSL2 is significantly slower than files stored inside the WSL filesystem. Always keep your dataset inside `~/`.
