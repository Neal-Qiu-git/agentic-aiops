"""Docker 工具"""
import logging
from typing import Optional, Dict, Any, List
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


class DockerPS(BaseTool):
    """Docker 容器列表"""
    name = "docker_ps"
    description = "列出 Docker 容器"
    category = ToolCategory.CONTAINER
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "all": {"type": "boolean", "description": "显示所有容器", "default": True},
            "filter": {"type": "string", "description": "过滤条件"},
        },
    }

    def execute(self, all: bool = True, filter: str = "", **kwargs) -> ToolResult:
        cmd = "docker ps"
        if all:
            cmd += " -a"
        if filter:
            cmd += f" --filter {filter}"
        cmd += " --format 'table {{.ID}}\\t{{.Names}}\\t{{.Status}}\\t{{.Ports}}'"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class DockerLogs(BaseTool):
    """Docker 容器日志"""
    name = "docker_logs"
    description = "获取 Docker 容器日志"
    category = ToolCategory.CONTAINER
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "container": {"type": "string", "description": "容器名称或 ID"},
            "tail": {"type": "integer", "description": "返回最后N行", "default": 100},
            "since": {"type": "string", "description": "从指定时间开始"},
        },
        "required": ["container"],
    }

    def execute(self, container: str, tail: int = 100, since: str = "", **kwargs) -> ToolResult:
        cmd = f"docker logs {container} --tail {tail}"
        if since:
            cmd += f" --since {since}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=30)

            output = out.strip()
            if err.strip():
                output += f"\n[stderr] {err.strip()}"

            return ToolResult(
                success=(code == 0),
                output=output[:8000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class DockerInspect(BaseTool):
    """Docker 容器详情"""
    name = "docker_inspect"
    description = "获取 Docker 容器详细信息"
    category = ToolCategory.CONTAINER
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "container": {"type": "string", "description": "容器名称或 ID"},
        },
        "required": ["container"],
    }

    def execute(self, container: str, **kwargs) -> ToolResult:
        cmd = f"docker inspect {container}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:8000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class DockerStats(BaseTool):
    """Docker 资源统计"""
    name = "docker_stats"
    description = "获取 Docker 容器资源使用情况"
    category = ToolCategory.CONTAINER
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "container": {"type": "string", "description": "容器名称或 ID（可选，为空则显示所有）"},
            "no_stream": {"type": "boolean", "description": "不持续更新", "default": True},
        },
    }

    def execute(self, container: str = "", no_stream: bool = True, **kwargs) -> ToolResult:
        cmd = "docker stats"
        if container:
            cmd += f" {container}"
        if no_stream:
            cmd += " --no-stream"
        cmd += " --format 'table {{.Name}}\\t{{.CPUPerc}}\\t{{.MemUsage}}\\t{{.NetIO}}\\t{{.BlockIO}}'"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class DockerCompose(BaseTool):
    """Docker Compose 工具"""
    name = "docker_compose"
    description = "Docker Compose 管理"
    category = ToolCategory.CONTAINER
    requires_ssh = True

    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "docker-compose 命令"},
            "path": {"type": "string", "description": "docker-compose.yml 路径"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, path: str = "", **kwargs) -> ToolResult:
        cmd = "docker-compose"
        if path:
            cmd += f" -f {path}"
        cmd += f" {command}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=60)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class DockerNetwork(BaseTool):
    """Docker 网络管理"""
    name = "docker_network"
    description = "Docker 网络管理"
    category = ToolCategory.CONTAINER
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "docker network 命令", "default": "ls"},
        },
    }

    def execute(self, command: str = "ls", **kwargs) -> ToolResult:
        cmd = f"docker network {command}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class DockerVolume(BaseTool):
    """Docker 卷管理"""
    name = "docker_volume"
    description = "Docker 卷管理"
    category = ToolCategory.CONTAINER
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "docker volume 命令", "default": "ls"},
        },
    }

    def execute(self, command: str = "ls", **kwargs) -> ToolResult:
        cmd = f"docker volume {command}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))
