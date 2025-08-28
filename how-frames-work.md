# How Frames Work in Hunyuan-GameCraft

## Overview

The Hunyuan-GameCraft system generates high-dynamic interactive game videos using diffusion models and a hybrid history-conditioned training strategy. The frame handling is complex due to several factors:

1. **Causal VAE compression** (spatial and temporal with different ratios)
2. **Hybrid history conditioning** (using past frames/clips as context for autoregressive generation)
3. **Different generation modes** (image-to-video vs. video-to-video continuation)
4. **Rotary position embeddings (RoPE)** requirements for the MM-DiT backbone

## Paper Context

According to the paper, Hunyuan-GameCraft:
- Operates at **25 FPS** with each video chunk comprising **33-frame clips** at 720p resolution
- Uses a **causal VAE** for encoding/decoding that has uneven encoding of initial vs. subsequent frames
- Implements **chunk-wise autoregressive extension** where each chunk corresponds to one action
- Employs **hybrid history conditioning** with ratios: 70% single historical clip, 5% multiple clips, 25% single frame

## Key Frame Numbers Explained

### The Magic Numbers: 33, 34, 37, 66, 69

These numbers are fundamental to the architecture and not arbitrary:

- **33 frames**: The base video chunk size - each action generates exactly 33 frames (1.32 seconds at 25 FPS)
- **34 frames**: Used for image-to-video generation in latent space (33 + 1 initial frame)
- **37 frames**: Used for rotary position embeddings when starting from an image
- **66 frames**: Used for video-to-video continuation in latent space (2 × 33 frame chunks)
- **69 frames**: Used for rotary position embeddings when continuing from video

### Why These Specific Numbers?

The paper mentions "chunk latent denoising" where each chunk is a 33-frame segment. The specific numbers arise from:

1. **Base Chunk Size**: 33 frames per action (fixed by training)
2. **Initial Frame Handling**: +1 frame for the reference image in image-to-video mode
3. **RoPE Alignment**: +3 frames for proper positional encoding alignment in the transformer
4. **History Conditioning**: Doubling for video continuation (using previous chunk as context)

## VAE Compression Explained

### VAE Types and the "4n+1" / "8n+1" Formula

The project uses different VAE (Variational Autoencoder) models identified by codes like "884" or "888":

#### VAE Naming Convention: "XYZ-16c-hy0801"
- **First digit (X)**: Temporal compression ratio
- **Second digit (Y)**: Spatial compression ratio (height)
- **Third digit (Z)**: Spatial compression ratio (width)
- **16c**: 16 latent channels
- **hy0801**: Version identifier

#### "884" VAE (Default in Code)
- **Temporal compression**: 4:1 (every 4 frames → 1 latent frame)
- **Spatial compression**: 8:1 for both height and width
- **Frame formula**: 
  - Standard: `latent_frames = (video_frames - 1) // 4 + 1`
  - Special handling: `latent_frames = (video_frames - 2) // 4 + 2` (for certain cases)
- **Why "4n+1"?**: The causal VAE requires frames in multiples of 4 plus 1 for proper temporal compression
  - Example: 33 frames → (33-1)/4 + 1 = 9 latent frames
  - Example: 34 frames → (34-2)/4 + 2 = 9 latent frames (special case in pipeline)
  - Example: 66 frames → (66-2)/4 + 2 = 17 latent frames

#### "888" VAE (Alternative)
- **Temporal compression**: 8:1 (every 8 frames → 1 latent frame)
- **Spatial compression**: 8:1 for both height and width
- **Frame formula**: `latent_frames = (video_frames - 1) // 8 + 1`
- **Why "8n+1"?**: Similar principle but with 8:1 temporal compression
  - Example: 33 frames → (33-1)/8 + 1 = 5 latent frames
  - Example: 65 frames → (65-1)/8 + 1 = 9 latent frames

#### No Compression VAE
- When VAE code doesn't match the pattern, no temporal compression is applied
- `latent_frames = video_frames`

### Why Different Formulas?

The formulas handle the causal nature of the VAE as mentioned in the paper:

1. **Causal VAE Characteristics**: The paper states that causal VAEs have "uneven encoding of initial versus subsequent frames"
2. **First Frame Special Treatment**: The initial frame requires different handling than subsequent frames
3. **Temporal Consistency**: The causal attention ensures each frame only attends to previous frames, maintaining temporal coherence
4. **Chunk Boundaries**: The formulas ensure proper alignment with the 33-frame chunk size used in training

## Frame Processing Pipeline

### 1. Image-to-Video Generation (First Segment)

```python
# Starting from a single image
if is_image:
    target_length = 34  # In latent space
    # For RoPE embeddings
    freqs_cos, freqs_sin = get_rotary_pos_embed(37, height, width)
```

**Why 34 and 37?**
- 34 frames in latent space = 33 generated frames + 1 initial frame
- 37 for RoPE = 34 + 3 extra for positional encoding alignment

### 2. Video-to-Video Continuation

```python
# Continuing from existing video
else:
    target_length = 66  # In latent space
    # For RoPE embeddings
    freqs_cos, freqs_sin = get_rotary_pos_embed(69, height, width)
```

**Why 66 and 69?**
- 66 frames = 2 × 33 frames (using previous segment as context)
- 69 for RoPE = 66 + 3 extra for positional encoding alignment

