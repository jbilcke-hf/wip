# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hunyuan-GameCraft is a high-dynamic interactive game video generation system that creates gameplay videos with controllable camera movements and actions. The system uses diffusion models and action-controlled generation to synthesize realistic game footage from reference images and keyboard/mouse input controls.

## Key Commands

### Installation
```bash
# Create and activate conda environment
conda create -n HYGameCraft python==3.10
conda activate HYGameCraft

# Install PyTorch and dependencies
conda install pytorch==2.5.1 torchvision==0.20.0 torchaudio==2.5.1 pytorch-cuda=12.4 -c pytorch -c nvidia

# Install requirements
python -m pip install -r requirements.txt

# Install flash attention (optional, for acceleration)
python -m pip install ninja
python -m pip install git+https://github.com/Dao-AILab/flash-attention.git@v2.6.3
```

### Download Models
```bash
cd weights
huggingface-cli download tencent/Hunyuan-GameCraft-1.0 --local-dir ./
```

### Run Inference

**Multi-GPU (8 GPUs) - Standard Model:**
```bash
torchrun --nnodes=1 --nproc_per_node=8 --master_port 29605 hymm_sp/sample_batch.py \
    --image-path "asset/village.png" \
    --prompt "YOUR_PROMPT" \
    --ckpt weights/gamecraft_models/mp_rank_00_model_states.pt \
    --video-size 704 1216 \
    --cfg-scale 2.0 \
    --image-start \
    --action-list w s d a \
    --action-speed-list 0.2 0.2 0.2 0.2 \
    --seed 250160 \
    --infer-steps 50 \
    --save-path './results/'
```

**Single GPU with Low VRAM (24GB minimum):**
```bash
export DISABLE_SP=1
export CPU_OFFLOAD=1
torchrun --nnodes=1 --nproc_per_node=1 --master_port 29605 hymm_sp/sample_batch.py \
    --ckpt weights/gamecraft_models/mp_rank_00_model_states.pt \
    --cpu-offload \
    --use-fp8 \
    [other parameters...]
```

**Distilled Model (faster, 8 inference steps):**
```bash
torchrun --nnodes=1 --nproc_per_node=8 --master_port 29605 hymm_sp/sample_batch.py \
    --ckpt weights/gamecraft_models/mp_rank_00_model_states_distill.pt \
    --cfg-scale 1.0 \
    --infer-steps 8 \
    --use-fp8 \
    [other parameters...]
```

## Architecture Overview

### Core Components

1. **Main Entry Points**
   - `hymm_sp/sample_batch.py`: Main script for batch video generation with distributed processing
   - `hymm_sp/sample_inference.py`: Core inference logic and model sampling
   - `hymm_sp/config.py`: Configuration parsing and argument handling

2. **Model Architecture (`hymm_sp/modules/`)**
   - `models.py`: Core diffusion model implementation
   - `cameranet.py`: Camera control and action encoding for game interactions
   - `token_refiner.py`: Text token refinement for prompt conditioning
   - `parallel_states.py`: Distributed training/inference state management
   - `fp8_optimization.py`: FP8 quantization for memory/speed optimization

3. **VAE Module (`hymm_sp/vae/`)**
   - `autoencoder_kl_causal_3d.py`: 3D causal VAE for video encoding/decoding
   - Handles latent space conversion for video frames

4. **Diffusion Pipeline (`hymm_sp/diffusion/`)**
   - `pipeline_hunyuan_video_game.py`: Custom pipeline for game video generation
   - `scheduling_flow_match_discrete.py`: Flow matching scheduler for denoising

5. **Data Processing (`hymm_sp/data_kits/`)**
   - `video_dataset.py`: Dataset handling for video inputs
   - `data_tools.py`: Video saving and processing utilities

### Key Features

- **Action Control**: Maps keyboard inputs (w/a/s/d) to continuous camera space for smooth transitions
- **Hybrid History Conditioning**: Extends video sequences autoregressively while preserving scene context
- **Model Distillation**: Accelerated inference model (8 steps vs 50 steps)
- **Memory Optimization**: FP8 quantization, CPU offloading, and SageAttention support
- **Distributed Processing**: Multi-GPU support with sequence parallelism

### Important Parameters

- `--action-list`: Sequence of keyboard actions (w/a/s/d)
- `--action-speed-list`: Movement speed for each action (0.0-3.0)
- `--video-size`: Output resolution (height width)
- `--cfg-scale`: Classifier-free guidance scale (1.0 for distilled, 2.0 for standard)
- `--infer-steps`: Denoising steps (8 for distilled, 50 for standard)
- `--use-fp8`: Enable FP8 optimization for memory reduction
- `--cpu-offload`: Offload model to CPU for low VRAM scenarios

### Model Weights Structure
```
weights/
├── gamecraft_models/
│   ├── mp_rank_00_model_states.pt        # Standard model
│   └── mp_rank_00_model_states_distill.pt # Distilled model
└── stdmodels/
    ├── vae_3d/                            # 3D VAE model
    ├── llava-llama-3-8b-v1_1-transformers/ # Text encoder
    └── openai_clip-vit-large-patch14/     # CLIP encoder
```

## Development Notes

- Environment variable `MODEL_BASE` should point to `weights/stdmodels`
- Use `export DISABLE_SP=1` and `export CPU_OFFLOAD=1` for single GPU inference
- Minimum GPU memory: 24GB (very slow), Recommended: 80GB per GPU
- Action length determines video duration (1 action = 33 frames at 25 FPS)
- SageAttention can be installed for additional acceleration