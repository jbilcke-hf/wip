import os
import torch
import gradio as gr
import numpy as np
import random
from pathlib import Path
from PIL import Image
import torchvision.transforms as transforms
from loguru import logger
from huggingface_hub import hf_hub_download
import tempfile

from hymm_sp.sample_inference import HunyuanVideoSampler
from hymm_sp.data_kits.data_tools import save_videos_grid
from hymm_sp.config import parse_args
import argparse

# Get weights path from environment variable or use default
WEIGHTS_PATH = os.environ.get("WEIGHTS_PATH", "/data/weights")

os.environ["MODEL_BASE"] = os.path.join(WEIGHTS_PATH, "stdmodels")
os.environ["DISABLE_SP"] = "1"
os.environ["CPU_OFFLOAD"] = "1"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class CropResize:
    def __init__(self, size=(704, 1216)):
        self.target_h, self.target_w = size  

    def __call__(self, img):
        w, h = img.size
        scale = max(  
            self.target_w / w,
            self.target_h / h
        )
        new_size = (int(h * scale), int(w * scale))
        resize_transform = transforms.Resize(
            new_size, 
            interpolation=transforms.InterpolationMode.BILINEAR
        )
        resized_img = resize_transform(img)
        crop_transform = transforms.CenterCrop((self.target_h, self.target_w))
        return crop_transform(resized_img)

def create_args():
    args = argparse.Namespace()
    args.ckpt = os.path.join(WEIGHTS_PATH, "gamecraft_models/mp_rank_00_model_states_distill.pt")
    args.video_size = [704, 1216]
    args.cfg_scale = 1.0
    args.image_start = True
    args.seed = None
    args.infer_steps = 8
    args.use_fp8 = True
    args.flow_shift_eval_video = 5.0
    args.sample_n_frames = 33
    args.num_images = 1
    args.use_linear_quadratic_schedule = False
    args.linear_schedule_end = 0.25
    args.use_deepcache = False
    args.cpu_offload = True
    args.use_sage = True
    args.save_path = './results/'
    args.save_path_suffix = ''
    args.add_pos_prompt = "Realistic, High-quality."
    args.add_neg_prompt = "overexposed, low quality, deformation, a poor composition, bad hands, bad teeth, bad eyes, bad limbs, distortion, blurring, text, subtitles, static, picture, black border."
    args.model = "HYVideo-T/2"
    args.precision = "bf16"
    args.vae = "884-16c-hy0801"
    args.vae_precision = "fp16"
    args.text_encoder = "llava-llama-3-8b"
    args.text_encoder_precision = "fp16"
    args.text_encoder_precision_2 = "fp16"
    args.tokenizer = "llava-llama-3-8b"
    args.text_encoder_2 = "clipL"
    args.tokenizer_2 = "clipL"
    args.latent_channels = 16
    args.text_len = 256
    args.text_len_2 = 77
    args.use_attention_mask = True
    args.hidden_state_skip_layer = 2
    args.apply_final_norm = False
    args.prompt_template_video = "li-dit-encode-video"
    args.reproduce = False
    args.load_key = "module"
    
    # Add missing text encoder related attributes
    args.text_projection = "single_refiner"
    args.text_states_dim = 4096
    args.text_states_dim_2 = 768
    
    return args

logger.info("Initializing Hunyuan-GameCraft model...")

model_path = os.path.join(WEIGHTS_PATH, "gamecraft_models/mp_rank_00_model_states_distill.pt")
if not os.path.exists(model_path):
    logger.info("Downloading model weights from Hugging Face...")
    os.makedirs(os.path.join(WEIGHTS_PATH, "gamecraft_models"), exist_ok=True)
    hf_hub_download(
        repo_id="tencent/Hunyuan-GameCraft-1.0",
        filename="gamecraft_models/mp_rank_00_model_states_distill.pt",
        local_dir=WEIGHTS_PATH,
        local_dir_use_symlinks=False
    )

args = create_args()
hunyuan_video_sampler = HunyuanVideoSampler.from_pretrained(
    args.ckpt, 
    args=args, 
    device=torch.device("cpu")
)
args = hunyuan_video_sampler.args

