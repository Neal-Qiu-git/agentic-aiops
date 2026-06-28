"""SSH 远程执行工具"""
from .base import BaseTool, ToolResult


class SSHExecTool(BaseTool):
    name = "ssh_exec"
    description = "在远程服务器上执行命令并返回结果"
    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "要执行的 shell 命令"},
            "host": {"type": "string", "description": "目标服务器地址（可选，默认使用配置的服务器）"},
            "timeout": {"type": "integer", "description": "超时时间(秒)", "default": 30},
        },
        "required": ["command"],
    }
    requires_ssh = True

    def execute(self, command: str, host: str = None, timeout: int = 30, **kwargs) -> ToolResult:
        from ..core.config import ServerConfig
        if not self._registry or not self._registry.ssh:
            return ToolResult(success=False, error="SSH 未配置")
        ssh = self._registry.ssh
        config = self._registry.config
        # 确定目标服务器
        server = None
        if host:
            server = config.get_server(host=host)
        if not server and config.servers:
            server = config.servers[0]
        if not server:
            return ToolResult(success=False, error=f"未找到服务器 {host}")

        try:
            out, err, code = ssh.exec_command(server, command, timeout=timeout)
            output = out.strip()
            if err.strip():
                output += f"\n[stderr] {err.strip()}"
            return ToolResult(success=(code == 0), output=output[:5000],
                            error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))
