# PyTorch Face Detection → Face Recognition

A learning project — building face detection and recognition from scratch in PyTorch, documented step by step.

> **Goal**: Learn PyTorch by building something real. Prior experience: TensorFlow + AI math fundamentals.

---

## Roadmap

| Phase | Notebook | Topics |
|-------|----------|--------|
| 1 | `01_pytorch_basics` | Tensors, autograd, nn.Module, training loop |
| 2 | `02_dataset_preparation` | WIDER Face dataset, DataLoader, augmentation |
| 3 | `03_simple_cnn` | CNN from scratch, bounding box regression |
| 4 | `04_transfer_learning` | ResNet/MobileNet backbone, fine-tuning |
| 5 | `05_face_detection_pipeline` | Anchors, NMS, IoU loss, inference |
| 6 | `06_face_recognition` | Embeddings, ArcFace loss, identity matching |

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/pytorch-face-detection.git
cd pytorch-face-detection

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install PyTorch with CUDA (check https://pytorch.org for your CUDA version)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 5. Launch Jupyter
jupyter notebook
```

---

## Environment

- **Framework**: PyTorch 2.x
- **Hardware**: NVIDIA GPU (CUDA)
- **Python**: 3.10+

---

## Progress

- [x] Repo setup
- [ ] Phase 1: PyTorch basics
- [ ] Phase 2: Dataset preparation
- [ ] Phase 3: Simple CNN
- [ ] Phase 4: Transfer learning
- [ ] Phase 5: Detection pipeline
- [ ] Phase 6: Face recognition