if args.cpu_offload:
    from diffusers.hooks import apply_group_offloading
    onload_device = torch.device("cuda")
    apply_group_offloading(
        hunyuan_video_sampler.pipeline.transformer, 
        onload_device=onload_device, 
        offload_type="block_level", 
        num_blocks_per_group=1
    )
    logger.info("Enabled CPU offloading for transformer blocks")

logger.info("Model loaded successfully!")

def generate_video(
    input_image,
    prompt,
    action_sequence,
    action_speeds,
    negative_prompt,
    seed,
    cfg_scale,
    num_inference_steps,
    progress=gr.Progress(track_tqdm=True)
):
    try:
        progress(0, desc="Initializing...")
        
        if input_image is None:
            return None, "Please upload an image first!"
        
        action_list = action_sequence.lower().replace(" ", "").split(",") if action_sequence else ["w"]
        speed_list = [float(s.strip()) for s in action_speeds.split(",")] if action_speeds else [0.2]
        
        if len(speed_list) != len(action_list):
            if len(speed_list) == 1:
                speed_list = speed_list * len(action_list)
            else:
                return None, f"Error: Number of speeds ({len(speed_list)}) must match number of actions ({len(action_list)})"
        
        for action in action_list:
            if action not in ['w', 'a', 's', 'd']:
                return None, f"Error: Invalid action '{action}'. Use only w, a, s, d"
        
        for speed in speed_list:
            if not 0.0 <= speed <= 3.0:
                return None, f"Error: Speed {speed} out of range. Use values between 0.0 and 3.0"
        
        progress(0.1, desc="Processing image...")
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            input_image.save(tmp_file.name)
            image_path = tmp_file.name
        
        closest_size = (704, 1216)
        ref_image_transform = transforms.Compose([
            CropResize(closest_size),
            transforms.CenterCrop(closest_size),
            transforms.ToTensor(), 
            transforms.Normalize([0.5], [0.5])
        ])
        
        raw_ref_image = Image.open(image_path).convert('RGB')
        ref_image_pixel_values = ref_image_transform(raw_ref_image)
        ref_image_pixel_values = ref_image_pixel_values.unsqueeze(0).unsqueeze(2).to(device)
        
        progress(0.2, desc="Encoding image...")
        
        with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=True):
            if args.cpu_offload:
                hunyuan_video_sampler.vae.quant_conv.to('cuda')
                hunyuan_video_sampler.vae.encoder.to('cuda')
            
            hunyuan_video_sampler.pipeline.vae.enable_tiling()
            
            raw_last_latents = hunyuan_video_sampler.vae.encode(
                ref_image_pixel_values
            ).latent_dist.sample().to(dtype=torch.float16)
            raw_last_latents.mul_(hunyuan_video_sampler.vae.config.scaling_factor)
            raw_ref_latents = raw_last_latents.clone()
            
            hunyuan_video_sampler.pipeline.vae.disable_tiling()
            if args.cpu_offload:
                hunyuan_video_sampler.vae.quant_conv.to('cpu')
                hunyuan_video_sampler.vae.encoder.to('cpu')
        
        ref_images = [raw_ref_image]
        last_latents = raw_last_latents
        ref_latents = raw_ref_latents
        
        progress(0.3, desc="Starting video generation...")
        
        if seed is None or seed == -1:
            seed = random.randint(0, 1_000_000)
        
        all_samples = []
        
        for idx, (action_id, action_speed) in enumerate(zip(action_list, speed_list)):
            is_image = (idx == 0)
            
            progress(0.3 + (0.6 * idx / len(action_list)), 
                    desc=f"Generating segment {idx+1}/{len(action_list)} (action: {action_id})")
            
            outputs = hunyuan_video_sampler.predict(
                prompt=prompt,
                action_id=action_id,
                action_speed=action_speed,                    
                is_image=is_image,
                size=(704, 1216),
                seed=seed,
                last_latents=last_latents,
                ref_latents=ref_latents,
                video_length=args.sample_n_frames,
                guidance_scale=cfg_scale,
                num_images_per_prompt=1,
                negative_prompt=negative_prompt,
                infer_steps=num_inference_steps,
                flow_shift=args.flow_shift_eval_video,
                use_linear_quadratic_schedule=args.use_linear_quadratic_schedule,
                linear_schedule_end=args.linear_schedule_end,
                use_deepcache=args.use_deepcache,
                cpu_offload=args.cpu_offload,
                ref_images=ref_images,
                output_dir=None,
                return_latents=True,
                use_sage=args.use_sage,
            )
            
            ref_latents = outputs["ref_latents"]
            last_latents = outputs["last_latents"]
            
            sub_samples = outputs['samples'][0]
            all_samples.append(sub_samples)
        
        progress(0.9, desc="Finalizing video...")
        
        if len(all_samples) > 0:
            out_cat = torch.cat(all_samples, dim=2)
        else:
            out_cat = all_samples[0]
        
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_video:
            output_path = tmp_video.name
        
        save_videos_grid(out_cat, output_path, n_rows=1, fps=25)
        
        if os.path.exists(image_path):
            os.remove(image_path)
        
        progress(1.0, desc="Complete!")
        return output_path, "Video generated successfully!"
        
    except Exception as e:
        logger.error(f"Error generating video: {e}")
        return None, f"Error: {str(e)}"

