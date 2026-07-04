"""GitOps 工具 - ArgoCD / FluxCD

ArgoCD 是 K8s GitOps 标准工具，FluxCD 是 CNCF 毕业项目。
实际使用：80%+ K8s 环境采用 GitOps 模式部署。
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _argocd_cmd(cmd: str, timeout: int = 30) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class ArgoCDApps(BaseTool):
    """列出/查询 ArgoCD 应用"""
    name = "argocd_apps"
    description = "列出 ArgoCD 管理的 GitOps 应用"
    category = ToolCategory.GITOPS
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/get/sync/history", "default": "list"},
        "name": {"type": "string", "description": "应用名称"},
        "project": {"type": "string", "description": "ArgoCD 项目"},
    }}

    def execute(self, action: str = "list", name: str = "", project: str = "", **kwargs) -> ToolResult:
        if action == "get" and name:
            return _argocd_cmd(f"argocd app get {name} -o json")
        if action == "sync" and name:
            return _argocd_cmd(f"argocd app sync {name}", timeout=120)
        if action == "history" and name:
            return _argocd_cmd(f"argocd app history {name} -o json")
        cmd = "argocd app list -o json"
        if project:
            cmd += f" --project {project}"
        return _argocd_cmd(cmd)


class ArgoCDProjects(BaseTool):
    """ArgoCD 项目管理"""
    name = "argocd_projects"
    description = "列出 ArgoCD 项目"
    category = ToolCategory.GITOPS
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/get", "default": "list"},
        "name": {"type": "string"},
    }}

    def execute(self, action: str = "list", name: str = "", **kwargs) -> ToolResult:
        if action == "get" and name:
            return _argocd_cmd(f"argocd proj get {name} -o json")
        return _argocd_cmd("argocd proj list -o json")


class ArgoCDRepositories(BaseTool):
    """ArgoCD 仓库管理"""
    name = "argocd_repos"
    description = "列出 ArgoCD 配置的 Git 仓库"
    category = ToolCategory.GITOPS
    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> ToolResult:
        return _argocd_cmd("argocd repo list -o json")


class FluxGetResources(BaseTool):
    """查询 FluxCD 资源"""
    name = "flux_get_resources"
    description = "查询 FluxCD 管理的 GitOps 资源"
    category = ToolCategory.GITOPS
    parameters = {"type": "object", "properties": {
        "resource_type": {"type": "string", "description": "kustomizations/helmreleases/sources", "default": "kustomizations"},
        "namespace": {"type": "string", "description": "命名空间"},
    }}

    def execute(self, resource_type: str = "kustomizations", namespace: str = "", **kwargs) -> ToolResult:
        ns = f"-n {namespace}" if namespace else "-A"
        return _argocd_cmd(f"flux get {resource_type} {ns} -o json")


class FluxReconcile(BaseTool):
    """触发 FluxCD 重同步"""
    name = "flux_reconcile"
    description = "强制 FluxCD 资源重新同步"
    category = ToolCategory.GITOPS
    is_destructive = True
    requires_confirmation = True
    parameters = {"type": "object", "properties": {
        "resource_type": {"type": "string", "description": "kustomization/helmrelease"},
        "name": {"type": "string"},
        "namespace": {"type": "string"},
    }, "required": ["resource_type", "name"]}

    def execute(self, resource_type: str, name: str, namespace: str = "default", **kwargs) -> ToolResult:
        return _argocd_cmd(f"flux reconcile {resource_type} {name} -n {namespace}", timeout=120)
