"""云平台工具 - 支持 AWS, 阿里云, 腾讯云"""
import json
import logging
from typing import Optional, Dict, Any, List
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


class AWSCLI(BaseTool):
    """AWS CLI 工具"""
    name = "aws_cli"
    description = "AWS CLI 命令执行"
    category = ToolCategory.CLOUD_API
    requires_ssh = True

    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "AWS CLI 命令"},
            "region": {"type": "string", "description": "区域", "default": "us-east-1"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, region: str = "us-east-1", **kwargs) -> ToolResult:
        cmd = f"aws {command} --region {region} --output json"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=60)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:8000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class AliyunCLI(BaseTool):
    """阿里云 CLI 工具"""
    name = "aliyun_cli"
    description = "阿里云 CLI 命令执行"
    category = ToolCategory.CLOUD_API
    requires_ssh = True

    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "阿里云 CLI 命令"},
            "region": {"type": "string", "description": "区域", "default": "cn-hangzhou"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, region: str = "cn-hangzhou", **kwargs) -> ToolResult:
        cmd = f"aliyun {command} --region {region}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=60)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:8000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TencentCLI(BaseTool):
    """腾讯云 CLI 工具"""
    name = "tencent_cli"
    description = "腾讯云 CLI 命令执行"
    category = ToolCategory.CLOUD_API
    requires_ssh = True

    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "腾讯云 CLI 命令"},
            "region": {"type": "string", "description": "区域", "default": "ap-guangzhou"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, region: str = "ap-guangzhou", **kwargs) -> ToolResult:
        cmd = f"tccli {command} --region {region}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=60)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:8000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TerraformTool(BaseTool):
    """Terraform 工具"""
    name = "terraform"
    description = "Terraform 基础设施管理"
    category = ToolCategory.ORCHESTRATION
    requires_ssh = True
    is_readonly = False

    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "terraform 命令"},
            "workspace": {"type": "string", "description": "工作空间"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, workspace: str = "", **kwargs) -> ToolResult:
        cmd = f"terraform {command}"
        if workspace:
            cmd += f" -chdir={workspace}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=120)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:8000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class AnsibleTool(BaseTool):
    """Ansible 工具"""
    name = "ansible"
    description = "Ansible 自动化工具"
    category = ToolCategory.ORCHESTRATION
    requires_ssh = True
    is_readonly = False

    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "ansible 命令"},
            "inventory": {"type": "string", "description": "主机清单"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, inventory: str = "", **kwargs) -> ToolResult:
        cmd = f"ansible {command}"
        if inventory:
            cmd += f" -i {inventory}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=120)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:8000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class HelmTool(BaseTool):
    """Helm 工具"""
    name = "helm"
    description = "Helm K8s 包管理"
    category = ToolCategory.ORCHESTRATION
    requires_ssh = True

    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "helm 命令"},
            "namespace": {"type": "string", "description": "命名空间"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, namespace: str = "", **kwargs) -> ToolResult:
        cmd = f"helm {command}"
        if namespace:
            cmd += f" -n {namespace}"

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
