[](#spaces-zerogpu-dynamic-gpu-allocation-for-spaces)Spaces ZeroGPU: Dynamic GPU Allocation for Spaces
======================================================================================================

![ZeroGPU schema](https://cdn-uploads.huggingface.co/production/uploads/5f17f0a0925b9863e28ad517/naVZI-v41zNxmGlhEhGDJ.gif)

ZeroGPU is a shared infrastructure that optimizes GPU usage for AI models and demos on Hugging Face Spaces. It dynamically allocates and releases NVIDIA H200 GPUs as needed, offering:

1.  **Free GPU Access**: Enables cost-effective GPU usage for Spaces.
2.  **Multi-GPU Support**: Allows Spaces to leverage multiple GPUs concurrently on a single application.

Unlike traditional single-GPU allocations, ZeroGPU’s efficient system lowers barriers for developers, researchers, and organizations to deploy AI models by maximizing resource utilization and power efficiency.

[](#using-and-hosting-zerogpu-spaces)Using and hosting ZeroGPU Spaces
---------------------------------------------------------------------

*   **Using existing ZeroGPU Spaces**
    *   ZeroGPU Spaces are available to use for free to all users. (Visit [the curated list](https://huggingface.co/spaces/enzostvs/zero-gpu-spaces)).
    *   [PRO users](https://huggingface.co/subscribe/pro) get x5 more daily usage quota and highest priority in GPU queues when using any ZeroGPU Spaces.
*   **Hosting your own ZeroGPU Spaces**
    *   Personal accounts: [Subscribe to PRO](https://huggingface.co/settings/billing/subscription) to access ZeroGPU in the hardware options when creating a new Gradio SDK Space.
    *   Organizations: [Subscribe to the Enterprise Hub](https://huggingface.co/enterprise) to enable ZeroGPU Spaces for all organization members.

[](#technical-specifications)Technical Specifications
-----------------------------------------------------

*   **GPU Type**: Nvidia H200 slice
*   **Available VRAM**: 70GB per workload

[](#compatibility)Compatibility
-------------------------------

ZeroGPU Spaces are designed to be compatible with most PyTorch-based GPU Spaces. While compatibility is enhanced for high-level Hugging Face libraries like `transformers` and `diffusers`, users should be aware that:

*   Currently, ZeroGPU Spaces are exclusively compatible with the **Gradio SDK**.
*   ZeroGPU Spaces may have limited compatibility compared to standard GPU Spaces.
*   Unexpected issues may arise in some scenarios.

### [](#supported-versions)Supported Versions

*   Gradio: 4+
*   PyTorch: 2.1.2, 2.2.2, 2.4.0, 2.5.1 (Note: 2.3.x is not supported due to a [PyTorch bug](https://github.com/pytorch/pytorch/issues/122085))
*   Python: 3.10.13

[](#getting-started-with-zerogpu)Getting started with ZeroGPU
-------------------------------------------------------------

To utilize ZeroGPU in your Space, follow these steps:

1.  Make sure the ZeroGPU hardware is selected in your Space settings.
2.  Import the `spaces` module.
3.  Decorate GPU-dependent functions with `@spaces.GPU`.

This decoration process allows the Space to request a GPU when the function is called and release it upon completion.

### [](#example-usage)Example Usage

Copied

import spaces
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from\_pretrained(...)
pipe.to('cuda')

@spaces.GPU
def generate(prompt):
    return pipe(prompt).images

gr.Interface(
    fn=generate,
    inputs=gr.Text(),
    outputs=gr.Gallery(),
).launch()

Note: The `@spaces.GPU` decorator is designed to be effect-free in non-ZeroGPU environments, ensuring compatibility across different setups.

[](#duration-management)Duration Management
-------------------------------------------

For functions expected to exceed the default 60-second of GPU runtime, you can specify a custom duration:

Copied

@spaces.GPU(duration=120)
def generate(prompt):
   return pipe(prompt).images

This sets the maximum function runtime to 120 seconds. Specifying shorter durations for quicker functions will improve queue priority for Space visitors.

[](#hosting-limitations)Hosting Limitations
-------------------------------------------

*   **Personal accounts ([PRO subscribers](https://huggingface.co/subscribe/pro))**: Maximum of 10 ZeroGPU Spaces.
*   **Organization accounts ([Enterprise Hub](https://huggingface.co/enterprise))**: Maximum of 50 ZeroGPU Spaces.

By leveraging ZeroGPU, developers can create more efficient and scalable Spaces, maximizing GPU utilization while minimizing costs.

[](#feedback)Feedback
---------------------

You can share your feedback on Spaces ZeroGPU directly on the HF Hub: [https://huggingface.co/spaces/zero-gpu-explorers/README/discussions](https://huggingface.co/spaces/zero-gpu-explorers/README/discussions)

[< \> Update on GitHub](https://github.com/huggingface/hub-docs/blob/main/docs/hub/spaces-zerogpu.md)