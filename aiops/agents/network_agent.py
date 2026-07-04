"""Network Agent - 网络运维专家"""
from .base import BaseAgent, AgentResult


class NetworkAgent(BaseAgent):
    """Network Agent - 负责网络设备和策略管理"""

    name = "network"
    description = "Network Agent - 网络运维（防火墙/负载均衡/DNS/VLAN/SDN）"
    role = "网络运维专家"
    task_description = "处理网络设备管理、防火墙策略、负载均衡配置、DNS 管理、网络故障排查"
    tools = [
        "ssh_exec", "http_get", "prometheus_query",
    ]
    max_steps = 12

    def run(self, task: str, context: dict = None) -> AgentResult:
        context = context or {}
        context["expertise"] = """你是网络运维专家：
1. 防火墙: iptables/nftables/firewalld/华为USG/思科ASA
2. 负载均衡: Nginx/HAProxy/ALB/CLB/ELB
3. DNS: BIND/CoreDNS/dnsmasq/Route53
4. VLAN/VXLAN: 网络隔离/隧道
5. VPN: IPSec/WireGuard/OpenVPN
6. SDN: OpenFlow/SDN 控制器
7. 网络诊断: ping/traceroute/mtr/tcpdump/iftop
8. 带宽管理: QoS/限流/优先级

执行流程：
1. 使用 ping/traceroute/mtr 诊断连通性
2. 检查防火墙规则和路由表
3. 分析网络流量和带宽使用
4. 排查 DNS 解析和负载均衡配置
5. 给出网络优化和安全加固建议
"""
        return super().run(task, context)
