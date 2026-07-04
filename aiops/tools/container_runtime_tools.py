"""容器运行时工具 - containerd / Podman

containerd: K8s 默认容器运行时 (CNCF 毕业)
Podman: Red Hat 无守护进程容器 (Daemonless)
"""
import subprocess
from .base import BaseTool, ToolResult, ToolCategory


def _run(cmd: str, t: int = 20) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=t)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class ContainerdTool(BaseTool):
    """containerd 容器管理"""
    name = "containerd_manage"
    description = "containerd 容器运行时管理 (K8s 默认)"
    category = ToolCategory.CONTAINER
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "containers/tasks/images/namespace", "default": "containers"},
        "namespace": {"type": "string", "default": "k8s.io"},
    }}

    def execute(self, action: str = "containers", namespace: str = "k8s.io", **kw) -> ToolResult:
        cmds = {
            "containers": f"ctr -n {namespace} containers list 2>/dev/null",
            "tasks": f"ctr -n {namespace} tasks list 2>/dev/null",
            "images": f"ctr -n {namespace} images list 2>/dev/null",
            "namespace": "ctr namespaces list 2>/dev/null",
        }
        return _run(cmds.get(action, cmds["containers"]))


class PodmanTool(BaseTool):
    """Podman 容器管理"""
    name = "podman_manage"
    description = "Podman 无守护进程容器管理 (Daemonless)"
    category = ToolCategory.CONTAINER
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "ps/images/stats/ pods/top", "default": "ps"},
        "format": {"type": "string", "description": "json/table", "default": "json"},
    }}

    def execute(self, action: str = "ps", format: str = "json", **kw) -> ToolResult:
        cmds = {
            "ps": f"podman ps --format {format} 2>/dev/null || echo 'Podman not installed'",
            "images": f"podman images --format {format} 2>/dev/null",
            "stats": "podman stats --format json --no-stream 2>/dev/null",
            "pods": "podman pod ls --format json 2>/dev/null",
        }
        return _run(cmds.get(action, cmds["ps"]))
