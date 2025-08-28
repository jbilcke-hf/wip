HTML conversions [sometimes display errors](https://info.dev.arxiv.org/about/accessibility_html_error_messages.html) due to content that did not convert correctly from the source. This paper uses the following packages that are not yet supported by the HTML conversion tool. Feedback on these issues are not necessary; they are known and are being worked on.

*   failed: epic

Authors: achieve the best HTML results from your LaTeX submissions by following these [best practices](https://info.arxiv.org/help/submit_latex_best_practices.html).

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2506.17201v1 \[cs.CV\] 20 Jun 2025

Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation  
with Hybrid History Condition
=================================================================================================

Report issue for preceding element

Jiaqi Li1,2111Equal Contribution. 222Work is done during the internship at Tencent Hunyuan.  Junshu Tang1111Equal Contribution.  Zhiyong Xu1  Longhuang Wu1  
 Yuan Zhou1  Shuai Shao1  Tianbao Yu1  Zhiguo Cao2  Qinglin Lu1333Corresponding author.  
  
1 Tencent Hunyuan  2 Huazhong University of Science and Technology  
[https://hunyuan-gamecraft.github.io/](https://hunyuan-gamecraft.github.io/)

Report issue for preceding element

###### Abstract

Report issue for preceding element

Recent advances in diffusion-based and controllable video generation have enabled high-quality and temporally coherent video synthesis, laying the groundwork for immersive interactive gaming experiences. However, current methods face limitations in dynamics, generality, long-term consistency, and efficiency, which limit the ability to create various gameplay videos. To address these gaps, we introduce Hunyuan-GameCraft, a novel framework for high-dynamic interactive video generation in game environments. To achieve fine-grained action control, we unify standard keyboard and mouse inputs into a shared camera representation space, facilitating smooth interpolation between various camera and movement operations. Then we propose a hybrid history-conditioned training strategy that extends video sequences autoregressively while preserving game scene information. Additionally, to enhance inference efficiency and playability, we achieve model distillation to reduce computational overhead while maintaining consistency across long temporal sequences, making it suitable for real-time deployment in complex interactive environments. The model is trained on a large-scale dataset comprising over one million gameplay recordings across over 100 AAA games, ensuring broad coverage and diversity, then fine-tuned on a carefully annotated synthetic dataset to enhance precision and control. The curated game scene data significantly improves the visual fidelity, realism and action controllability. Extensive experiments demonstrate that Hunyuan-GameCraft significantly outperforms existing models, advancing the realism and playability of interactive game video generation.

Report issue for preceding element

![Refer to caption](x1.png)

Figure 2: Additional results by Hunyuan-GameCraft on multi-actions control. In our case, blue-lit keys indicate key presses. W, A, S, D represent transition movement and ↑, ←, ↓, → denote changes in view angles.

Report issue for preceding element

![[Uncaptioned image]](x2.png)

Figure 1: _Hunyuan-GameCraft_ can create high-dynamic interactive game video content from a single image and corresponding prompt. We simulate a series of action signals. The left and right frames depict key moments from game video sequences generated in response to different inputs. Hunyuan-GameCraft can accurately produce content aligned with each interaction, supports long-term video generation with temporal and 3D consistency, and effectively preserves historical scene information throughout the sequence. In this case, W, A, S, D represent transition movement and ↑, ←, ↓, → denote changes in view angles.

Report issue for preceding element

1 Introduction
--------------

Report issue for preceding element

The rapid progress in generative modeling has transformed numerous fields, including entertainment and education, and beyond, fueling growing interest in high-dynamic, immersive, generative gaming experiences. Recent breakthroughs in diffusion-based video generation \[[1](https://arxiv.org/html/2506.17201v1#bib.bib1), [2](https://arxiv.org/html/2506.17201v1#bib.bib2), [31](https://arxiv.org/html/2506.17201v1#bib.bib31), [6](https://arxiv.org/html/2506.17201v1#bib.bib6), [19](https://arxiv.org/html/2506.17201v1#bib.bib19)\] have significantly advanced dynamic content creation, enabling high-quality, temporally coherent video synthesis. Moreover, advances in controllable video generation have introduced novel creative forms of dynamic, user-driven video production, expanding the boundaries of interactive digital experiences.

Report issue for preceding element

GameNGen \[[26](https://arxiv.org/html/2506.17201v1#bib.bib26)\]

GameGenX \[[5](https://arxiv.org/html/2506.17201v1#bib.bib5)\]

Oasis \[[8](https://arxiv.org/html/2506.17201v1#bib.bib8)\]

Matrix \[[10](https://arxiv.org/html/2506.17201v1#bib.bib10)\]

Genie 2 \[[22](https://arxiv.org/html/2506.17201v1#bib.bib22)\]

GameFactory \[[34](https://arxiv.org/html/2506.17201v1#bib.bib34)\]

Matrix-Game \[[36](https://arxiv.org/html/2506.17201v1#bib.bib36)\]

Hunyuan-GameCraft

Game Sources

DOOM

AAA Games

Minecraft

AAA Games

Unknown

Minecraft

Minecraft

AAA Games

Resolution

240240240240p

720720720720p

640×360640360640\\times 360640 × 360

720720720720p

720720720720p

640×360640360640\\times 360640 × 360

720720720720p

720720720720p

Action Space

Key

Instruction

Key + Mouse

4 Keys

Key+Mouse

7 Keys+Mouse

7 Keys+Mouse

Continous

Scene Generalizable

✗

✗

✗

✔

✔

✔

✔

✔

Scene Dynamic

✔

✔

✗

✔

✗

✔

✗

✔

Scene Memory

✗

✗

✗

✗

✗

✗

✔

✔

Table 1: Comparison with recent interactive game models. Hunyuan-GameCraft serves as a model capable of generating infinitely long game videos conditioned on continuous action signals, while maintaining strong generalization, high temporal dynamics, and effective preservation of historical scene information.

Report issue for preceding element

Recent advances in visual generation have explored spatial intelligence, the analysis and creation of coherent spatial scenes. These models focus on interactivity and exploration, enabling dynamic 3D/4D environments with spatiotemporal coherence. For example, WorldLabs \[[32](https://arxiv.org/html/2506.17201v1#bib.bib32)\] demonstrates the potential for reconstructing high-fidelity 3D environments from static imagery, while Genie 2 \[[22](https://arxiv.org/html/2506.17201v1#bib.bib22)\] introduces latent action modeling to enable physics-consistent interactions over time. Despite these advances, current approaches still struggle with significant limitations in critical areas such as real-time dynamic scene element fidelity, long-sequence consistency, and computational efficiency, limiting their applicability in high-dynamic, playable interactive scenarios. Notably, in game interaction modeling, real-time interactive generation and high dynamicity constitute fundamental components of player experience.

Report issue for preceding element

To address these challenges, we introduce Hunyuan-GameCraft, a novel framework designed for high-dynamic, action-controllable video synthesis in game environments. Built upon a text-to-video foundation model, HunyuanVideo \[[18](https://arxiv.org/html/2506.17201v1#bib.bib18)\], our method enables the generation of temporally coherent and visually rich gameplay footage conditioned on discrete user actions. We unify a broad set of standard keyboard and mouse inputs (e.g., W, A, S, D, arrow keys, Space) into a shared camera representation space, which unified embedding supports smooth interpolation between various camera and movement operations, ensuring physical plausibility while enabling cinematic flexibility in user-driven interactions, for example, speeding up.

Report issue for preceding element

To maintain long-term consistency in interactive game video generation, prior works \[[6](https://arxiv.org/html/2506.17201v1#bib.bib6), [15](https://arxiv.org/html/2506.17201v1#bib.bib15), [20](https://arxiv.org/html/2506.17201v1#bib.bib20)\] have primarily focused on training-free extensions, streaming denoising or last-frame conditioning. However, these approaches often suffer from quality degradation and temporal inconsistency with causal VAEs \[[33](https://arxiv.org/html/2506.17201v1#bib.bib33)\]. We propose a novel hybrid history-conditioned training strategy that autoregressively extends sequences while preserving scene information, using historical context integration and a mask indicator to address error accumulation in autoregressive generation. Moreover, to improve inference efficiency and playability, we implement the model distillation acceleration strategy \[[28](https://arxiv.org/html/2506.17201v1#bib.bib28)\], which reduces computational overhead while maintaining consistency across long temporal sequences, making our framework suitable for real-time deployment in complex interactive environments.

Report issue for preceding element

We evaluate our Hunyuan-GameCraft on both curated game scenes and general styles, obtaining a significant lead over current models. In summary, our contributions are:

Report issue for preceding element

*   •
    
    We propose Hunyuan-GameCraft, a novel interactive game video synthesis framework for dynamic content creation in game scenes, enabling users to produce content through customized action input.
    
    Report issue for preceding element
    
*   •
    
    We unify the discrete keyboard/mouse action signals into a shared continuous action space, supporting more complex and fine-grained interactive inputs, such as speed, angle, etc.
    
    Report issue for preceding element
    
*   •
    
    We introduce a novel hybrid history-condition training strategy that maintains long-term spatial and temporal coherency across various action signals.
    
    Report issue for preceding element
    
*   •
    
    We implement model distillation to speed up the inference speed which improves the interaction experience.
    
    Report issue for preceding element
    

2 Related Work
--------------

Report issue for preceding element

### 2.1 Interactive Game Scene World Model

Report issue for preceding element

Recent research has gradually focused on incorporating video generation models to enhance dynamic prediction and interaction capabilities in game scenes. We conduct a survey on recent works, as shown in Tab. [1](https://arxiv.org/html/2506.17201v1#S1.T1 "Table 1 ‣ 1 Introduction ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"). WorldDreamer \[[30](https://arxiv.org/html/2506.17201v1#bib.bib30)\] proposes constructing a general world model by predicting masked tokens, which supports multi-modal interaction and is applicable to natural scenes and driving environments. GameGen-X \[[5](https://arxiv.org/html/2506.17201v1#bib.bib5)\], a diffusion Transformer model for open-world games, integrates multi-modal control signals to enable interactive video generation. The Genie series \[[22](https://arxiv.org/html/2506.17201v1#bib.bib22)\] generates 3D worlds from single-image prompts, while the Matrix model leverages game data with a streaming generation format to infinitely produce content through user actions.

Report issue for preceding element

### 2.2 Camera-Controlled Video Generation

Report issue for preceding element

Motionctrl \[[31](https://arxiv.org/html/2506.17201v1#bib.bib31)\] uses a unified and flexible motion controller designed for video generation, which independently controls the movement of video cameras and objects to achieve precise control over the motion perspectives in generated videos. CameraCtrl \[[13](https://arxiv.org/html/2506.17201v1#bib.bib13)\] employs Plücker embedding as the primary representation for camera parameters, training only the camera encoder and linear layers to achieve camera control. Furthermore, the recent approach CameraCtrl II \[[14](https://arxiv.org/html/2506.17201v1#bib.bib14)\] constructs a high-dynamics dataset with camera parameter annotations for training, and designs a lightweight camera injection module and training scheme to preserve the dynamics of pretrained models.

Report issue for preceding element

### 2.3 Long Video Extension

Report issue for preceding element

Generating long videos poses challenges in maintaining temporal consistency and high visual quality over extended durations. Early methods used GAN to explore long video generation \[[23](https://arxiv.org/html/2506.17201v1#bib.bib23)\]. With the popularity of diffusion, some methods began to try to solve the problem using diffusion model. StreamingT2V \[[15](https://arxiv.org/html/2506.17201v1#bib.bib15)\] introduces short-term and long-term memory blocks with randomized blending to ensure consistency and scalability in text-to-video generation. In addition, some methods also explore different paradigms, such as next frame prediction \[[11](https://arxiv.org/html/2506.17201v1#bib.bib11), [12](https://arxiv.org/html/2506.17201v1#bib.bib12)\], combining next-token and full-sequence diffusion (DiffusionForcing) \[[6](https://arxiv.org/html/2506.17201v1#bib.bib6)\] and test-time training  \[[7](https://arxiv.org/html/2506.17201v1#bib.bib7)\]. Compared with previous methods, we propose a novel hybrid history-conditioned training strategy that extends video sequences in an autoregressive way while effectively preserving game scene information, under a diffusion paradigm.

Report issue for preceding element

3 Dataset Construction
----------------------

Report issue for preceding element

### 3.1 Game Scene Data Curation

Report issue for preceding element

We curate over 100 AAA titles, such as Assassin’s Creed, Red Dead Redemption, and Cyberpunk 2077, to create a diverse dataset with high-resolution graphics and complex interactions. As shown in Fig [3](https://arxiv.org/html/2506.17201v1#S3.F3 "Figure 3 ‣ 3.1 Game Scene Data Curation ‣ 3 Dataset Construction ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"), our end-to-end data processing framework comprises four stages that addresses annotated gameplay data scarcity while establishing new standards for camera-controlled video generation.

Report issue for preceding element

![Refer to caption](x3.png)

Figure 3: Dataset Construction Pipeline. It consists of four pre-processing steps: Scene and Action-aware Data Partition, Data Filtering, Interaction Annotation and structured captioning.

Report issue for preceding element

![Refer to caption](x4.png)

Figure 4: Overall architecture of Hunyuan-GameCraft. Given a reference image and the corresponding prompt, the keyboard or mouse signal, we transform these options to the continuous camera space. Then we design a light-weight action encoder to encode the input camera trajectory. The action and image features are added after patchify. For long video extension, we design a variable mask indicator, where 1 and 0 indicate history frames and predicted frames, respectively.

Report issue for preceding element

Scene and Action-aware Data Partition. We introduce a two-tier video partitioning approach (scene-level and action-level). Using PySceneDetect \[[4](https://arxiv.org/html/2506.17201v1#bib.bib4)\], we segment 2-3 hour gameplay recordings into 6-second coherent clips (1M+ clips at 1080p). RAFT \[[24](https://arxiv.org/html/2506.17201v1#bib.bib24)\] computes optical flow gradients to detect action boundaries (e.g., rapid aiming), enabling precise alignment for video generation training.

Report issue for preceding element

Data Filtering. To enhance synthesis quality, we employ quality assessment \[[17](https://arxiv.org/html/2506.17201v1#bib.bib17)\] to remove low-fidelity clips, apply OpenCV \[[3](https://arxiv.org/html/2506.17201v1#bib.bib3)\]\-based luminance filtering to eliminate dark scenes, and utilize VLM \[[29](https://arxiv.org/html/2506.17201v1#bib.bib29)\]\-based gradient detection for comprehensive data filtering from multiple perspectives.

Report issue for preceding element

Interaction Annotation. We reconstruct 6-DoF camera trajectories using Monst3R \[[35](https://arxiv.org/html/2506.17201v1#bib.bib35)\] to model viewpoint dynamics (translational/rotational motion). Each clip is annotated with frame-by-frame position/orientation data, which is essential for video generation training.

Report issue for preceding element

Structured Captioning. For video captioning, we implement a hierarchical strategy using game-specific VLMs \[[29](https://arxiv.org/html/2506.17201v1#bib.bib29)\] to generate: 1) concise 30-character summaries and 2) detailed 100+ character descriptions. These captions are randomly sampled during training.

Report issue for preceding element

### 3.2 Synthetic Data Construction

Report issue for preceding element

We rendered about 3,000 high-quality motion sequences from curated 3D assets, systematically sampling multiple starting positions to generate diverse camera trajectories (translations, rotations, and composites) re-rendered at varying speeds. Our multi-phase training strategy demonstrates that introducing high-precision rendered sequences significantly improves motion prediction accuracy and temporal coherence during viewpoint transitions, while establishing essential geometric priors for complex camera movements that complement real-world samples.

Report issue for preceding element

### 3.3 Distribution Balancing Strategy

Report issue for preceding element

Leveraging a hybrid training framework with combined datasets, we addressed inherent forward-motion bias in camera trajectories via a two-pronged strategy: 1) stratified sampling of start-end vectors to balance directional representation in 3D space and 2) temporal inversion augmentation to double backward motion coverage. Combined with late-stage fine-tuning using uniformly distributed rendered data, these techniques enhanced control signal generalization, training stability, and cross-directional performance consistency.

Report issue for preceding element

4 Method
--------

Report issue for preceding element

In this paper, we propose Hunyuan-GameCraft, a high-dynamic interactive game video generation model based on a previously open-sourced MM-DiT \[[9](https://arxiv.org/html/2506.17201v1#bib.bib9)\] based text-to-video model, HunyuanVideo \[[18](https://arxiv.org/html/2506.17201v1#bib.bib18)\]. The overall framework is shown in Fig [4](https://arxiv.org/html/2506.17201v1#S3.F4 "Figure 4 ‣ 3.1 Game Scene Data Curation ‣ 3 Dataset Construction ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"). To achieve fine-grained controllable game video synthesis with temporal coherence, we first unify diverse common keyboard/mouse options in games (W, A, S, D, ↑, ←, ↓, →, Space, etc.) into a shared camera representation space (Sec. [4.1](https://arxiv.org/html/2506.17201v1#S4.SS1 "4.1 Continuous Action Space and Injection ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition")) and design a light-weight action encoder to encode the camera trajectory(Sec. [4.1](https://arxiv.org/html/2506.17201v1#S4.SS1 "4.1 Continuous Action Space and Injection ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition")). Then, we propose a hybrid history-conditioned video extension approach that autoregressively denoise new noisy latent conditioned on historical denoised chunks (Sec. [4.2](https://arxiv.org/html/2506.17201v1#S4.SS2 "4.2 Hybrid history conditioned Long Video Extension ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition")). Finally, to accelerate the inference speed and improve the interaction experience, we implement the model distillation, based on Phased Consistency Model \[[28](https://arxiv.org/html/2506.17201v1#bib.bib28)\]. This distillation achieves a 10–20× acceleration in inference speed, reducing latency to less than 5s per action (Sec. [4.3](https://arxiv.org/html/2506.17201v1#S4.SS3 "4.3 Accelerated Generative Interaction ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition")).

Report issue for preceding element

### 4.1 Continuous Action Space and Injection

Report issue for preceding element

To achieve fine-grained control over the generated content for enhanced interactive effects, we define a subset action space 𝒜𝒜\\mathcal{A}caligraphic\_A within the camera parameter 𝒞⊆ℝn𝒞superscriptℝ𝑛\\mathcal{C}\\subseteq\\mathbb{R}^{n}caligraphic\_C ⊆ blackboard\_R start\_POSTSUPERSCRIPT italic\_n end\_POSTSUPERSCRIPT dedicated to continuous and intuitive motion control injection:

Report issue for preceding element

𝒜:\={𝐚\=(𝐝trans,𝐝rot,α,β)|𝐝trans∈𝕊2,𝐝rot∈𝕊2,α∈\[0,vmax\],β∈\[0,ωmax\]}.\\mathcal{A}\\mathrel{\\mathop{:}}\\mathrel{\\mkern-1.2mu}=\\Bigg{\\{}\\mathbf{a}=\\Big% {(}\\mathbf{d}\_{\\text{trans}},\\mathbf{d}\_{\\text{rot}},\\alpha,\\beta\\Big{)}\\;% \\Bigg{|}\\;\\begin{aligned} &\\mathbf{d}\_{\\text{trans}}\\in\\mathbb{S}^{2},\\quad% \\mathbf{d}\_{\\text{rot}}\\in\\mathbb{S}^{2},\\\\ &\\alpha\\in\[0,v\_{\\text{max}}\],\\quad\\beta\\in\[0,\\omega\_{\\text{max}}\]\\end{aligned}% \\Bigg{\\}}\\!.caligraphic\_A : = { bold\_a = ( bold\_d start\_POSTSUBSCRIPT trans end\_POSTSUBSCRIPT , bold\_d start\_POSTSUBSCRIPT rot end\_POSTSUBSCRIPT , italic\_α , italic\_β ) | start\_ROW start\_CELL end\_CELL start\_CELL bold\_d start\_POSTSUBSCRIPT trans end\_POSTSUBSCRIPT ∈ blackboard\_S start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT , bold\_d start\_POSTSUBSCRIPT rot end\_POSTSUBSCRIPT ∈ blackboard\_S start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT , end\_CELL end\_ROW start\_ROW start\_CELL end\_CELL start\_CELL italic\_α ∈ \[ 0 , italic\_v start\_POSTSUBSCRIPT max end\_POSTSUBSCRIPT \] , italic\_β ∈ \[ 0 , italic\_ω start\_POSTSUBSCRIPT max end\_POSTSUBSCRIPT \] end\_CELL end\_ROW } .

(1)

𝐝transsubscript𝐝trans\\mathbf{d}\_{\\text{trans}}bold\_d start\_POSTSUBSCRIPT trans end\_POSTSUBSCRIPT and 𝐝rotsubscript𝐝rot\\mathbf{d}\_{\\text{rot}}bold\_d start\_POSTSUBSCRIPT rot end\_POSTSUBSCRIPT are unit vectors defining the translation and rotation direction on the 2-sphere space 𝕊2superscript𝕊2\\mathbb{S}^{2}blackboard\_S start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT, respectively. Scalars α𝛼\\alphaitalic\_α and β𝛽\\betaitalic\_β are used for controlling translation and rotation speed, bounded by maximum velocity vmaxsubscript𝑣maxv\_{\\text{max}}italic\_v start\_POSTSUBSCRIPT max end\_POSTSUBSCRIPT and ωmaxsubscript𝜔max\\omega\_{\\text{max}}italic\_ω start\_POSTSUBSCRIPT max end\_POSTSUBSCRIPT. Specifically, they are the differential modulus of relative velocity and angle during frame-by-frame motion.

Report issue for preceding element

Building upon prior knowledge of gaming scenarios and general camera control conventions, we eliminate the degree of freedom in the roll dimension while incorporating velocity control. This design enables fine-grained trajectory manipulation that aligns with user input habits. Furthermore, this representation can be seamlessly converted into standard camera trajectory parameters and Plücker embeddings. Similar with previous camera-controlled video generation arts, we design a light-weight camera information encoding network that aligns Plücker embeddings with video latents. Unlike previous approaches that employ cascaded residual blocks or transformer blocks to construct Plücker embedding encoders, our encoding network consists solely of a limited number of convolutional layers for spatial downsampling and pooling layers for temporal downsampling. A learnable scaling coefficient is incorporated to automatically optimize the relative weighting during token-wise addition, ensuring stable and adaptive feature fusion.

Report issue for preceding element

Then we adopted the token addition strategy to inject camera pose control into the MM-DiT backbone. Dual lightweight learnable tokenizers are used to achieve efficient feature fusion between video and action tokens, enabling effective interactive control. Additional ablation studies and comparative analyses are detailed in Sec. [5.3](https://arxiv.org/html/2506.17201v1#S5.SS3 "5.3 Ablation Study ‣ 5 Experiment ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition").

Report issue for preceding element

Leveraging the robust multimodal fusion and interaction capabilities of MM-DiT backbone, our method achieves state-of-the-art interactive performance despite significant encoder parameter reduction, while maintaining negligible additional computational overhead.

Report issue for preceding element

![Refer to caption](x5.png)

Figure 5: Comparison of different autoregressive long video extension schemes. (i) Training-free inference. (ii) Streaming generation. (iii) Hybrid history condition proposed in this paper.

Report issue for preceding element

### 4.2 Hybrid history conditioned Long Video Extension

Report issue for preceding element

Consistently generating long or potentially infinite-length videos remains a fundamental challenge in interactive video generation. As shown in Fig [5](https://arxiv.org/html/2506.17201v1#S4.F5 "Figure 5 ‣ 4.1 Continuous Action Space and Injection ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"), current video extrapolation approaches can be categorized into three main paradigms: (1) training-free inference from single images, (2) rolling streaming generation with non-uniform noise windows, and (3) chunk-wise extension using historical segments. As shown in Fig [6](https://arxiv.org/html/2506.17201v1#S4.F6 "Figure 6 ‣ 4.2 Hybrid history conditioned Long Video Extension ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition")(a), training-free methods lack insufficient historical context during extrapolation, leading to inconsistent generation quality and frequent scene collapse in iterative generation. The streaming approach shows significant architectural incompatibility with our image-to-video foundation model, where the causal VAE’s uneven encoding of initial versus subsequent frames fundamentally limits efficiency and scalability. To address these limitations, we investigate hybrid-conditioned autoregressive video extension, where multiple guidance conditions are mixed during training to achieve high consistency, fidelity, and compatibility.

Report issue for preceding element

As illustrated in Fig. [5](https://arxiv.org/html/2506.17201v1#S4.F5 "Figure 5 ‣ 4.1 Continuous Action Space and Injection ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"), we define each autoregressive step as a chunk latent denoising process guided by head latent and interactive signals. The chunk latent, serving as a global representation by causal VAE, is subsequently decoded into a temporally consistent video segment that precisely corresponds to the input action. Head condition can be different forms, including (i) a single image frame latent, (ii) the final latent from the previous clip, or (iii) a longer latent clip segment. Hunyuan-GameCraft achieves high-fidelity denoising of chunk latents through concatenation at both condition and noise levels. An additional binary mask assigns value 1 to head latent regions and 0 to chunk segments, enabling precise control over the denoising part. Within the noise schedule, the preceding head condition remains noise-free as clean latent, which guides subsequent noisy chunk latents through flow matching to progressively denoise and generate new clean video clips for the next denoising iteration.

Report issue for preceding element

We conduct extensive experiments on the three aforementioned head conditions, as detailed in Fig [6](https://arxiv.org/html/2506.17201v1#S4.F6 "Figure 6 ‣ 4.2 Hybrid history conditioned Long Video Extension ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"). The results demonstrate that autoregressive video extension shows improved consistency and generation quality when the head condition contains more information, while interactive performance decreases accordingly. This trade-off occurs because the training data comes from segmented long videos, where subsequent clips typically maintain motion continuity with preceding ones. As a result, stronger historical priors naturally couple the predicted next clip with the given history, which limits responsiveness to changed action inputs. However, richer reference information simultaneously enhances temporal coherence and generation fidelity.

Report issue for preceding element

![Refer to caption](x6.png)

Figure 6: Analysis on different video extension schemes. Baseline (a) is a naive solution using training-free inference from single images, and it will lead to obvious quality collapse. Using history clip condition (b) will result in control degradation. With our proposed hybrid history condition (c), the model can achieve accurate action control and history preservation (see red box). W, A, S denote moving forward, left and backward.

Report issue for preceding element

![Refer to caption](x7.png)

Figure 7: Qualitative comparison on the test benchmark. We compare with Matrix-Game on multi-actions control accuracy and long-term consistency. And we compare with other camera-controlled video generation arts CameraCtrl, MotionCtrl and WanX-Cam on single-action control accuracy. In our case, blue-lit keys indicate key presses. W, A, S, D represent transition movement and ↑, ←, ↓, → denote changes in view angles.

Report issue for preceding element

To address this trade-off, in addition to constructing training samples and applying stratified sampling, hybrid-conditioned training is proposed to mix all three extension modes during training to jointly optimize both interactive capability and generation consistency. This hybrid approach achieves state-of-the-art performance by reasonably balancing these competing objectives. The hybrid-conditioned paradigm also provides practical deployment benefits. It successfully integrates two separate tasks (initial frame generation and video extension) into a unified model. This integration enables seamless transitions between generation modes without requiring architectural modifications, making the solution particularly valuable for real-world applications that demand both flexible control and coherent long-term video generation.

Report issue for preceding element

### 4.3 Accelerated Generative Interaction

Report issue for preceding element

To enhance the gameplay experience and enable accelerated interaction with the generated game videos, we further extend our approach by integrating acceleration techniques. A promising direction involves combining our core framework with Consistency Models \[[21](https://arxiv.org/html/2506.17201v1#bib.bib21)\], a state-of-the-art method for accelerating diffusion-based generation. In particular, we adopt the Phased Consistency Model (PCM) \[[28](https://arxiv.org/html/2506.17201v1#bib.bib28)\], which distills the original diffusion process and classifier-free guidance into a compact eight-step consistency model. To further reduce computational overhead and improve inference efficiency, we introduce Classifier-Free Guidance Distillation. This approach defines a distillation objective that trains the student model to directly produce guided outputs without relying on external guidance mechanisms, the object function is designed as:

Report issue for preceding element

Lc⁢f⁢g\=𝔼w∼pw,t∼U⁢\[0,1\]⁢\[‖uθ^⁢(zt,t,w,Ts)−uθs⁢(zt,t,w,Ts)‖22\],subscript𝐿𝑐𝑓𝑔subscript𝔼formulae-sequencesimilar-to𝑤subscript𝑝𝑤similar-to𝑡𝑈01delimited-\[\]subscriptsuperscriptnorm^subscript𝑢𝜃subscript𝑧𝑡𝑡𝑤subscript𝑇𝑠superscriptsubscript𝑢𝜃𝑠subscript𝑧𝑡𝑡𝑤subscript𝑇𝑠22\\displaystyle L\_{cfg}=\\mathbb{E}\_{w\\sim p\_{w},t\\sim U\[0,1\]}\[||\\hat{u\_{\\theta}}% (z\_{t},t,w,T\_{s})-u\_{\\theta}^{s}(z\_{t},t,w,T\_{s})||^{2}\_{2}\],italic\_L start\_POSTSUBSCRIPT italic\_c italic\_f italic\_g end\_POSTSUBSCRIPT = blackboard\_E start\_POSTSUBSCRIPT italic\_w ∼ italic\_p start\_POSTSUBSCRIPT italic\_w end\_POSTSUBSCRIPT , italic\_t ∼ italic\_U \[ 0 , 1 \] end\_POSTSUBSCRIPT \[ | | over^ start\_ARG italic\_u start\_POSTSUBSCRIPT italic\_θ end\_POSTSUBSCRIPT end\_ARG ( italic\_z start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT , italic\_t , italic\_w , italic\_T start\_POSTSUBSCRIPT italic\_s end\_POSTSUBSCRIPT ) - italic\_u start\_POSTSUBSCRIPT italic\_θ end\_POSTSUBSCRIPT start\_POSTSUPERSCRIPT italic\_s end\_POSTSUPERSCRIPT ( italic\_z start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT , italic\_t , italic\_w , italic\_T start\_POSTSUBSCRIPT italic\_s end\_POSTSUBSCRIPT ) | | start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT \] ,

(2)

uθ^(zt,t,w,Ts)\=(1+w)u(zt,t,Ts)−wuθ(zt,t,)\\displaystyle\\hat{u\_{\\theta}}(z\_{t},t,w,T\_{s})=(1+w)u\_{(}z\_{t},t,T\_{s})-wu\_{% \\theta}(z\_{t},t,)over^ start\_ARG italic\_u start\_POSTSUBSCRIPT italic\_θ end\_POSTSUBSCRIPT end\_ARG ( italic\_z start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT , italic\_t , italic\_w , italic\_T start\_POSTSUBSCRIPT italic\_s end\_POSTSUBSCRIPT ) = ( 1 + italic\_w ) italic\_u start\_POSTSUBSCRIPT ( end\_POSTSUBSCRIPT italic\_z start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT , italic\_t , italic\_T start\_POSTSUBSCRIPT italic\_s end\_POSTSUBSCRIPT ) - italic\_w italic\_u start\_POSTSUBSCRIPT italic\_θ end\_POSTSUBSCRIPT ( italic\_z start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT , italic\_t , )

where Tssubscript𝑇𝑠T\_{s}italic\_T start\_POSTSUBSCRIPT italic\_s end\_POSTSUBSCRIPT denotes the prompt. Through this integration, we achieve up to a 20× speedup in inference, reaching real-time rendering rates of 6.6 frames per second (FPS), thereby significantly enhancing the interactivity and playability of our system.

Report issue for preceding element

5 Experiment
------------

Report issue for preceding element

### 5.1 Experimental Setup

Report issue for preceding element

Implementation Details. Hunyuan-GameCraft builds upon text-to-video foundation model HunyuanVideo  \[[18](https://arxiv.org/html/2506.17201v1#bib.bib18)\], implementing a latent mask mechanism and hybrid history conditioning to achieve image-to-video generation and long video extension. The experiments employ full-parameter training on 192 NVIDIA H20 GPUs, conducted in two phases with a batch size of 48. The first phase trains the model for 30k iterations at a learning rate of 3×10−53superscript1053\\times 10^{-5}3 × 10 start\_POSTSUPERSCRIPT - 5 end\_POSTSUPERSCRIPT using all collected game data and synthetic data at their original proportions. The second phase introduces data augmentation techniques, as described in Sec. [3](https://arxiv.org/html/2506.17201v1#S3 "3 Dataset Construction ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"), to balance action distributions, while reducing the learning rate to 1×10−51superscript1051\\times 10^{-5}1 × 10 start\_POSTSUPERSCRIPT - 5 end\_POSTSUPERSCRIPT for an additional 20,000 iterations to enhance generation quality and interactive performance. The hybrid history condition maintains specific ratios: 0.70.70.70.7 for single historical clip, 0.050.050.050.05 for multiple historical clips, and 0.250.250.250.25 for single frame. The system operates at 25252525 fps, with each video chunk comprising 33333333\-frame clips at 720p resolution.

Report issue for preceding element

Evaluation Datasets. We curate a test set of 150 diverse images and 12 different action signals, sourced from online repositories, spanning gaming scenarios, stylized artwork, and AI-generated content. This composition facilitates both quantitative and qualitative evaluation of interactive control accuracy and generalization. To demonstrate cross-scenario adaptability, we present exemplar results from diverse contexts.

Report issue for preceding element

Evaluation Metrics. We employ several metrics for comprehensive evaluation to ensure fair comparison. We utilize Fréchet Video Distance(FVD) \[[25](https://arxiv.org/html/2506.17201v1#bib.bib25)\] to evaluate the video realism. Relative pose error (RPE trans and RPE rot) are adopted to evaluate interactive control performance, after applying a Sim3 Umeyama alignment on the reconstructed trajectory of prediction to the ground truth. Following Matrix-Game, we employ Image Quality and Aesthetic scores for visual quality assessment, while utilizing Temporal Consistency to evaluate the visual and cinematographic continuity of generated sequences. For dynamic performance evaluation, we adapt the Dynamic Degree metric from VBench \[[16](https://arxiv.org/html/2506.17201v1#bib.bib16)\], modifying its original binary classification approach to directly report absolute optical flow values as Dynamic Average, enabling a more nuanced, continuous assessment of motion characteristics. Additionally, we incorporate user preference scores obtained from user studies.

Report issue for preceding element

Baselines. We compare our method with four representative baselines, including a current state-of-the-art open-sourced interactive game model, Matrix-Game, and three camera-controlled generation works: CameraCtrl \[[13](https://arxiv.org/html/2506.17201v1#bib.bib13)\], MotionCtrl \[[31](https://arxiv.org/html/2506.17201v1#bib.bib31)\] and WanX-Cam \[[27](https://arxiv.org/html/2506.17201v1#bib.bib27)\]. The CameraCtrl and MotionCtrl employ the image-to-video SVD implementation, while WanX-Cam corresponds to the VideoX-Fun implementation.

Report issue for preceding element

Model

Visual Quality

Temporal

RPE

Infer Speed↑↑\\uparrow↑ (FPS)

FVD↓↓\\downarrow↓

Image Quality↑↑\\uparrow↑

Dynamic Average↑↑\\uparrow↑

Aesthetic↑↑\\uparrow↑

Temporal Consistency↑↑\\uparrow↑

Trans↓↓\\downarrow↓

Rot↓↓\\downarrow↓

CameraCtrl

1580.9

0.66

7.2

0.64

0.92

0.13

0.25

1.75

MotionCtrl

1902.0

0.68

7.8

0.48

0.94

0.17

0.32

0.67

WanX-Cam

1677.6

0.70

17.8

0.67

0.92

0.16

0.36

0.13

Matrix-Game

2260.7

0.72

31.7

0.65

0.94

0.18

0.35

0.06

Ours

1554.2

0.69

67.2

0.67

0.95

0.08

0.20

0.25

Ours + PCM

1883.3

0.67

43.8

0.65

0.93

0.08

0.20

6.6

Table 2: Quantitative comparison with recent related works. ↑↑\\uparrow↑ indicates higher is better, while ↓↓\\downarrow↓ indicates that lower is better. The best result is shown in bold.

Report issue for preceding element

### 5.2 Comparisons with other methods

Report issue for preceding element

Quantitative Comparison. We conduct comprehensive comparisons with Matrix-Game, the current leading open-source game interaction model, under identical gaming scenarios. Despite employing the same base model \[[18](https://arxiv.org/html/2506.17201v1#bib.bib18)\], Hunyuan-GameCraft demonstrates significant improvements across the majority of key metrics, including generation quality, dynamic capability, control accuracy, and temporal consistency as shown in Tab. [2](https://arxiv.org/html/2506.17201v1#S5.T2 "Table 2 ‣ 5.1 Experimental Setup ‣ 5 Experiment ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"). Notably, Hunyuan-GameCraft achieves the best results in dynamic performance compared to Matrix-Game, while simultaneously reducing interaction errors by 55%percent5555\\%55 % in cross-domain tests. These advancements are attributable to our optimized training strategy and conditional injection mechanism, which collectively enable robust interactive generation across both gaming scenarios and diverse artistic styles.

Report issue for preceding element

We also evaluate generation quality and control accuracy on the same test set, with quantitative results presented in Tab. [2](https://arxiv.org/html/2506.17201v1#S5.T2 "Table 2 ‣ 5.1 Experimental Setup ‣ 5 Experiment ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"). Hunyuan-GameCraft demonstrates superior performance compared to other baselines. The results suggest that our action-space formulation captures fundamental principles of camera motion that transcend game scene characteristics. Furthermore, we report the inference speed of each baseline. Our method can achieve nearly real-time inference while slightly damaging the dynamic and visual quality, which is more suitable for game scene interaction.

Report issue for preceding element

Qualitative Comparison. As shown in Fig. [7](https://arxiv.org/html/2506.17201v1#S4.F7 "Figure 7 ‣ 4.2 Hybrid history conditioned Long Video Extension ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"), we qualitatively demonstrate superior capabilities of Hunyuan-GameCraft from multiple perspectives. The part(a) compares our method with Matrix-Game in sequential single-action scenarios, using the Minecraft environment originally employed for training of Matrix-Game. The results demonstrate significantly superior interaction capabilities of Hunyuan-GameCraft. Furthermore, continuous left-right rotations effectively showcase the enhanced historical information retention enabled by hybrid history condition training approach. The comparison of both game interaction models with sequential coupled action is shown in (b). Our method can accurately map input-coupled interaction signals while maintaining both quality consistency and spatial coherence during long video extension, achieving an immersive exploration experience. Part(c) focuses on evaluating image-to-video generation performance under single action across all baselines. Hunyuan-GameCraft demonstrates significant advantages in dynamic capability, including windmill rotation consistency, as well as overall visual quality.

Report issue for preceding element

User Study. Given the current lack of comprehensive benchmarks for interactive video generation models in both gaming and general scenarios, we conducted a user study involving 30 evaluators to enhance the reliability of our assessment. As shown in Tab. [3](https://arxiv.org/html/2506.17201v1#S5.T3 "Table 3 ‣ 5.2 Comparisons with other methods ‣ 5 Experiment ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"), our method achieved the highest scores by a margin across multiple dimensions in the anonymous user rankings.

Report issue for preceding element

Method

Video Quality ↑↑\\uparrow↑

Temporal Consistency ↑↑\\uparrow↑

Motion Smooth ↑↑\\uparrow↑

Action Accuracy ↑↑\\uparrow↑

Dynamic↑↑\\uparrow↑

CameraCtrl

2.20

2.40

2.16

2.87

2.57

MotionCtrl

3.23

3.20

3.21

3.09

3.22

WanX-Cam

2.42

2.53

2.44

2.81

2.46

Matrix-Game

2.72

2.43

2.75

1.63

2.21

Ours

4.42

4.44

4.53

4.61

4.54

Table 3: Average ranking score of user study. For each object, users are asked to give a rank score where 5 for the best, and 1 for the worst. User prefer ours the best in both aspects.

Report issue for preceding element

### 5.3 Ablation Study

Report issue for preceding element

In this section, comprehensive experiments are conducted to validate the effectiveness of our contributions, including the data distribution, control injection, and hybrid history conditioning.

Report issue for preceding element

FVD↓↓\\downarrow↓

DA↑↑\\uparrow↑

Aesthetic↑↑\\uparrow↑

RPE trans↓↓\\downarrow↓

RPE rot↓↓\\downarrow↓

(a) Only Synthetic Data

2550.7

34.6

0.56

0.07

0.17

(b) Only Live Data

1937.7

77.2

0.60

0.16

0.27

(c) Token Concat.

2236.4

59.7

0.54

0.13

0.29

(d) Channel-wise Concat.

1725.5

63.2

0.49

0.11

0.25

(e) Image Condition

1655.3

47.6

0.58

0.07

0.22

(f) Clip Condition

1743.5

55.3

0.57

0.16

0.30

(g) Ours (Render:Live=1:5)

1554.2

67.2

0.67

0.08

0.20

Table 4: Ablation study on different data distribution, control injection, and hybrid history conditioning. DA denotes Dynamic Average score.

Report issue for preceding element

Data Distribution. To understand the distinct contributions of game data and synthetic data, we began with an ablation study evaluating their impact on the model’s capabilities. Notably, the synthetic data does not highlight dynamic objects due to the computational expense and complexity of generating dynamical scenes. Tab. [4](https://arxiv.org/html/2506.17201v1#S5.T4 "Table 4 ‣ 5.3 Ablation Study ‣ 5 Experiment ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition")(a)(b) demonstrate that training exclusively on synthetic data significantly improves interaction accuracy but substantially degrades dynamic generation capabilities, while gameplay data exhibits the opposite characteristics. Our training distribution achieves balanced results.

Report issue for preceding element

Action Control Injection. Here we present ablation details for our camera injection experiments. Since the Plücker embeddings are already temporally and spatially aligned with the video latent representations, we implement three straightforward camera control schemes: (i) Token Addition, (ii) Token Concatenation, and (iii) Channel-wise Concatenation, as shown in the Tab. [4](https://arxiv.org/html/2506.17201v1#S5.T4 "Table 4 ‣ 5.3 Ablation Study ‣ 5 Experiment ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition")(c)(d)(g). Simply adding control signals at the initial stage achieves state-of-the-art control performance. Considering computational efficiency, we ultimately adopt Token Addition in our framework.

Report issue for preceding element

Hybrid History Conditioning. Hunyuan-GameCraft implements hybrid history conditioning for video generation and extension. Fig. [6](https://arxiv.org/html/2506.17201v1#S4.F6 "Figure 6 ‣ 4.2 Hybrid history conditioned Long Video Extension ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition") visually demonstrates visual results under different conditioning schemes, while we provide quantitative ablation analysis here. As shown in Tab. [4](https://arxiv.org/html/2506.17201v1#S5.T4 "Table 4 ‣ 5.3 Ablation Study ‣ 5 Experiment ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition")(e)(f)(g), Hunyuan-GameCraft achieves satisfactory control accuracy when trained with single frame conditioning, yet suffers from quality degradation over multiple action sequences due to limited historical context, leading to quality collapse as shown in Fig. [6](https://arxiv.org/html/2506.17201v1#S4.F6 "Figure 6 ‣ 4.2 Hybrid history conditioned Long Video Extension ‣ 4 Method ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"). When employing historical clip conditioning, the model exhibits degraded interaction accuracy when processing control signals that significantly deviate from historical motions. Our hybrid history conditioning effectively balances this trade-off, enabling Hunyuan-GameCraft to simultaneously achieve superior interaction performance, long-term consistency and visual quality.

Report issue for preceding element

![Refer to caption](x8.png)

Figure 8: Long Video Extension Results. Hunyuan-GameCraft can generate minute-level video clips in length while maintaining the visual quality.

Report issue for preceding element

![Refer to caption](x9.png)

Figure 9: Interactive results on the third-perspective game video generation.

Report issue for preceding element

![Refer to caption](x10.png)

Figure 10: Hunyuan-GameCraft enables high-fidelity and high-dynamic real-world video generation with accurate camera control.

Report issue for preceding element

6 Generalization on Real Worlds
-------------------------------

Report issue for preceding element

Although our model is tailored for game scenes, the integration of a pre-trained video foundation model significantly enhances its generalization capabilities, enabling it to generate interactive videos in real-world domains as well. As shown in Fig [10](https://arxiv.org/html/2506.17201v1#S5.F10 "Figure 10 ‣ 5.3 Ablation Study ‣ 5 Experiment ‣ Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition"), given images in real world, Hunyuan-GameCraft can successfully generate reasonable video with conditioned camera movement while keeping the dynamics.

Report issue for preceding element

7 Limitations and Future Work
-----------------------------

Report issue for preceding element

While Hunyuan-GameCraft demonstrates impressive capabilities in interactive game video generation, its current action space is mainly tailored to open-world exploration and lacks a wider array of game-specific actions such as shooting, throwing, and explosions. In future work, we will expand the dataset with more diverse gameplay elements. Building on our advancements in controllability, long-form video generation, and history preservation, we will focus on developing the next-generation model for more physical and playable game interactions.

Report issue for preceding element

8 Conclusion
------------

Report issue for preceding element

In this paper, we introduce Hunyuan-GameCraft, a significant step forward in interactive video generation. Through a unified action representation, hybrid history-conditioned training, and model distillation, our framework enables fine-grained control, efficient inference, and scalable long video synthesis. Besides, Hunyuan-GameCraft delivers enhanced realism, responsiveness, and temporal coherence. Our results demonstrate substantial improvements over existing methods, establishing Hunyuan-GameCraft as a robust foundation for future research and real-time deployment in immersive gaming environments.

Report issue for preceding element

References
----------

Report issue for preceding element

*   Blattmann et al. \[2023a\]↑ Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_, 2023a.
*   Blattmann et al. \[2023b\]↑ Andreas Blattmann, Robin Rombach, Huan Ling, Tim Dockhorn, Seung Wook Kim, Sanja Fidler, and Karsten Kreis. Align your latents: High-resolution video synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_, pages 22563–22575, 2023b.
*   Bradski \[2000\]↑ Gary Bradski. The opencv library. _Dr. Dobb’s Journal: Software Tools for the Professional Programmer_, 25(11):120–123, 2000.
*   \[4\]↑ Brandon Castellano. PySceneDetect.
*   Che et al. \[2025\]↑ Haoxuan Che, Xuanhua He, Quande Liu, Cheng Jin, and Hao Chen. Gamegen-x: Interactive open-world game video generation. In _International Conference on Learning Representations_, 2025.
*   Chen et al. \[2024\]↑ Boyuan Chen, Diego Martí Monsó, Yilun Du, Max Simchowitz, Russ Tedrake, and Vincent Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. _Advances in Neural Information Processing Systems_, 37:24081–24125, 2024.
*   Dalal et al. \[2025\]↑ Karan Dalal, Daniel Koceja, Gashon Hussein, Jiarui Xu, Yue Zhao, Youjin Song, Shihao Han, Ka Chun Cheung, Jan Kautz, Carlos Guestrin, et al. One-minute video generation with test-time training. _arXiv preprint arXiv:2504.05298_, 2025.
*   Decard \[2024\]↑ Decard. Oasis: A universe in a transformer. [https://www.decart.ai/articles/oasis-interactive-ai-video-game-model](https://www.decart.ai/articles/oasis-interactive-ai-video-game-model), 2024.
*   Esser et al. \[2024\]↑ Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas Müller, Harry Saini, Yam Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling rectified flow transformers for high-resolution image synthesis. In _Forty-first international conference on machine learning_, 2024.
*   Feng et al. \[2024\]↑ Ruili Feng, Han Zhang, Zhantao Yang, Jie Xiao, Zhilei Shu, Zhiheng Liu, Andy Zheng, Yukun Huang, Yu Liu, and Hongyang Zhang. The matrix: Infinite-horizon world generation with real-time moving control. _arXiv preprint arXiv:2412.03568_, 2024.
*   Gao et al. \[2024\]↑ Kaifeng Gao, Jiaxin Shi, Hanwang Zhang, Chunping Wang, and Jun Xiao. Vid-gpt: Introducing gpt-style autoregressive generation in video diffusion models. _arXiv preprint arXiv:2406.10981_, 2024.
*   Gu et al. \[2025\]↑ Yuchao Gu, Weijia Mao, and Mike Zheng Shou. Long-context autoregressive video modeling with next-frame prediction. _arXiv preprint arXiv:2503.19325_, 2025.
*   He et al. \[2024\]↑ Hao He, Yinghao Xu, Yuwei Guo, Gordon Wetzstein, Bo Dai, Hongsheng Li, and Ceyuan Yang. Cameractrl: Enabling camera control for text-to-video generation. _arXiv preprint arXiv:2404.02101_, 2024.
*   He et al. \[2025\]↑ Hao He, Ceyuan Yang, Shanchuan Lin, Yinghao Xu, Meng Wei, Liangke Gui, Qi Zhao, Gordon Wetzstein, Lu Jiang, and Hongsheng Li. Cameractrl ii: Dynamic scene exploration via camera-controlled video diffusion models. _arXiv preprint arXiv:2503.10592_, 2025.
*   Henschel et al. \[2024\]↑ Roberto Henschel, Levon Khachatryan, Hayk Poghosyan, Daniil Hayrapetyan, Vahram Tadevosyan, Zhangyang Wang, Shant Navasardyan, and Humphrey Shi. Streamingt2v: Consistent, dynamic, and extendable long video generation from text. _arXiv preprint arXiv:2403.14773_, 2024.
*   Huang et al. \[2024\]↑ Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang, Chenyang Si, Yuming Jiang, Yuanhan Zhang, Tianxing Wu, Qingyang Jin, Nattapol Chanpaisit, et al. Vbench: Comprehensive benchmark suite for video generative models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_, pages 21807–21818, 2024.
*   KolorsTeam \[2024\]↑ KolorsTeam. Kolors: Effective training of diffusion model for photorealistic text-to-image synthesis. _arXiv preprint_, 2024.
*   Kong et al. \[2024\]↑ Weijie Kong, Qi Tian, Zijian Zhang, Rox Min, Zuozhuo Dai, Jin Zhou, Jiangfeng Xiong, Xin Li, Bo Wu, Jianwei Zhang, et al. Hunyuanvideo: A systematic framework for large video generative models. _arXiv preprint arXiv:2412.03603_, 2024.
*   Li et al. \[2025\]↑ Ruihuang Li, Caijin Zhou, Shoujian Zheng, Jianxiang Lu, Jiabin Huang, Comi Chen, Junshu Tang, Guangzheng Xu, Jiale Tao, Hongmei Wang, et al. Hunyuan-game: Industrial-grade intelligent game creation model. _arXiv preprint arXiv:2505.14135_, 2025.
*   Lu et al. \[2024\]↑ Yu Lu, Yuanzhi Liang, Linchao Zhu, and Yi Yang. Freelong: Training-free long video generation with spectralblend temporal attention. _arXiv preprint arXiv:2407.19918_, 2024.
*   Luo et al. \[2023\]↑ Simian Luo, Yiqin Tan, Longbo Huang, Jian Li, and Hang Zhao. Latent consistency models: Synthesizing high-resolution images with few-step inference. _arXiv preprint arXiv:2310.04378_, 2023.
*   Parker-Holder et al. \[2024\]↑ Jack Parker-Holder, Philip Ball, Jake Bruce, Vibhavari Dasagi, Kristian Holsheimer, Christos Kaplanis, Alexandre Moufarek, Guy Scully, Jeremy Shar, Jimmy Shi, Stephen Spencer, Jessica Yung, Michael Dennis, Sultan Kenjeyev, Shangbang Long, Vlad Mnih, Harris Chan, Maxime Gazeau, Bonnie Li, Fabio Pardo, Luyu Wang, Lei Zhang, Frederic Besse, Tim Harley, Anna Mitenkova, Jane Wang, Jeff Clune, Demis Hassabis, Raia Hadsell, Adrian Bolton, Satinder Singh, and Tim Rocktäschel. Genie 2: A large-scale foundation world model. 2024.
*   Skorokhodov et al. \[2022\]↑ Ivan Skorokhodov, Sergey Tulyakov, and Mohamed Elhoseiny. Stylegan-v: A continuous video generator with the price, image quality and perks of stylegan2. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_, pages 3626–3636, 2022.
*   Teed and Deng \[2020\]↑ Zachary Teed and Jia Deng. Raft: Recurrent all-pairs field transforms for optical flow. In _Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part II 16_, pages 402–419. Springer, 2020.
*   Unterthiner et al. \[2019\]↑ Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Kurach, Raphaël Marinier, Marcin Michalski, and Sylvain Gelly. Fvd: A new metric for video generation. 2019.
*   Valevski et al. \[2024\]↑ Dani Valevski, Yaniv Leviathan, Moab Arar, and Shlomi Fruchter. Diffusion models are real-time game engines. _arXiv preprint arXiv:2408.14837_, 2024.
*   Wan et al. \[2025\]↑ Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, Jianyuan Zeng, Jiayu Wang, Jingfeng Zhang, Jingren Zhou, Jinkai Wang, Jixuan Chen, Kai Zhu, Kang Zhao, Keyu Yan, Lianghua Huang, Mengyang Feng, Ningyi Zhang, Pandeng Li, Pingyu Wu, Ruihang Chu, Ruili Feng, Shiwei Zhang, Siyang Sun, Tao Fang, Tianxing Wang, Tianyi Gui, Tingyu Weng, Tong Shen, Wei Lin, Wei Wang, Wei Wang, Wenmeng Zhou, Wente Wang, Wenting Shen, Wenyuan Yu, Xianzhong Shi, Xiaoming Huang, Xin Xu, Yan Kou, Yangyu Lv, Yifei Li, Yijing Liu, Yiming Wang, Yingya Zhang, Yitong Huang, Yong Li, You Wu, Yu Liu, Yulin Pan, Yun Zheng, Yuntao Hong, Yupeng Shi, Yutong Feng, Zeyinzi Jiang, Zhen Han, Zhi-Fan Wu, and Ziyu Liu. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_, 2025.
*   Wang et al. \[2024a\]↑ Fu-Yun Wang, Zhaoyang Huang, Alexander Bergman, Dazhong Shen, Peng Gao, Michael Lingelbach, Keqiang Sun, Weikang Bian, Guanglu Song, Yu Liu, et al. Phased consistency models. _Advances in neural information processing systems_, 37:83951–84009, 2024a.
*   Wang et al. \[2024b\]↑ Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_, 2024b.
*   Wang et al. \[2024c\]↑ Xiaofeng Wang, Zheng Zhu, Guan Huang, Boyuan Wang, Xinze Chen, and Jiwen Lu. Worlddreamer: Towards general world models for video generation via predicting masked tokens. _arXiv preprint arXiv:2401.09985_, 2024c.
*   Wang et al. \[2024d\]↑ Zhouxia Wang, Ziyang Yuan, Xintao Wang, Yaowei Li, Tianshui Chen, Menghan Xia, Ping Luo, and Ying Shan. Motionctrl: A unified and flexible motion controller for video generation. In _ACM SIGGRAPH 2024 Conference Papers_, pages 1–11, 2024d.
*   WorldLabs \[2024\]↑ WorldLabs. Generating worlds. [https://www.worldlabs.ai/blog](https://www.worldlabs.ai/blog), 2024.
*   Yang et al. \[2021\]↑ Mengyue Yang, Furui Liu, Zhitang Chen, Xinwei Shen, Jianye Hao, and Jun Wang. Causalvae: Disentangled representation learning via neural structural causal models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_, pages 9593–9602, 2021.
*   Yu et al. \[2025\]↑ Jiwen Yu, Yiran Qin, Xintao Wang, Pengfei Wan, Di Zhang, and Xihui Liu. Gamefactory: Creating new games with generative interactive videos. _arXiv preprint arXiv:2501.08325_, 2025.
*   Zhang et al. \[2024\]↑ Junyi Zhang, Charles Herrmann, Junhwa Hur, Varun Jampani, Trevor Darrell, Forrester Cole, Deqing Sun, and Ming-Hsuan Yang. Monst3r: A simple approach for estimating geometry in the presence of motion. _arXiv preprint arXiv:2410.03825_, 2024.
*   Zhang et al. \[2025\]↑ Yifan Zhang, Chunli Peng, Boyang Wang, Puyi Wang, Qingcheng Zhu, Zedong Gao, Eric Li, Yang Liu, and Yahui Zhou. Matrix-game: Interactive world foundation model. _arXiv_, 2025.
