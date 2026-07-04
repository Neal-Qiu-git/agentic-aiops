"""扩展中间件工具 - Pulsar / NATS / Traefik / HAProxy / Consul

Apache Pulsar: 新一代消息队列 (多租户 + 分层存储)
NATS: 云原生消息系统 (CNCF 毕业项目)
Traefik: 云原生反向代理 (CNCF 孵化项目)
HAProxy: 高性能负载均衡
Consul: 服务发现 + 配置中心 (CNCF 项目)
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _mw_cmd(cmd: str, timeout: int = 15) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class PulsarTool(BaseTool):
    """Apache Pulsar 消息队列"""
    name = "pulsar_manage"
    description = "Pulsar 集群管理: topic/subscription/stats"
    category = ToolCategory.MESSAGE_QUEUE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "topics/subscriptions/stats/cluster", "default": "topics"},
        "topic": {"type": "string"},
        "tenant": {"type": "string", "default": "public"},
        "namespace": {"type": "string", "default": "default"},
    }}

    def execute(self, action: str = "topics", topic: str = "", tenant: str = "public",
                namespace: str = "default", **kwargs) -> ToolResult:
        import os
        url = os.environ.get("PULSAR_URL", "http://localhost:8080")
        if action == "topics":
            return _mw_cmd(f"curl -s '{url}/admin/v2/{tenant}/{namespace}/topics'")
        if action == "subscriptions" and topic:
            return _mw_cmd(f"curl -s '{url}/admin/v2/{tenant}/{namespace}/{topic}/subscriptions'")
        if action == "stats" and topic:
            return _mw_cmd(f"curl -s '{url}/admin/v2/{tenant}/{namespace}/{topic}/stats'")
        if action == "cluster":
            return _mw_cmd(f"curl -s '{url}/admin/v2/clusters'")
        return ToolResult(success=False, error="参数不足")


class NATSTool(BaseTool):
    """NATS 消息系统"""
    name = "nats_manage"
    description = "NATS/JetStream 管理: streams/consumers/health"
    category = ToolCategory.MESSAGE_QUEUE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "info/streams/consumers/health", "default": "info"},
        "stream": {"type": "string"},
    }}

    def execute(self, action: str = "info", stream: str = "", **kwargs) -> ToolResult:
        if action == "info":
            return _mw_cmd("nats server info 2>/dev/null || echo 'nats CLI not found'")
        if action == "streams":
            cmd = f"nats stream ls 2>/dev/null"
            return _mw_cmd(cmd)
        if action == "consumers" and stream:
            return _mw_cmd(f"nats consumer ls {stream} 2>/dev/null")
        if action == "health":
            import os
            url = os.environ.get("NATS_URL", "http://localhost:8222")
            return _mw_cmd(f"curl -s '{url}/healthz'")
        return ToolResult(success=False, error="参数不足")


class TraefikTool(BaseTool):
    """Traefik 反向代理"""
    name = "traefik_manage"
    description = "Traefik 路由/中间件/健康查询"
    category = ToolCategory.REVERSE_PROXY
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "overview/routers/middlewares/health/rawdata", "default": "overview"},
    }}

    def execute(self, action: str = "overview", **kwargs) -> ToolResult:
        import os
        url = os.environ.get("TRAEFIK_URL", "http://localhost:8080")
        endpoints = {
            "routers": "/api/http/routers",
            "middlewares": "/api/http/middlewares",
            "services": "/api/http/services",
            "health": "/ping",
            "rawdata": "/api/overview",
        }
        endpoint = endpoints.get(action, "/api/overview")
        return _mw_cmd(f"curl -s '{url}{endpoint}'")


class HAProxyTool(BaseTool):
    """HAProxy 负载均衡"""
    name = "haproxy_manage"
    description = "HAProxy 状态/后端健康/连接统计"
    category = ToolCategory.REVERSE_PROXY
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "stats/info/backends/servers", "default": "info"},
    }}

    def execute(self, action: str = "info", **kwargs) -> ToolResult:
        if action == "stats":
            return _mw_cmd("echo 'show stat' | socat stdio /var/run/haproxy/admin.sock 2>/dev/null || echo 'HAProxy socket not found'")
        if action == "info":
            return _mw_cmd("echo 'show info' | socat stdio /var/run/haproxy/admin.sock 2>/dev/null || haproxy -vv 2>/dev/null")
        if action == "backends":
            return _mw_cmd("echo 'show stat' | socat stdio /var/run/haproxy/admin.sock 2>/dev/null | grep 'BACKEND' | awk -F',' '{print $1, $18, $19}'")
        if action == "servers":
            return _mw_cmd("echo 'show stat' | socat stdio /var/run/haproxy/admin.sock 2>/dev/null | grep -v BACKEND | grep -v '#' | awk -F',' '{print $1\":\"$2, $18, $19}'")
        return ToolResult(success=False, error="参数不足")


class ConsulTool(BaseTool):
    """HashiCorp Consul 服务发现"""
    name = "consul_manage"
    description = "Consul 服务注册/发现/KV 存储/健康检查"
    category = ToolCategory.UTILITY
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "services/health/kv/checks", "default": "services"},
        "key": {"type": "string", "description": "KV 存储键"},
        "service": {"type": "string", "description": "服务名"},
    }}

    def execute(self, action: str = "services", key: str = "", service: str = "", **kwargs) -> ToolResult:
        import os
        url = os.environ.get("CONSUL_URL", "http://localhost:8500")
        if action == "services":
            return _mw_cmd(f"curl -s '{url}/v1/catalog/services'")
        if action == "health" and service:
            return _mw_cmd(f"curl -s '{url}/v1/health/service/{service}?passing=true'")
        if action == "kv" and key:
            return _mw_cmd(f"curl -s '{url}/v1/kv/{key}?raw'")
        if action == "checks":
            return _mw_cmd(f"curl -s '{url}/v1/health/checks'")
        return ToolResult(success=False, error="参数不足")
