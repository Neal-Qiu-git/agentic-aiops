"""
Agentic AIOps - Agent 驱动的智能运维平台

一个基于 ReAct 循环的智能运维系统，支持多种 Agent 和工具。
"""

__version__ = "2.1.0"
__author__ = "Neal"
__license__ = "MIT"
__description__ = "Agent 驱动的智能运维平台"

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
