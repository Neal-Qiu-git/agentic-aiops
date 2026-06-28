"""
Agentic AIOps - AI Native 智能运维平台

基于 LLM + ReAct + MCP + Multi-Agent 构建的新一代 AI 运维平台。
真正实现：AI 能独立完成一次完整的运维闭环。
"""

__version__ = "3.1.0"
__author__ = "Neal"
__license__ = "MIT"
__description__ = "AI Native 智能运维平台，让 AI 不仅能分析，还能真正完成运维工作"

# 导出核心模块
from .core.config import Config, ServerConfig, AIConfig
from .core.engine import AIOpsEngine, create_engine
from .core.ssh_manager import SSHManager
from .core.ai_agent import AIAgent

# 导出工具模块
from .tools.base import BaseTool, ToolResult, ToolRegistry, ToolCategory

__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    "__license__",
    "__description__",
    # 核心模块
    "Config",
    "ServerConfig",
    "AIConfig",
    "AIOpsEngine",
    "create_engine",
    "SSHManager",
    "AIAgent",
    # 工具模块
    "BaseTool",
    "ToolResult",
    "ToolRegistry",
    "ToolCategory",
]
