"""Tool Registry - 工具注册中心"""
import time
from .base import BaseTool, ToolResult


class ToolRegistry:
    """工具注册中心 - 管理所有 MCP 工具"""

    def __init__(self, ssh_manager=None, config=None):
        self._tools = {}
        self._agents = {}
        self.ssh = ssh_manager
        self.config = config
        self._audit_log = []

    def register(self, tool: BaseTool):
        """注册工具"""
        self._tools[tool.name] = tool
        tool._registry = self

    def register_agent(self, name: str, agent_factory):
        """注册 Agent 为可调用工具"""
        self._agents[name] = agent_factory

    def get(self, name: str) -> BaseTool:
        """获取工具"""
        return self._tools.get(name)

    def list_tools(self) -> list:
        """列出所有工具"""
        return [{"name": t.name, "description": t.description} for t in self._tools.values()]

    def execute(self, name: str, args: dict) -> str:
        """执行工具"""
        tool = self._tools.get(name)
        if not tool:
            return f"工具 {name} 未注册"

        start = time.time()
        try:
            result = tool.execute(**args)
            elapsed = time.time() - start
            self._audit_log.append({
                "tool": name, "args": args, "success": result.success,
                "elapsed": round(elapsed, 2), "output_len": len(result.output),
            })
            return result.to_string()
        except Exception as e:
            elapsed = time.time() - start
            self._audit_log.append({
                "tool": name, "args": args, "success": False,
                "elapsed": round(elapsed, 2), "error": str(e),
            })
            return f"工具执行异常: {e}"

    def execute_agent(self, agent_name: str, task: str, context: dict = None) -> "AgentResult":
        """执行 Agent"""
        factory = self._agents.get(agent_name)
        if not factory:
            from ..agents.base import AgentResult
            return AgentResult(answer=f"Agent {agent_name} 未注册", success=False)
        agent = factory()
        return agent.run(task, context)

    def get_audit_log(self) -> list:
        return self._audit_log
