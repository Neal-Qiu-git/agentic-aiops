"""配置管理工具 - Ansible + SonarQube

Ansible: 最流行的无代理配置管理 (Red Hat)
SonarQube: 代码质量/安全扫描标准
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _run_cmd(cmd: str, timeout: int = 30) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class AnsibleAdHoc(BaseTool):
    """Ansible Ad-Hoc 命令"""
    name = "ansible_adhoc"
    description = "执行 Ansible Ad-Hoc 命令 (无 Playbook)"
    category = ToolCategory.ORCHESTRATION
    parameters = {"type": "object", "properties": {
        "hosts": {"type": "string", "description": "目标主机/组 (如 webserver, db-server)"},
        "module": {"type": "string", "description": "模块名 (ping/shell/command/service/yum/apt/copy)", "default": "ping"},
        "args": {"type": "string", "description": "模块参数"},
        "inventory": {"type": "string", "description": "inventory 文件路径"},
    }, "required": ["hosts", "module"]}

    def execute(self, hosts: str, module: str = "ping", args: str = "",
                inventory: str = "", **kwargs) -> ToolResult:
        cmd = f"ansible {hosts} -m {module}"
        if args:
            cmd += f" -a '{args}'"
        if inventory:
            cmd += f" -i {inventory}"
        cmd += " 2>/dev/null || echo 'Ansible not installed'"
        return _run_cmd(cmd, timeout=60)


class AnsiblePlaybook(BaseTool):
    """执行 Ansible Playbook"""
    name = "ansible_playbook"
    description = "执行 Ansible Playbook 自动化编排"
    category = ToolCategory.ORCHESTRATION
    is_destructive = True
    requires_confirmation = True
    parameters = {"type": "object", "properties": {
        "playbook": {"type": "string", "description": "Playbook 文件路径"},
        "inventory": {"type": "string", "description": "inventory 文件路径"},
        "tags": {"type": "string", "description": "只执行指定 tag"},
        "check": {"type": "boolean", "description": "Dry-run 模式", "default": False},
    }, "required": ["playbook"]}

    def execute(self, playbook: str, inventory: str = "", tags: str = "",
                check: bool = False, **kwargs) -> ToolResult:
        cmd = f"ansible-playbook {playbook}"
        if inventory:
            cmd += f" -i {inventory}"
        if tags:
            cmd += f" --tags {tags}"
        if check:
            cmd += " --check --diff"
        cmd += " 2>/dev/null || echo 'Ansible not installed'"
        return _run_cmd(cmd, timeout=120)


class AnsibleInventory(BaseTool):
    """查询 Ansible Inventory"""
    name = "ansible_inventory"
    description = "列出 Ansible inventory 主机和组"
    category = ToolCategory.ORCHESTRATION
    parameters = {"type": "object", "properties": {
        "inventory": {"type": "string", "description": "inventory 文件/目录"},
        "list": {"type": "boolean", "description": "列出所有主机", "default": True},
    }}

    def execute(self, inventory: str = "", list: bool = True, **kwargs) -> ToolResult:
        cmd = "ansible-inventory --list 2>/dev/null"
        if inventory:
            cmd = f"ansible-inventory -i {inventory} --list 2>/dev/null"
        return _run_cmd(cmd)


class SonarQubeScan(BaseTool):
    """SonarQube 代码质量扫描"""
    name = "sonarqube_scan"
    description = "运行 SonarQube Scanner 扫描代码质量和安全"
    category = ToolCategory.CICD
    parameters = {"type": "object", "properties": {
        "project_key": {"type": "string", "description": "SonarQube 项目 Key"},
        "sources": {"type": "string", "description": "源码目录", "default": "."},
        "language": {"type": "string", "description": "编程语言"},
    }, "required": ["project_key"]}

    def execute(self, project_key: str, sources: str = ".", language: str = "", **kwargs) -> ToolResult:
        cmd = (f"sonar-scanner -Dsonar.projectKey={project_key} "
               f"-Dsonar.sources={sources} -Dsonar.host.url=${{SONAR_HOST_URL}} "
               f"-Dsonar.login=${{SONAR_TOKEN}} 2>/dev/null || echo 'sonar-scanner not installed'")
        if language:
            cmd = cmd.replace("-Dsonar.sources=", f"-Dsonar.language={language} -Dsonar.sources=")
        return _run_cmd(cmd, timeout=120)


class SonarQubeStatus(BaseTool):
    """SonarQube 项目状态"""
    name = "sonarqube_status"
    description = "查询 SonarQube 项目质量状态 (bugs/vulnerabilities/coverage)"
    category = ToolCategory.CICD
    parameters = {"type": "object", "properties": {
        "project_key": {"type": "string", "description": "项目 Key"},
    }, "required": ["project_key"]}

    def execute(self, project_key: str, **kwargs) -> ToolResult:
        import os
        url = os.environ.get("SONAR_HOST_URL", "http://localhost:9000")
        token = os.environ.get("SONAR_TOKEN", "")
        auth = f"-u {token}:" if token else ""
        return _run_cmd(f"curl -s {auth} '{url}/api/measures/component?component={project_key}&metricKeys=bugs,vulnerabilities,code_smells,coverage,ncloc,duplicated_lines_density' 2>/dev/null")
