"""工具基类 - 安全版本"""
import time
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ToolCategory(Enum):
    """工具类别"""
    SSH = "ssh"
    K8S = "k8s"
    DOCKER = "docker"
    DATABASE = "database"
    MONITORING = "monitoring"
    LOG = "log"
    SECURITY = "security"
    UTILITY = "utility"


@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    output: str
    error: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    tool_name: str = ""

    def to_string(self) -> str:
        """转换为字符串"""
        if self.success:
            return self.output
        return f"ERROR: {self.error}\n{self.output}"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "output": self.output[:1000],  # 限制输出长度
            "error": self.error,
            "metadata": self.metadata,
            "execution_time": self.execution_time,
            "tool_name": self.tool_name,
        }


class BaseTool(ABC):
    """工具基类 - 所有 MCP 工具继承此类"""

    name: str = "base"
    description: str = ""
    category: ToolCategory = ToolCategory.UTILITY
    parameters: Dict[str, Any] = field(default_factory=dict)  # JSON Schema
    requires_ssh: bool = False
    requires_confirmation: bool = False  # 是否需要确认
    timeout: int = 30
    max_output_size: int = 10000

    # 安全属性
    is_destructive: bool = False  # 是否是破坏性操作
    is_readonly: bool = True  # 是否是只读操作

    def __init__(self):
        self._registry = None
        self._execution_count = 0
        self._last_execution_time = 0.0

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        pass

    def validate_input(self, **kwargs) -> Optional[str]:
        """
        验证输入参数

        Returns:
            错误信息，如果验证通过返回 None
        """
        # 检查必需参数
        required = self.parameters.get("required", [])
        for param in required:
            if param not in kwargs or kwargs[param] is None:
                return f"缺少必需参数: {param}"

        return None

    def pre_execute(self, **kwargs) -> Optional[ToolResult]:
        """
        执行前的准备工作

        Returns:
            如果返回 ToolResult，则跳过执行
        """
        # 验证输入
        error = self.validate_input(**kwargs)
        if error:
            return ToolResult(success=False, error=error, tool_name=self.name)

        # 检查是否需要确认
        if self.requires_confirmation and not kwargs.get("confirm", False):
            return ToolResult(
                success=False,
                error=f"此操作需要确认。请设置 confirm=true 以执行。",
                tool_name=self.name,
            )

        return None

    def post_execute(self, result: ToolResult, **kwargs) -> ToolResult:
        """
        执行后的处理

        Args:
            result: 执行结果
            kwargs: 输入参数

        Returns:
            处理后的结果
        """
        # 限制输出大小
        if result.output and len(result.output) > self.max_output_size:
            result.output = result.output[:self.max_output_size] + "\n... [输出已截断]"

        # 添加元数据
        result.tool_name = self.name
        result.metadata["category"] = self.category.value
        result.metadata["is_destructive"] = self.is_destructive
        result.metadata["is_readonly"] = self.is_readonly

        return result

    def run(self, **kwargs) -> ToolResult:
        """
        运行工具（包含安全检查和日志记录）

        Returns:
            ToolResult
        """
        start_time = time.time()

        try:
            # 执行前检查
            pre_result = self.pre_execute(**kwargs)
            if pre_result:
                return pre_result

            logger.info(f"执行工具: {self.name}, 参数: {list(kwargs.keys())}")

            # 执行工具
            result = self.execute(**kwargs)

            # 执行后处理
            result = self.post_execute(result, **kwargs)

            # 记录执行时间
            execution_time = time.time() - start_time
            result.execution_time = execution_time

            # 更新统计
            self._execution_count += 1
            self._last_execution_time = execution_time

            # 记录日志
            if result.success:
                logger.info(f"工具执行成功: {self.name}, 耗时: {execution_time:.2f}s")
            else:
                logger.warning(f"工具执行失败: {self.name}, 错误: {result.error}")

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"工具执行异常: {self.name}, 错误: {e}, 耗时: {execution_time:.2f}s")
            return ToolResult(
                success=False,
                error=f"工具执行异常: {e}",
                tool_name=self.name,
                execution_time=execution_time,
            )

    def to_schema(self) -> Dict[str, Any]:
        """转换为 OpenAI function calling schema"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取工具统计信息"""
        return {
            "name": self.name,
            "category": self.category.value,
            "execution_count": self._execution_count,
            "last_execution_time": self._last_execution_time,
            "requires_ssh": self.requires_ssh,
            "requires_confirmation": self.requires_confirmation,
            "is_destructive": self.is_destructive,
            "is_readonly": self.is_readonly,
        }


class ToolRegistry:
    """工具注册中心"""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._audit_log: list = []

    def register(self, tool: BaseTool):
        """注册工具"""
        if tool.name in self._tools:
            logger.warning(f"工具 {tool.name} 已存在，将被覆盖")
        self._tools[tool.name] = tool
        tool._registry = self
        logger.debug(f"注册工具: {tool.name}")

    def get(self, name: str) -> Optional[BaseTool]:
        """获取工具"""
        return self._tools.get(name)

    def list_tools(self) -> list:
        """列出所有工具"""
        return [
            {
                "name": t.name,
                "description": t.description,
                "category": t.category.value,
                "requires_ssh": t.requires_ssh,
                "is_destructive": t.is_destructive,
            }
            for t in self._tools.values()
        ]

    def list_tools_by_category(self, category: ToolCategory) -> list:
        """按类别列出工具"""
        return [
            {"name": t.name, "description": t.description}
            for t in self._tools.values()
            if t.category == category
        ]

    def execute(self, name: str, args: Dict[str, Any]) -> str:
        """执行工具"""
        tool = self._tools.get(name)
        if not tool:
            return f"工具 {name} 未注册"

        # 记录审计日志
        audit_entry = {
            "tool": name,
            "args": {k: str(v)[:100] for k, v in args.items()},
            "timestamp": time.time(),
        }

        try:
            result = tool.run(**args)
            audit_entry["success"] = result.success
            audit_entry["execution_time"] = result.execution_time
            audit_entry["output_len"] = len(result.output)
            self._audit_log.append(audit_entry)
            return result.to_string()
        except Exception as e:
            audit_entry["success"] = False
            audit_entry["error"] = str(e)
            self._audit_log.append(audit_entry)
            return f"工具执行异常: {e}"

    def get_audit_log(self, limit: int = 100) -> list:
        """获取审计日志"""
        return self._audit_log[-limit:]

    def get_tool_stats(self) -> Dict[str, Any]:
        """获取所有工具统计"""
        return {
            "total_tools": len(self._tools),
            "tools": {name: tool.get_stats() for name, tool in self._tools.items()},
        }
