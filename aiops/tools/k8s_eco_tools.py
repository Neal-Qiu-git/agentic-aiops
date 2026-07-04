"""K8s 生态工具 - Helm / Harbor / Cert-Manager / MetalLB

Helm: K8s 包管理事实标准 (CNCF 毕业)
Harbor: K8s 容器镜像仓库 (CNCF 毕业)
Cert-Manager: K8s TLS 证书管理 (CNCF 孵化)
MetalLB: K8s 裸金属负载均衡 (CNCF 毕业)
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _k8s_cmd(cmd: str, timeout: int = 30) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class HelmList(BaseTool):
    """列出 Helm Releases"""
    name = "helm_list"
    description = "列出 Helm 安装的 releases (所有命名空间)"
    category = ToolCategory.K8S
    parameters = {"type": "object", "properties": {
        "namespace": {"type": "string", "description": "过滤命名空间"},
        "output": {"type": "string", "description": "json/table", "default": "json"},
    }}

    def execute(self, namespace: str = "", output: str = "json", **kwargs) -> ToolResult:
        ns = f"-A" if not namespace else f"-n {namespace}"
        return _k8s_cmd(f"helm list {ns} -o {output} 2>/dev/null || echo 'Helm not installed'")


class HelmStatus(BaseTool):
    """Helm Release 详情"""
    name = "helm_status"
    description = "查看 Helm Release 详细状态"
    category = ToolCategory.K8S
    parameters = {"type": "object", "properties": {
        "release": {"type": "string", "description": "Release 名称"},
        "namespace": {"type": "string", "default": "default"},
    }, "required": ["release"]}

    def execute(self, release: str, namespace: str = "default", **kwargs) -> ToolResult:
        return _k8s_cmd(f"helm status {release} -n {namespace} -o json")


class HelmHistory(BaseTool):
    """Helm Release 历史"""
    name = "helm_history"
    description = "查看 Helm Release 版本历史 (回溯依据)"
    category = ToolCategory.K8S
    parameters = {"type": "object", "properties": {
        "release": {"type": "string"},
        "namespace": {"type": "string", "default": "default"},
    }, "required": ["release"]}

    def execute(self, release: str, namespace: str = "default", **kwargs) -> ToolResult:
        return _k8s_cmd(f"helm history {release} -n {namespace} -o json")


class HelmRollback(BaseTool):
    """Helm Rollback"""
    name = "helm_rollback"
    description = "回滚 Helm Release 到指定版本"
    category = ToolCategory.K8S
    is_destructive = True
    requires_confirmation = True
    parameters = {"type": "object", "properties": {
        "release": {"type": "string"},
        "revision": {"type": "integer", "description": "目标版本号"},
        "namespace": {"type": "string", "default": "default"},
    }, "required": ["release", "revision"]}

    def execute(self, release: str, revision: int, namespace: str = "default", **kwargs) -> ToolResult:
        return _k8s_cmd(f"helm rollback {release} {revision} -n {namespace}", timeout=120)


class HarborProjects(BaseTool):
    """Harbor 镜像仓库项目"""
    name = "harbor_projects"
    description = "列出 Harbor 镜像仓库项目和仓库"
    category = ToolCategory.CONTAINER
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "projects/repositories/artifacts", "default": "projects"},
        "project": {"type": "string", "description": "项目名"},
    }}

    def execute(self, action: str = "projects", project: str = "", **kwargs) -> ToolResult:
        import os
        url = os.environ.get("HARBOR_URL", "https://harbor.example.com")
        user = os.environ.get("HARBOR_USER", "admin")
        secret = os.environ.get("HARBOR_SECRET", "")
        auth = f"-u {user}:{secret}" if secret else ""
        if action == "repositories" and project:
            return _k8s_cmd(f"curl -s {auth} '{url}/api/v2.0/projects/{project}/repositories' 2>/dev/null || echo 'Harbor not reachable'")
        if action == "artifacts" and project:
            return _k8s_cmd(f"curl -s {auth} '{url}/api/v2.0/projects/{project}/repositories?page_size=10' 2>/dev/null")
        return _k8s_cmd(f"curl -s {auth} '{url}/api/v2.0/projects' 2>/dev/null")


class CertManagerCerts(BaseTool):
    """Cert-Manager 证书管理"""
    name = "certmanager_certs"
    description = "查看 Cert-Manager 管理的 TLS 证书"
    category = ToolCategory.SECURITY
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "certs/issuers/challenges", "default": "certs"},
        "namespace": {"type": "string", "default": ""},
    }}

    def execute(self, action: str = "certs", namespace: str = "", **kwargs) -> ToolResult:
        ns = f"-n {namespace}" if namespace else "-A"
        cmds = {
            "certs": f"kubectl get certificates {ns} -o json 2>/dev/null",
            "issuers": f"kubectl get issuers {ns} -o json 2>/dev/null || kubectl get clusterissuers -o json 2>/dev/null",
            "challenges": f"kubectl get challenges {ns} -o json 2>/dev/null",
        }
        return _k8s_cmd(cmds.get(action, cmds["certs"]))


class MetalLBBGP(BaseTool):
    """MetalLB BGP/IP 地址池"""
    name = "metallb_status"
    description = "查看 MetalLB 地址池和 BGP 对等体状态"
    category = ToolCategory.UTILITY
    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> ToolResult:
        return _k8s_cmd("kubectl get IPAddressPool -A -o json 2>/dev/null; echo '---'; kubectl get BGPPeer -A -o json 2>/dev/null || echo 'MetalLB not found'")
