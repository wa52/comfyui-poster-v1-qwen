"""DashScope Qwen text generation node."""

import json
import os
import ssl
import time
import urllib.error
import urllib.request


class DashScopeQwenText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "system_prompt": ("STRING", {
                    "default": "You are a concise assistant.",
                    "multiline": True,
                }),
                "model": (["qwen-plus", "qwen-turbo", "qwen-max"], {
                    "default": "qwen-plus",
                }),
                "region": (["China", "International"], {
                    "default": "China",
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
                "temperature": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.05,
                }),
                "max_tokens": ("INT", {
                    "default": 256,
                    "min": 1,
                    "max": 8192,
                    "step": 1,
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate"
    CATEGORY = "api/text"

    def generate(self, prompt, system_prompt, model, region, api_key, temperature, max_tokens):
        key = api_key.strip() or os.environ.get("DASHSCOPE_API_KEY", "").strip()
        if not key:
            raise ValueError("DashScope API key is required. Enter it in the node or set DASHSCOPE_API_KEY.")

        host = "dashscope.aliyuncs.com" if region == "China" else "dashscope-intl.aliyuncs.com"
        url = f"https://{host}/compatible-mode/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        request_data = json.dumps(payload).encode("utf-8")
        result = None
        for attempt in range(3):
            request = urllib.request.Request(
                url,
                data=request_data,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "Connection": "close",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    result = json.loads(response.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as error:
                detail = error.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"DashScope API error {error.code}: {detail}") from error
            except (urllib.error.URLError, ssl.SSLError, ConnectionResetError, TimeoutError) as error:
                reason = getattr(error, "reason", error)
                transient = isinstance(reason, (ssl.SSLError, ConnectionResetError, TimeoutError, EOFError))
                if not transient or attempt == 2:
                    raise RuntimeError(f"DashScope connection failed: {reason}") from error
                time.sleep(1.5 * (attempt + 1))

        try:
            text = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError(f"Unexpected DashScope response: {result}") from error
        return (text.strip(),)


class DashScopeQwenTextFields(DashScopeQwenText):
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("title", "subtitle", "price")

    def generate(self, prompt, system_prompt, model, region, api_key, temperature, max_tokens):
        text = super().generate(prompt, system_prompt, model, region, api_key, temperature, max_tokens)[0]
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        lines = (lines + ["", "", ""])[:3]
        return tuple(lines)


class SplitTextFields:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING", {"default": "", "multiline": True})}}

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("title", "subtitle", "price")
    FUNCTION = "split"
    CATEGORY = "text"

    def split(self, text):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        lines = (lines + ["", "", ""])[:3]
        return tuple(lines)
