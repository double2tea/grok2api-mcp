# -*- coding: utf-8 -*-
"""FastMCP服务器实例"""

from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from app.services.mcp.tools import (
    ask_grok_impl,
    generate_image_impl,
    generate_video_impl,
    list_models_impl,
)
from app.core.config import setting


def create_mcp_server() -> FastMCP:
    api_key = setting.grok_config.get("api_key")
    
    auth = None
    if api_key:
        auth = StaticTokenVerifier(
            tokens={api_key: {"client_id": "grok2api-client", "scopes": ["read", "write", "admin"]}},
            required_scopes=["read"],
        )
    
    return FastMCP(
        name="Grok2API-MCP",
        instructions="MCP server for Grok AI",
        auth=auth,
    )


mcp = create_mcp_server()


@mcp.tool
async def ask_grok(query: str, model: str = "grok-3-fast", system_prompt: str = None) -> str:
    """调用Grok AI进行对话"""
    return await ask_grok_impl(query, model, system_prompt)


@mcp.tool
async def generate_image(prompt: str, num_images: int = 2, model: str = "grok-3-fast") -> str:
    """调用Grok AI生成图片"""
    return await generate_image_impl(prompt, num_images, model)


@mcp.tool
async def generate_video(image_url: str, prompt: str) -> str:
    """调用Grok AI根据图片生成视频"""
    return await generate_video_impl(image_url, prompt)


@mcp.tool
async def list_models() -> str:
    """获取Grok2API支持的模型列表"""
    return await list_models_impl()
