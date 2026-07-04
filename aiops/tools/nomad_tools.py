"""HashiCorp Nomad 工具"""
import logging
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


class NomadJobs(BaseTool):
    """列出 Nomad 作业"""
    name = "nomad_jobs"
    description = "列出 Nomad 集群中的所有作业及状态"
    category = ToolCategory.ORCHESTRATION
    requires_ssh = True
    is_readonly = True

    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> ToolResult:
        cmd = "nomad job status"
        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)
            return ToolResult(success=(code == 0), output=out.strip()[:5000], error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class NomadJobDetail(BaseTool):
    """查看 Nomad 作业详情"""
    name = "nomad_job_detail"
    description = "获取 Nomad 作业详细信息(分配/任务组/约束)"
    category = ToolCategory.ORCHESTRATION
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "job": {"type": "string", "description": "作业名称"},
        },
        "required": ["job"],
    }

    def execute(self, job: str, **kwargs) -> ToolResult:
        cmd = f"nomad job status {job}"
        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)
            return ToolResult(success=(code == 0), output=out.strip()[:5000], error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class NomadNodes(BaseTool):
    """列出 Nomad 节点"""
    name = "nomad_nodes"
    description = "列出 Nomad 集群节点及状态"
    category = ToolCategory.ORCHESTRATION
    requires_ssh = True
    is_readonly = True

    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> ToolResult:
        cmd = "nomad node status"
        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)
            return ToolResult(success=(code == 0), output=out.strip()[:5000], error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class NomadAllocs(BaseTool):
    """列出 Nomad 分配"""
    name = "nomad_allocs"
    description = "列出 Nomad 作业的分配(Allocation)状态"
    category = ToolCategory.ORCHESTRATION
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "job": {"type": "string", "description": "作业名称(可选)"},
        },
    }

    def execute(self, job: str = "", **kwargs) -> ToolResult:
        cmd = f"nomad alloc status {job}" if job else "nomad alloc list"
        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=15)
            return ToolResult(success=(code == 0), output=out.strip()[:5000], error=err.strip() if code != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))
