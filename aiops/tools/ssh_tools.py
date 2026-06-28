"""SSH 远程执行工具 - 安全版本"""
import logging
from typing import Optional, List
from .base import BaseTool, ToolResult, ToolCategory
from ..core.security import CommandValidator, SecurityLevel

logger = logging.getLogger(__name__)


class SSHExecTool(BaseTool):
    """SSH 远程执行工具"""
    name = "ssh_exec"
    description = "在远程服务器上执行命令并返回结果"
    category = ToolCategory.SSH
    requires_ssh = True
    is_readonly = False  # 命令可能是破坏性的

    parameters = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "要执行的 shell 命令"
            },
            "host": {
                "type": "string",
                "description": "目标服务器地址（可选，默认使用配置的服务器）"
            },
            "timeout": {
                "type": "integer",
                "description": "超时时间(秒)",
                "default": 30,
            },
            "confirm": {
                "type": "boolean",
                "description": "确认执行危险命令",
                "default": False,
            },
        },
        "required": ["command"],
    }

    def __init__(self):
        super().__init__()
        self._validator = None

    def _get_validator(self) -> CommandValidator:
        """获取命令验证器"""
        if self._validator is None:
            # 从配置获取验证器
            if self._registry and hasattr(self._registry, 'config'):
                from ..core.security import create_command_validator_from_config
                self._validator = create_command_validator_from_config(self._registry.config)
            else:
                self._validator = CommandValidator()
        return self._validator

    def validate_input(self, command: str = None, **kwargs) -> Optional[str]:
        """验证输入"""
        if not command or not command.strip():
            return "命令不能为空"

        # 验证命令安全性
        validator = self._get_validator()
        result = validator.validate(command)

        if result.is_blocked:
            return f"命令被安全策略阻止: {result.message}"

        return None

    def execute(self, command: str, host: Optional[str] = None,
                timeout: int = 30, confirm: bool = False, **kwargs) -> ToolResult:
        """执行 SSH 命令"""
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

        # 验证命令安全性
        validator = self._get_validator()
        security_result = validator.validate(command)

        if security_result.level == SecurityLevel.BLOCKED:
            logger.warning(f"命令被阻止: {command}")
            return ToolResult(
                success=False,
                error=f"命令被安全策略阻止: {security_result.message}",
                metadata={"security_level": security_result.level.value}
            )

        if security_result.level == SecurityLevel.WARNING:
            if not confirm:
                return ToolResult(
                    success=False,
                    error=f"命令存在安全风险: {security_result.message}。请设置 confirm=true 以执行。",
                    metadata={"security_level": security_result.level.value}
                )
            logger.warning(f"用户确认执行危险命令: {command}")

        # 清理命令
        clean_command = validator.sanitize_command(command)

        try:
            logger.info(f"SSH 执行命令: {server.host} -> {clean_command[:100]}...")
            out, err, code = ssh.exec_command(server, clean_command, timeout=timeout)

            output = out.strip()
            if err.strip():
                output += f"\n[stderr] {err.strip()}"

            return ToolResult(
                success=(code == 0),
                output=output[:5000],
                error=err.strip() if code != 0 else "",
                metadata={
                    "host": server.host,
                    "exit_code": code,
                    "security_level": security_result.level.value,
                }
            )
        except Exception as e:
            logger.error(f"SSH 命令执行失败: {e}")
            return ToolResult(success=False, error=str(e))


class SSHTestConnectionTool(BaseTool):
    """SSH 连接测试工具"""
    name = "ssh_test_connection"
    description = "测试 SSH 连接是否正常"
    category = ToolCategory.SSH
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "host": {
                "type": "string",
                "description": "目标服务器地址"
            },
        },
    }

    def execute(self, host: Optional[str] = None, **kwargs) -> ToolResult:
        """测试 SSH 连接"""
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
            logger.info(f"测试 SSH 连接: {server.host}")
            out, err, code = ssh.exec_command(server, "echo 'connection test successful'", timeout=10)

            if code == 0 and "connection test successful" in out:
                return ToolResult(
                    success=True,
                    output=f"SSH 连接正常: {server.host}",
                    metadata={"host": server.host}
                )
            else:
                return ToolResult(
                    success=False,
                    error=f"SSH 连接异常: {err or out}",
                    metadata={"host": server.host, "exit_code": code}
                )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"SSH 连接测试失败: {e}",
                metadata={"host": server.host}
            )


class SSHGetSystemInfoTool(BaseTool):
    """SSH 获取系统信息工具"""
    name = "ssh_get_system_info"
    description = "获取远程服务器系统信息"
    category = ToolCategory.SSH
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "host": {
                "type": "string",
                "description": "目标服务器地址"
            },
        },
    }

    def execute(self, host: Optional[str] = None, **kwargs) -> ToolResult:
        """获取系统信息"""
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
            logger.info(f"获取系统信息: {server.host}")

            # 组合命令获取系统信息
            commands = [
                "uname -a",
                "cat /etc/os-release 2>/dev/null | head -5",
                "uptime",
                "free -h | head -3",
                "df -h / | tail -1",
                "nproc",
            ]
            combined_cmd = " && ".join(commands)

            out, err, code = ssh.exec_command(server, combined_cmd, timeout=30)

            if code == 0:
                return ToolResult(
                    success=True,
                    output=out.strip(),
                    metadata={"host": server.host}
                )
            else:
                return ToolResult(
                    success=False,
                    error=f"获取系统信息失败: {err}",
                    metadata={"host": server.host, "exit_code": code}
                )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"获取系统信息异常: {e}",
                metadata={"host": server.host}
            )
