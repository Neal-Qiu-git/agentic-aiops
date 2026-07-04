"""多云平台工具 - AWS/Azure/阿里云/腾讯云/华为云"""
import json
import logging
import subprocess
from typing import Optional
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _run_cli(cmd: str, timeout: int = 30) -> ToolResult:
    """执行 CLI 命令"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
    except subprocess.TimeoutExpired:
        return ToolResult(success=False, error=f"命令超时 ({timeout}s)")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class AzureCLI(BaseTool):
    """Azure CLI 工具"""
    name = "azure_cli"
    description = "Azure CLI 命令执行"
    category = ToolCategory.CLOUD_API
    requires_ssh = True
    parameters = {"type": "object", "properties": {"command": {"type": "string"}, "subscription": {"type": "string"}}, "required": ["command"]}

    def execute(self, command: str, subscription: str = "", **kwargs) -> ToolResult:
        cmd = f"az {command} -o json"
        if subscription:
            cmd += f" --subscription {subscription}"
        return _run_cli(cmd)


class AliyunCLI(BaseTool):
    """阿里云 CLI 工具"""
    name = "aliyun_cli"
    description = "阿里云 CLI 命令执行"
    category = ToolCategory.CLOUD_API
    requires_ssh = True
    parameters = {"type": "object", "properties": {"command": {"type": "string"}, "region": {"type": "string", "default": "cn-hangzhou"}}, "required": ["command"]}

    def execute(self, command: str, region: str = "cn-hangzhou", **kwargs) -> ToolResult:
        cmd = f"aliyun {command} --region {region} --output json"
        return _run_cli(cmd)


class TencentCLI(BaseTool):
    """腾讯云 CLI 工具"""
    name = "tencent_cli"
    description = "腾讯云 CLI 命令执行"
    category = ToolCategory.CLOUD_API
    requires_ssh = True
    parameters = {"type": "object", "properties": {"command": {"type": "string"}, "region": {"type": "string", "default": "ap-guangzhou"}}, "required": ["command"]}

    def execute(self, command: str, region: str = "ap-guangzhou", **kwargs) -> ToolResult:
        cmd = f"tccli {command} --region {region} --output json"
        return _run_cli(cmd)


class HuaweiCLI(BaseTool):
    """华为云 CLI 工具"""
    name = "huawei_cli"
    description = "华为云 CLI 命令执行"
    category = ToolCategory.CLOUD_API
    requires_ssh = True
    parameters = {"type": "object", "properties": {"command": {"type": "string"}, "region": {"type": "string", "default": "cn-north-4"}}, "required": ["command"]}

    def execute(self, command: str, region: str = "cn-north-4", **kwargs) -> ToolResult:
        cmd = f"hcloud {command} --region {region} --output json"
        return _run_cli(cmd)
