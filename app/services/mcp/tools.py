# -*- coding: utf-8 -*-
"""MCP Tools"""

import json
from typing import Optional
from app.services.grok.client import GrokClient
from app.core.logger import logger
from app.core.exception import GrokApiException


async def ask_grok_impl(query: str, model: str = "grok-3-fast", system_prompt: Optional[str] = None) -> str:
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})
        request_data = {"model": model, "messages": messages, "stream": True}
        
        logger.info(f"[MCP] ask_grok 调用, 模型: {model}")
        response_iterator = await GrokClient.openai_to_grok(request_data)
        
        content_parts = []
        async for chunk in response_iterator:
            if isinstance(chunk, bytes):
                chunk = chunk.decode("utf-8")
            if chunk.startswith("data: "):
                data_str = chunk[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    choices = data.get("choices", [])
                    if choices:
                        delta = choices[0].get("delta", {})
                        if content := delta.get("content"):
                            content_parts.append(content)
                except json.JSONDecodeError:
                    continue
        
        result = "".join(content_parts)
        logger.info(f"[MCP] ask_grok 完成")
        return result
    except Exception as e:
        logger.error(f"[MCP] ask_grok异常: {str(e)}")
        raise Exception(f"处理请求时出错: {str(e)}")


async def generate_image_impl(prompt: str, num_images: int = 2, model: str = "grok-3-fast") -> str:
    try:
        messages = [{"role": "user", "content": f"请根据以下描述生成图片: {prompt}"}]
        request_data = {"model": model, "messages": messages, "stream": False}
        
        logger.info(f"[MCP] generate_image 调用")
        result = await GrokClient.openai_to_grok(request_data)
        
        if isinstance(result, tuple):
            media_urls = result[1] if len(result) > 1 else []
        else:
            media_urls = []
        
        image_urls = media_urls if media_urls else []
        if not image_urls:
            raise Exception("未能生成图片")
        
        content = ""
        for i, img_url in enumerate(image_urls):
            if not str(img_url).startswith("http"):
                img_url = f"https://assets.grok.com/{img_url}"
            content += f"\n![Generated Image {i + 1}]({img_url})"
        
        return content.strip() if content else "生成了图片"
    except Exception as e:
        logger.error(f"[MCP] generate_image异常: {str(e)}")
        raise Exception(f"图片生成失败: {str(e)}")


async def generate_video_impl(image_url: str, prompt: str) -> str:
    try:
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_url}}]}]
        request_data = {"model": "grok-imagine-0.9", "messages": messages, "stream": False}
        
        logger.info(f"[MCP] generate_video 调用")
        result = await GrokClient.openai_to_grok(request_data)
        
        if isinstance(result, tuple):
            video_url = result[1][0] if result[1] else None
        else:
            video_url = None
        
        if not video_url:
            raise Exception("未能生成视频")
        
        if not str(video_url).startswith("http"):
            video_url = f"https://assets.grok.com/{video_url}"
        
        return f'<video src="{video_url}" controls="controls" width="500" height="300"></video>'
    except Exception as e:
        logger.error(f"[MCP] generate_video异常: {str(e)}")
        raise Exception(f"视频生成失败: {str(e)}")


async def list_models_impl() -> str:
    try:
        from app.models.grok_models import _MODEL_CONFIG
        models_list = []
        for model_id, config in _MODEL_CONFIG.items():
            models_list.append({
                "id": model_id,
                "display_name": config.get("display_name", model_id),
                "description": config.get("description", ""),
                "requires_super": config.get("requires_super", False),
                "cost": config.get("cost", {"multiplier": 1}),
                "capabilities": {
                    "chat": True,
                    "image_generation": True,
                    "video_generation": config.get("is_video_model", False),
                }
            })
        return json.dumps(models_list, ensure_ascii=False, indent=2)
    except Exception as e:
        raise Exception(f"获取模型列表失败: {str(e)}")
