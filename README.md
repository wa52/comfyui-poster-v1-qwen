# ComfyUI Poster V1 — Qwen

中文电商海报工作流：本地 Z-Image 生成 9:16 无文字主视觉，DashScope Qwen API 生成两行中文文案，再用 `DrawText+` 精确叠加。

V0.2 已加入真实负面条件、结构化文案拆分（产品名/卖点/价格）和三个独立文字图层，适合继续调整字号、颜色和坐标。

## 使用

1. 安装/复制 `custom_nodes/comfyui-dashscope-text` 到 ComfyUI 的 `custom_nodes`，重启 ComfyUI。
2. 安装并启用 **ComfyUI-GGUF**（提供 `UnetLoaderGGUF` 和 `CLIPLoaderGGUF`）以及 **ComfyUI Essentials**（提供 `DrawText+`）。
3. 将 `NotoSansSC-VF.ttf`（或其他支持中文的字体）放入 `custom_nodes/ComfyUI_essentials/fonts/`。
4. 导入 `workflow_api.json`，在 `DashScopeQwenText` 节点填写自己的 DashScope Key。
5. 确认模型文件已存在：`z_image_turbo-Q8_0.gguf`、`Qwen3-4B-UD-Q6_K_XL.gguf`、`z-image-ae.safetensors`。

`workflow_ui.json` 保留节点位置和画布布局；`workflow_api.json` 用于 API/队列执行。两个文件都不包含真实 API Key。

API Key 不包含在本仓库中；请勿把真实 Key 提交到 Git。

## 输出

默认尺寸为 720×1280（9:16），提示词明确禁止生图模型绘制文字，文案由 Qwen API 生成后拆分为三个可独立编辑的文字图层。
