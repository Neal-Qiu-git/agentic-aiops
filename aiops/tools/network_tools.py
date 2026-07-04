"""网络工具 - 防火墙/负载均衡/DNS/VPN"""
import logging
import subprocess
from typing import Optional
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _net_cmd(cmd: str, timeout: int = 15) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class FirewallTool(BaseTool):
    """防火墙管理"""
    name = "firewall_manage"
    description = "管理防火墙规则(iptables/firewalld/nftables)"
    category = ToolCategory.SECURITY
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "list/status/add/del", "default": "list"}, "rule": {"type": "string", "description": "规则(添加时)"}}, "required": ["action"]}

    def execute(self, action: str = "list", rule: str = "", **kwargs) -> ToolResult:
        if action == "list":
            return _net_cmd("iptables -L -n --line-numbers 2>/dev/null || firewall-cmd --list-all 2>/dev/null || nft list ruleset 2>/dev/null")
        elif action == "status":
            return _net_cmd("systemctl is-active firewalld 2>/dev/null; systemctl is-active iptables 2>/dev/null")
        elif action == "add" and rule:
            return _net_cmd(f"firewall-cmd --permanent --add-rich-rule='{rule}' && firewall-cmd --reload")
        elif action == "del" and rule:
            return _net_cmd(f"firewall-cmd --permanent --remove-rich-rule='{rule}' && firewall-cmd --reload")
        return ToolResult(success=False, error="Invalid action")


class LoadBalancerTool(BaseTool):
    """负载均衡状态查询"""
    name = "loadbalancer_status"
    description = "查询负载均衡状态(Nginx/HAProxy/云LB)"
    category = ToolCategory.NETWORK
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"type": {"type": "string", "description": "nginx/haproxy", "default": "nginx"}}}

    def execute(self, type: str = "nginx", **kwargs) -> ToolResult:
        if type == "nginx":
            return _net_cmd("nginx -T 2>/dev/null | head -200")
        elif type == "haproxy":
            return _net_cmd("echo 'show stat' | socat /var/run/haproxy/admin.sock stdio 2>/dev/null || haproxy -c 2>/dev/null")
        return ToolResult(success=False, error=f"Unsupported type: {type}")


class DNSTool(BaseTool):
    """DNS 管理"""
    name = "dns_manage"
    description = "DNS 解析和管理"
    category = ToolCategory.NETWORK
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"domain": {"type": "string"}, "action": {"type": "string", "description": "resolve/zone/status", "default": "resolve"}}}

    def execute(self, domain: str = "", action: str = "resolve", **kwargs) -> ToolResult:
        if action == "resolve" and domain:
            return _net_cmd(f"dig +short {domain} 2>/dev/null || nslookup {domain} 2>/dev/null")
        elif action == "status":
            return _net_cmd("cat /etc/resolv.conf 2>/dev/null; systemctl is-active named 2>/dev/null || systemctl is-active bind9 2>/dev/null")
        elif action == "zone" and domain:
            return _net_cmd(f"dig {domain} ANY +noall +answer 2>/dev/null")
        return ToolResult(success=False, error="Invalid params")


class NetworkDiagTool(BaseTool):
    """网络诊断"""
    name = "network_diag"
    description = "网络连通性诊断(ping/traceroute/mtr/iftop)"
    category = ToolCategory.NETWORK
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"target": {"type": "string"}, "tool": {"type": "string", "description": "ping/traceroute/mtr/iftop", "default": "ping"}, "count": {"type": "integer", "default": 5}}}

    def execute(self, target: str, tool: str = "ping", count: int = 5, **kwargs) -> ToolResult:
        cmds = {
            "ping": f"ping -c {count} {target}",
            "traceroute": f"traceroute -m 15 {target}",
            "mtr": f"mtr -r -c {count} {target}",
            "iftop": "iftop -t -s 5 2>/dev/null | head -30",
        }
        return _net_cmd(cmds.get(tool, cmds["ping"]), timeout=30)


class VPNTool(BaseTool):
    """VPN 状态查询"""
    name = "vpn_status"
    description = "查询 VPN 连接状态"
    category = ToolCategory.NETWORK
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"type": {"type": "string", "description": "wireguard/ipsec/openvpn", "default": "wireguard"}}}

    def execute(self, type: str = "wireguard", **kwargs) -> ToolResult:
        if type == "wireguard":
            return _net_cmd("wg show 2>/dev/null || echo 'WireGuard not installed'")
        elif type == "ipsec":
            return _net_cmd("ipsec status 2>/dev/null || strongswan status 2>/dev/null")
        elif type == "openvpn":
            return _net_cmd("systemctl status openvpn@* 2>/dev/null; cat /var/log/openvpn/*.log 2>/dev/null | tail -20")
        return ToolResult(success=False, error=f"Unsupported: {type}")
