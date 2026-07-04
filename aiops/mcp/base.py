"""MCP 基类"""
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class MCPCapability(Enum):
    """MCP 能力"""
    EXECUTE = "execute"           # 执行命令
    QUERY = "query"               # 查询数据
    STREAM = "stream"             # 流式输出
    NOTIFICATION = "notification" # 通知
    FILE_SYSTEM = "file_system"   # 文件系统
    NETWORK = "network"           # 网络
    DATABASE = "database"         # 数据库
    MESSAGE_QUEUE = "message_queue"  # 消息队列
    CLOUD_API = "cloud_api"       # 云 API
    CONTAINER = "container"       # 容器
    ORCHESTRATION = "orchestration"  # 编排


@dataclass
class MCPToolInfo:
    """MCP 工具信息"""
    name: str
    description: str
    version: str
    author: str
    capabilities: List[MCPCapability]
    parameters: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    category: str = ""
    enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "capabilities": [c.value for c in self.capabilities],
            "parameters": self.parameters,
            "tags": self.tags,
            "category": self.category,
            "enabled": self.enabled,
        }


class BaseMCPTool(ABC):
    """MCP 工具基类"""

    def __init__(self):
        self._info: Optional[MCPToolInfo] = None

    @abstractmethod
    def get_info(self) -> MCPToolInfo:
        """获取工具信息"""
        pass

    @abstractmethod
    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """
        执行命令

        Args:
            command: 命令
            **kwargs: 参数

        Returns:
            执行结果
        """
        pass

    @abstractmethod
    def query(self, query: str, **kwargs) -> Any:
        """
        查询数据

        Args:
            query: 查询语句
            **kwargs: 参数

        Returns:
            查询结果
        """
        pass

    def get_capabilities(self) -> List[MCPCapability]:
        """获取能力列表"""
        info = self.get_info()
        return info.capabilities

    def has_capability(self, capability: MCPCapability) -> bool:
        """检查是否有某种能力"""
        return capability in self.get_capabilities()
