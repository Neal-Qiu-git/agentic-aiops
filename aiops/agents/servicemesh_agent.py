"""ServiceMesh Agent - 服务网格专家"""
from .base import BaseAgent, AgentResult


class ServiceMeshAgent(BaseAgent):
    """ServiceMesh Agent - 负责服务网格管理"""

    name = "servicemesh"
    description = "ServiceMesh Agent - 服务网格（Istio/Linkerd）"
    role = "服务网格专家"
    task_description = "处理 Istio/Linkerd 服务网格配置、流量管理、可观测性、安全策略"
    tools = [
        "kubectl", "k8s_get_pods", "k8s_get_events",
        "ssh_exec", "http_get", "prometheus_query",
    ]
    max_steps = 12

    def run(self, task: str, context: dict = None) -> AgentResult:
        context = context or {}
        context["expertise"] = """你是服务网格专家：
1. Istio: Sidecar 注入/VirtualService/DestinationRule/Gateway
2. Linkerd: ServiceProfile/TLS/流量分割
3. 流量管理: 金丝雀发布/A-B测试/故障注入/超时重试
4. 安全: mTLS/JWT/RBAC/授权策略
5. 可观测性: 分布式追踪/指标/日志
6. 故障排查: Sidecar 代理问题/证书过期/配置冲突

执行流程：
1. 检查 mesh 控制面和数据面状态
2. 分析流量路由和策略配置
3. 排查 Sidecar 代理日志
4. 验证 mTLS 和安全策略
5. 优化流量管理和可观测性
"""
        return super().run(task, context)
