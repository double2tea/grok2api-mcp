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
    """创建MCP服务器实例，如果配置了API密钥则启用认证"""
    # 检查是否配置了API密钥
    api_key = setting.grok_config.get("api_key")

    # 如果配置了API密钥，则启用静态token验证
    auth = None
    if api_key:
        auth = StaticTokenVerifier(
            tokens={
                api_key: {
                    "client_id": "grok2api-client",
                    "scopes": ["read", "write", "admin"],
                }
            },
            required_scopes=["read"],
        )

    # 创建FastMCP实例
    return FastMCP(
        name="Grok2API-MCP",
        instructions="MCP server providing Grok AI chat, image generation, and video generation capabilities.",
        auth=auth,
    )


# 创建全局MCP实例
mcp = create_mcp_server()


# 注册ask_grok工具
@mcp.tool
async def ask_grok(
    query: str, model: str = "grok-3-fast", system_prompt: str = None
) -> str:
    """
    调用Grok AI进行对话，适用于一般问答、写作、分析等任务。

    Args:
        query: 用户的问题或指令
        model: 模型名称 (默认: grok-3-fast)
        system_prompt: 可选的系统提示词

    Returns:
        Grok AI的回复
    """
    return await ask_grok_impl(query, model, system_prompt)


@mcp.tool
async def generate_image(prompt: str, model: str = "grok-3-fast") -> str:
    """
    使用Grok AI生成图片。

    Args:
        prompt: 图片描述提示词 (例如: "一只在太空中飞行的猫")
        model: 模型名称 (默认: grok-3-fast)

    Returns:
        包含生成图片链接的Markdown内容
    """
    return await generate_image_impl(prompt, model)


@mcp.tool
async def generate_video(
    prompt: str, image_url: str, model: str = "grok-imagine-0.9"
) -> str:
    """
    使用Grok AI生成视频 (图生视频)。

    Args:
        prompt: 视频描述提示词 (例如: "让图片中的人物动起来")
        image_url: 源图片URL
        model: 视频模型 (默认: grok-imagine-0.9)

    Returns:
        包含生成视频链接的Markdown内容
    """
    return await generate_video_impl(prompt, image_url, model)


@mcp.tool
async def list_models() -> str:
    """
    列出所有可用的Grok模型及其功能支持情况。

    Returns:
        Markdown格式的模型列表
    """
    return await list_models_impl()
