"""DashScope Text — ComfyUI custom node pack."""

from .src.nodes import DashScopeQwenText, DashScopeQwenTextFields, SplitTextFields

NODE_CLASS_MAPPINGS = {
    "DashScopeQwenText": DashScopeQwenText,
    "DashScopeQwenTextFields": DashScopeQwenTextFields,
    "SplitTextFields": SplitTextFields,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DashScopeQwenText": "DashScope Qwen Text",
    "DashScopeQwenTextFields": "DashScope Qwen Text Fields",
    "SplitTextFields": "Split Text Fields",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
