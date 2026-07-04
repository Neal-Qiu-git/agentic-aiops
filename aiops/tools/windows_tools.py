"""Windows 远程管理工具 - WinRM + PowerShell"""
import logging
import subprocess
from typing import Optional
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


class WinRMExec(BaseTool):
    """WinRM 远程执行 PowerShell"""
    name = "winrm_exec"
    description = "通过 WinRM 执行 PowerShell 命令"
    category = ToolCategory.REMOTE
    requires_ssh = False
    parameters = {
        "type": "object",
        "properties": {
            "host": {"type": "string", "description": "Windows 主机地址"},
            "user": {"type": "string", "description": "用户名"},
            "password": {"type": "string", "description": "密码"},
            "command": {"type": "string", "description": "PowerShell 命令"},
        },
        "required": ["host", "user", "password", "command"],
    }

    def execute(self, host: str, user: str, password: str, command: str, **kwargs) -> ToolResult:
        # 使用 sshpass + ssh 或者 python-winrm
        ps_cmd = f'powershell -Command "{command}"'
        cmd = f"ssh {user}@{host} '{ps_cmd}'"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class WinRMEventLog(BaseTool):
    """Windows 事件日志查询"""
    name = "winrm_eventlog"
    description = "查询 Windows 事件日志"
    category = ToolCategory.LOG
    requires_ssh = False
    parameters = {
        "type": "object",
        "properties": {
            "host": {"type": "string"},
            "user": {"type": "string"},
            "password": {"type": "string"},
            "log_name": {"type": "string", "description": "日志名称(System/Application/Security)", "default": "System"},
            "level": {"type": "string", "description": "级别(Error/Warning/Critical)", "default": "Error"},
            "count": {"type": "integer", "description": "返回条数", "default": 50},
        },
        "required": ["host", "user", "password"],
    }

    def execute(self, host: str, user: str, password: str, log_name: str = "System", level: str = "Error", count: int = 50, **kwargs) -> ToolResult:
        ps_cmd = f'Get-EventLog -LogName {log_name} -EntryType {level} -Newest {count} | Select-Object TimeGenerated,Source,Message | ConvertTo-Json'
        cmd = f"ssh {user}@{host} 'powershell -Command "{ps_cmd}"'"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class WinRMService(BaseTool):
    """Windows 服务管理"""
    name = "winrm_service"
    description = "管理 Windows 服务"
    category = ToolCategory.SYSTEM
    requires_ssh = False
    parameters = {
        "type": "object",
        "properties": {
            "host": {"type": "string"},
            "user": {"type": "string"},
            "password": {"type": "string"},
            "action": {"type": "string", "description": "操作(start/stop/restart/status)", "default": "status"},
            "service": {"type": "string", "description": "服务名称"},
        },
        "required": ["host", "user", "password", "service"],
    }

    def execute(self, host: str, user: str, password: str, service: str, action: str = "status", **kwargs) -> ToolResult:
        action_map = {"status": "Get-Service", "start": "Start-Service", "stop": "Stop-Service", "restart": "Restart-Service"}
        ps_cmd = f'{action_map.get(action, "Get-Service")} -Name {service} | ConvertTo-Json'
        cmd = f"ssh {user}@{host} 'powershell -Command "{ps_cmd}"'"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))
