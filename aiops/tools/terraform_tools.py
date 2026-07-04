"""Terraform 工具 - 基础设施即代码 (IaC)

Terraform 是 IaC 事实标准，支持 AWS/Azure/GCP/阿里云/华为云等。
实际使用：90%+ 多云环境使用 Terraform 管理基础设施。
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _tf_cmd(cmd: str, workdir: str = "", timeout: int = 60) -> ToolResult:
    try:
        cd = f"cd {workdir} && " if workdir else ""
        r = subprocess.run(f"{cd}{cmd}", shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class TerraformInit(BaseTool):
    """terraform init"""
    name = "terraform_init"
    description = "初始化 Terraform 工作目录"
    category = ToolCategory.IAC
    parameters = {"type": "object", "properties": {
        "workdir": {"type": "string", "description": "工作目录路径"},
    }, "required": ["workdir"]}

    def execute(self, workdir: str, **kwargs) -> ToolResult:
        return _tf_cmd("terraform init -no-color", workdir)


class TerraformPlan(BaseTool):
    """terraform plan"""
    name = "terraform_plan"
    description = "预览 Terraform 变更计划"
    category = ToolCategory.IAC
    parameters = {"type": "object", "properties": {
        "workdir": {"type": "string"},
        "var_file": {"type": "string", "description": "变量文件路径"},
    }, "required": ["workdir"]}

    def execute(self, workdir: str, var_file: str = "", **kwargs) -> ToolResult:
        cmd = "terraform plan -no-color -detailed-exitcode"
        if var_file:
            cmd += f" -var-file={var_file}"
        return _tf_cmd(cmd, workdir, timeout=120)


class TerraformApply(BaseTool):
    """terraform apply"""
    name = "terraform_apply"
    description = "应用 Terraform 变更"
    category = ToolCategory.IAC
    is_destructive = True
    requires_confirmation = True
    parameters = {"type": "object", "properties": {
        "workdir": {"type": "string"},
        "auto_approve": {"type": "boolean", "default": False},
    }, "required": ["workdir"]}

    def execute(self, workdir: str, auto_approve: bool = False, **kwargs) -> ToolResult:
        cmd = "terraform apply -no-color"
        if auto_approve:
            cmd += " -auto-approve"
        return _tf_cmd(cmd, workdir, timeout=300)


class TerraformState(BaseTool):
    """查询 Terraform 状态"""
    name = "terraform_state"
    description = "查看 Terraform 状态信息"
    category = ToolCategory.IAC
    parameters = {"type": "object", "properties": {
        "workdir": {"type": "string"},
        "action": {"type": "string", "description": "list/show", "default": "list"},
        "resource": {"type": "string", "description": "资源地址"},
    }, "required": ["workdir"]}

    def execute(self, workdir: str, action: str = "list", resource: str = "", **kwargs) -> ToolResult:
        if action == "show" and resource:
            return _tf_cmd(f"terraform state show {resource}", workdir)
        return _tf_cmd("terraform state list", workdir)


class TerraformOutput(BaseTool):
    """terraform output"""
    name = "terraform_output"
    description = "查看 Terraform 输出值"
    category = ToolCategory.IAC
    parameters = {"type": "object", "properties": {
        "workdir": {"type": "string"},
    }, "required": ["workdir"]}

    def execute(self, workdir: str, **kwargs) -> ToolResult:
        return _tf_cmd("terraform output -no-color", workdir)


class TerraformValidate(BaseTool):
    """terraform validate"""
    name = "terraform_validate"
    description = "验证 Terraform 配置语法"
    category = ToolCategory.IAC
    parameters = {"type": "object", "properties": {
        "workdir": {"type": "string"},
    }, "required": ["workdir"]}

    def execute(self, workdir: str, **kwargs) -> ToolResult:
        return _tf_cmd("terraform validate -no-color", workdir)