with gr.Blocks(title="Hunyuan-GameCraft") as demo:
    gr.Markdown("""
    # 🎮 Hunyuan-GameCraft Video Generation
    
    Generate interactive game-style videos from a single image using keyboard actions (W/A/S/D).
    Using the **distilled model** for faster generation (8 inference steps).
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(
                label="Input Image",
                type="pil",
                height=400
            )
            
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="Describe the scene...",
                value="A charming medieval village with cobblestone streets, thatched-roof houses, and vibrant flower gardens under a bright blue sky.",
                lines=3
            )
            
            with gr.Accordion("Action Controls", open=True):
                action_sequence = gr.Textbox(
                    label="Action Sequence (comma-separated)",
                    placeholder="w, a, s, d",
                    value="w, s, d, a",
                    info="Use w (forward), a (left), s (backward), d (right)"
                )
                
                action_speeds = gr.Textbox(
                    label="Action Speeds (comma-separated)",
                    placeholder="0.2, 0.2, 0.2, 0.2",
                    value="0.2, 0.2, 0.2, 0.2",
                    info="Speed for each action (0.0 to 3.0). Single value applies to all."
                )
            
            with gr.Accordion("Advanced Settings", open=False):
                negative_prompt = gr.Textbox(
                    label="Negative Prompt",
                    value="overexposed, low quality, deformation, a poor composition, bad hands, bad teeth, bad eyes, bad limbs, distortion, blurring, text, subtitles, static, picture, black border.",
                    lines=2
                )
                
                seed = gr.Number(
                    label="Seed",
                    value=-1,
                    precision=0,
                    info="Set to -1 for random seed"
                )
                
                cfg_scale = gr.Slider(
                    label="CFG Scale",
                    minimum=0.5,
                    maximum=3.0,
                    value=1.0,
                    step=0.1,
                    info="Classifier-free guidance scale (1.0 for distilled model)"
                )
                
                num_inference_steps = gr.Slider(
                    label="Inference Steps",
                    minimum=4,
                    maximum=20,
                    value=8,
                    step=1,
                    info="Number of denoising steps (8 for distilled model)"
                )
            
            generate_btn = gr.Button("Generate Video", variant="primary")
        
        with gr.Column(scale=1):
            output_video = gr.Video(
                label="Generated Video",
                height=400
            )
            status_text = gr.Textbox(
                label="Status",
                interactive=False
            )
    
    gr.Markdown("""
    ### Tips:
    - Each action generates 33 frames (1.3 seconds at 25 FPS)
    - The distilled model is optimized for speed with 8 inference steps
    - Use FP8 optimization for better memory efficiency
    - Minimum GPU memory: 24GB VRAM
    """)
    
    generate_btn.click(
        fn=generate_video,
        inputs=[
            input_image,
            prompt,
            action_sequence,
            action_speeds,
            negative_prompt,
            seed,
            cfg_scale,
            num_inference_steps
        ],
        outputs=[output_video, status_text]
    )
    
    gr.Examples(
        examples=[
            [
                "asset/village.png",
                "A charming medieval village with cobblestone streets, thatched-roof houses, and vibrant flower gardens under a bright blue sky.",
                "w, a, d, s",
                "0.2, 0.2, 0.2, 0.2"
            ]
        ],
        inputs=[input_image, prompt, action_sequence, action_speeds],
        label="Example"
    )

if __name__ == "__main__":
    demo.launch(share=True)