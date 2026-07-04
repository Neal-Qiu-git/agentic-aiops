"""容器安全工具 - Trivy / Falco / OPA

Trivy: CNCF 毕业项目，漏洞扫描事实标准
Falco: CNCF 毕业项目，运行时安全
OPA/Gatekeeper: CNCF 毕业项目，策略引擎
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _sec_cmd(cmd: str, timeout: int = 60) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:10000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class TrivyScan(BaseTool):
    """Trivy 漏洞扫描"""
    name = "trivy_scan"
    description = "使用 Trivy 扫描镜像/文件系统/仓库漏洞"
    category = ToolCategory.SECURITY
    parameters = {"type": "object", "properties": {
        "target": {"type": "string", "description": "扫描目标 (镜像名/路径/仓库URL)"},
        "scan_type": {"type": "string", "description": "image/fs/repo/config", "default": "image"},
        "severity": {"type": "string", "description": "严重级别过滤", "default": "HIGH,CRITICAL"},
        "format": {"type": "string", "description": "json/table", "default": "json"},
    }, "required": ["target"]}

    def execute(self, target: str, scan_type: str = "image",
                severity: str = "HIGH,CRITICAL", format: str = "json", **kwargs) -> ToolResult:
        cmd = f"trivy {scan_type} --severity {severity} --format {format} {target}"
        return _sec_cmd(cmd, timeout=120)


class TrivyRepo(BaseTool):
    """扫描 Git 仓库"""
    name = "trivy_repo"
    description = "扫描 Git 仓库的代码安全和配置问题"
    category = ToolCategory.SECURITY
    parameters = {"type": "object", "properties": {
        "repo_url": {"type": "string"},
        "branch": {"type": "string", "default": "main"},
    }, "required": ["repo_url"]}

    def execute(self, repo_url: str, branch: str = "main", **kwargs) -> ToolResult:
        return _sec_cmd(f"trivy repo --branch {branch} --severity HIGH,CRITICAL {repo_url}", timeout=180)


class FalcoRules(BaseTool):
    """Falco 规则管理"""
    name = "falco_rules"
    description = "查询 Falco 运行时安全规则和告警"
    category = ToolCategory.SECURITY
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/alerts/validate", "default": "list"},
        "rules_file": {"type": "string", "description": "规则文件路径 (验证时)"},
    }}

    def execute(self, action: str = "list", rules_file: str = "", **kwargs) -> ToolResult:
        if action == "validate" and rules_file:
            return _sec_cmd(f"falco --validate {rules_file}")
        if action == "alerts":
            return _sec_cmd("falcosidekick --list 2>/dev/null || journalctl -u falco --no-pager -n 50 2>/dev/null || echo 'Falco not running locally'")
        # list rules
        return _sec_cmd("falco --list 2>/dev/null || ls /etc/falco/rules.d/ 2>/dev/null || echo 'Falco rules not found locally'")


class OPAEvaluate(BaseTool):
    """OPA 策略评估"""
    name = "opa_evaluate"
    description = "使用 OPA/Gatekeeper 评估策略"
    category = ToolCategory.SECURITY
    parameters = {"type": "object", "properties": {
        "policy": {"type": "string", "description": "策略路径 (如 data.kubernetes.admission)"},
        "input": {"type": "string", "description": "输入 JSON"},
        "data_file": {"type": "string", "description": "数据文件路径"},
    }, "required": ["policy"]}

    def execute(self, policy: str, input: str = "", data_file: str = "", **kwargs) -> ToolResult:
        cmd = f"opa eval {policy}"
        if data_file:
            cmd += f" -d {data_file}"
        if input:
            cmd += f" -I '{input}'"
        return _sec_cmd(cmd)


class KubeBench(BaseTool):
    """CIS Kubernetes 基准检查"""
    name = "kube_bench"
    description = "运行 kube-bench 进行 K8s CIS 基准安全检查"
    category = ToolCategory.SECURITY
    parameters = {"type": "object", "properties": {
        "target": {"type": "string", "description": "master/node/all", "default": "all"},
    }}

    def execute(self, target: str = "all", **kwargs) -> ToolResult:
        return _sec_cmd(f"kube-bench {target} --json", timeout=120)


class KubescapeScan(BaseTool):
    """Kubescape 安全扫描"""
    name = "kubescape_scan"
    description = "Kubescape K8s 安全合规扫描 (NSA/CISA 框架)"
    category = ToolCategory.SECURITY
    parameters = {"type": "object", "properties": {
        "framework": {"type": "string", "description": "nsa/cisa/mitre/pci-dss", "default": "nsa"},
        "format": {"type": "string", "description": "json/table", "default": "json"},
    }}

    def execute(self, framework: str = "nsa", format: str = "json", **kwargs) -> ToolResult:
        return _sec_cmd(f"kubescape scan --framework {framework} --format {format}", timeout=180)
