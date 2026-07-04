"""Docker Swarm 集群管理工具"""
import logging
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


class SwarmInfo(BaseTool):
    """获取 Docker Swarm 集群信息"""
    name = "swarm_info"
    description = "获取 Docker Swarm 集群状态、节点数、管理器信息"
    category = ToolCategory.CONTAINER
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "filter": {"type": "string", "description": "过滤字段(self/nodes/services)", "default": "self"},
        },
    }

    def execute(self, filter: str = "self", **kwargs) -> ToolResult:
        cmd = f"docker info --format '{{{{.Swarm}}}}' && docker node ls"
        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)
            return ToolResult(success=(code == 0), output=out.strip()[:5000], error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SwarmServices(BaseTool):
    """列出 Docker Swarm 服务"""
    name = "swarm_services"
    description = "列出 Swarm 服务及状态(副本数/镜像/端口)"
    category = ToolCategory.CONTAINER
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "filter": {"type": "string", "description": "过滤条件"},
        },
    }

    def execute(self, filter: str = "", **kwargs) -> ToolResult:
        cmd = "docker service ls"
        if filter:
            cmd += f" --filter {filter}"
        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)
            return ToolResult(success=(code == 0), output=out.strip()[:5000], error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SwarmServiceScale(BaseTool):
    """扩缩容 Swarm 服务"""
    name = "swarm_service_scale"
    description = "调整 Swarm 服务副本数"
    category = ToolCategory.CONTAINER
    requires_ssh = True

    parameters = {
        "type": "object",
        "properties": {
            "service": {"type": "string", "description": "服务名称"},
            "replicas": {"type": "integer", "description": "目标副本数"},
        },
        "required": ["service", "replicas"],
    }

    def execute(self, service: str, replicas: int, **kwargs) -> ToolResult:
        cmd = f"docker service scale {service}={replicas}"
        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=30)
            return ToolResult(success=(code == 0), output=out.strip()[:5000], error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SwarmServiceLogs(BaseTool):
    """查看 Swarm 服务日志"""
    name = "swarm_service_logs"
    description = "获取 Swarm 服务日志"
    category = ToolCategory.LOG
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "service": {"type": "string", "description": "服务名称"},
            "tail": {"type": "integer", "description": "返回行数", "default": 100},
        },
        "required": ["service"],
    }

    def execute(self, service: str, tail: int = 100, **kwargs) -> ToolResult:
        cmd = f"docker service logs --tail {tail} --no-stream {service}"
        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)
            return ToolResult(success=(code == 0), output=out.strip()[:5000], error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SwarmNodeList(BaseTool):
    """列出 Swarm 节点"""
    name = "swarm_nodes"
    description = "列出 Swarm 集群节点及状态(Ready/Down/Manager/Worker)"
    category = ToolCategory.CONTAINER
    requires_ssh = True
    is_readonly = True

    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> ToolResult:
        cmd = "docker node ls"
        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)
            return ToolResult(success=(code == 0), output=out.strip()[:5000], error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))