### 3. Camera Network Compression

The CameraNet has special handling for these frame counts:

```python
def compress_time(self, x, num_frames):
    if x.shape[-1] == 66 or x.shape[-1] == 34:
        # Split into two segments
        x_len = x.shape[-1]
        # First segment: keep first frame, pool the rest
        x_clip1 = x[...,:x_len//2]
        # Second segment: keep first frame, pool the rest
        x_clip2 = x[...,x_len//2:x_len]
```

This compression strategy:
1. **Preserves key frames**: First frame of each segment
2. **Pools temporal information**: Averages remaining frames
3. **Maintains continuity**: Ensures smooth transitions

## Why Can't We Easily Change to 18 Frames?

Changing from 33 to 18 frames per chunk is problematic for multiple reasons:

### 1. Training-Time Fixed Parameters
According to the paper:
- The model was trained with **33-frame chunks at 25 FPS**
- The hybrid history conditioning ratios were optimized for 33-frame segments
- The entire dataset was annotated and partitioned into 6-second clips containing multiple 33-frame chunks

### 2. VAE Constraints
- **884 VAE**: Requires (n-1) or (n-2) divisible by 4
  - 18 frames: (18-1)/4 = 4.25 ❌ (not integer)
  - Would need 17 or 21 frames for proper compression
- **888 VAE**: Requires (n-1) divisible by 8
  - 18 frames: (18-1)/8 = 2.125 ❌ (not integer)
  - Would need 17 or 25 frames instead

### 3. Hardcoded Dependencies
Multiple components assume 33-frame chunks:
- **sample_inference.py**: Lines 525, 527, 613, 615 hardcode 34/37/66/69
- **cameranet.py**: Line 150 specifically checks for 34 or 66 frames
- **ActionToPoseFromID**: Hardcoded duration=33 for camera trajectory generation
- **app.py**: sample_n_frames=33 is fixed

### 4. Model Architecture Assumptions
- **MM-DiT backbone**: Trained with specific sequence lengths
- **Rotary Position Embeddings**: Optimized for 37/69 frame sequences
- **Camera encoder**: Designed for 33-frame action sequences
- **Attention patterns**: Expect these specific sequence lengths

## Recommendations for Frame Count Modification

If you must change frame counts, consider:

1. **Use VAE-compatible numbers**:
   - For 884 VAE: 17, 21, 25, 29, 33, 37... (4n+1 pattern)
   - For 888 VAE: 17, 25, 33, 41... (8n+1 pattern)

2. **Modify all dependent locations**:
   - `sample_inference.py`: Update target_length logic
   - `cameranet.py`: Update compress_time conditions
   - `ActionToPoseFromID`: Change duration parameter
   - App configuration: Update sample_n_frames

3. **Consider retraining or fine-tuning**:
   - The model may need adaptation for different sequence lengths
   - Quality might be suboptimal without retraining

4. **Test thoroughly**:
   - Different frame counts may expose edge cases
   - Ensure VAE encoding/decoding works correctly
   - Verify temporal consistency in generated videos

## Technical Details

### Latent Space Calculation Examples

For **884 VAE** (4:1 temporal compression):
```
Input: 33 frames → (33-1)/4 + 1 = 9 latent frames
Input: 34 frames → (34-2)/4 + 2 = 9 latent frames (special case)
Input: 66 frames → (66-2)/4 + 2 = 17 latent frames
```

For **888 VAE** (8:1 temporal compression):
```
Input: 33 frames → (33-1)/8 + 1 = 5 latent frames
Input: 65 frames → (65-1)/8 + 1 = 9 latent frames
```

### Memory Implications

Fewer frames = less memory usage:
- 33 frames at 704×1216: ~85MB per frame in FP16
- 18 frames would use ~46% less memory
- But VAE constraints limit viable options

## Paper-Code Consistency Analysis

The documentation is consistent with both the paper and the codebase:

### From the Paper:
- "The system operates at 25 fps, with each video chunk comprising 33-frame clips at 720p resolution"
- Uses "chunk latent denoising process" for autoregressive generation
- Implements "hybrid history-conditioned training strategy"
- Mentions causal VAE's "uneven encoding of initial versus subsequent frames"

### From the Code:
- `sample_n_frames = 33` throughout the codebase
- VAE compression formulas match the 884/888 patterns
- Hardcoded frame values (34, 37, 66, 69) align with the chunk-based architecture
- CameraNet's special handling for 34/66 frames confirms the two-mode generation

## Conclusion

The frame counts in Hunyuan-GameCraft are fundamental to its architecture:

1. **33 frames** is the atomic unit, trained into the model and fixed by the dataset construction
2. **34/37 and 66/69** emerge from the interaction between:
   - The 33-frame chunk size
   - Causal VAE requirements
   - MM-DiT transformer's RoPE needs
   - Hybrid history conditioning strategy

3. The **884 VAE** (4:1 temporal compression) is the default, requiring frames in patterns of 4n+1 or 4n+2

4. Changing to different frame counts (like 18) would require:
   - Retraining the entire model
   - Reconstructing the dataset
   - Modifying the VAE architecture
   - Updating all hardcoded dependencies

The system's design reflects careful engineering trade-offs between generation quality, temporal consistency, and computational efficiency, as validated by the paper's experimental results showing superior performance compared to alternatives.