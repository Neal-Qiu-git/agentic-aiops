"""工具基类"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    output: str
    error: str = ""
    metadata: dict = field(default_factory=dict)

    def to_string(self):
        if self.success:
            return self.output
        return f"ERROR: {self.error}\n{self.output}"


class BaseTool(ABC):
    """工具基类 - 所有 MCP 工具继承此类"""

    name: str = "base"
    description: str = ""
    parameters: dict = field(default_factory=dict)  # JSON Schema
    requires_ssh: bool = False
    timeout: int = 30

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        pass

    def to_schema(self) -> dict:
        """转换为 OpenAI function calling schema"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }
