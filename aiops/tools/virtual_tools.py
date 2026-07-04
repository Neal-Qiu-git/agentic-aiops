"""虚拟化工具 - VMware/KVM/Xen"""
import json
import logging
import subprocess
from typing import Optional
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _virt_cmd(cmd: str, timeout: int = 20) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class VMwareTool(BaseTool):
    """VMware vSphere 管理"""
    name = "vmware_manage"
    description = "VMware vSphere/ESXi 虚拟机管理"
    category = ToolCategory.UTILITY
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "list/status/top/stats", "default": "list"}, "host": {"type": "string"}, "user": {"type": "string"}, "password": {"type": "string"}}}

    def execute(self, action: str = "list", host: str = "", user: str = "", password: str = "", **kwargs) -> ToolResult:
        if action == "list" and host:
            return _virt_cmd(f"govc ls /vm 2>/dev/null || echo 'govc not installed'")
        elif action == "status":
            return _virt_cmd("vim-cmd vmsvc/getallvms 2>/dev/null || echo 'ESXi CLI not available'")
        elif action == "stats":
            return _virt_cmd("esxtop -b -n 1 2>/dev/null | head -30 || echo 'esxtop not available'")
        return ToolResult(success=False, error="Invalid params")


class LibvirtTool(BaseTool):
    """KVM/libvirt 虚拟机管理"""
    name = "libvirt_manage"
    description = "KVM/QEMU/libvirt 虚拟机管理"
    category = ToolCategory.UTILITY
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "list/start/stop/status/info/disk/net", "default": "list"}, "vm_name": {"type": "string"}, "host": {"type": "string"}}}

    def execute(self, action: str = "list", vm_name: str = "", host: str = "", **kwargs) -> ToolResult:
        prefix = f"ssh {host} " if host else ""
        cmds = {
            "list": f"{prefix}virsh list --all 2>/dev/null",
            "status": f"{prefix}virsh list --running 2>/dev/null",
            "info": f"{prefix}virsh dominfo {vm_name} 2>/dev/null" if vm_name else "",
            "disk": f"{prefix}virsh domblklist {vm_name} 2>/dev/null" if vm_name else "",
            "net": f"{prefix}virsh net-list --all 2>/dev/null",
            "start": f"{prefix}virsh start {vm_name} 2>/dev/null" if vm_name else "",
            "stop": f"{prefix}virsh shutdown {vm_name} 2>/dev/null" if vm_name else "",
        }
        cmd = cmds.get(action, cmds["list"])
        if not cmd:
            return ToolResult(success=False, error=f"vm_name required for {action}")
        return _virt_cmd(cmd, timeout=30)


class ProxmoxTool(BaseTool):
    """Proxmox VE 管理"""
    name = "proxmox_manage"
    description = "Proxmox VE 虚拟化平台管理"
    category = ToolCategory.UTILITY
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "list/status/cluster", "default": "list"}}}

    def execute(self, action: str = "list", **kwargs) -> ToolResult:
        cmds = {
            "list": "pvesh get /nodes/$(hostname)/qemu --output-format json 2>/dev/null || pct list 2>/dev/null",
            "status": "pveversion 2>/dev/null; pvesm status 2>/dev/null",
            "cluster": "pveam cmdb 2>/dev/null; ha-manager status 2>/dev/null",
        }
        return _virt_cmd(cmds.get(action, cmds["list"]))
