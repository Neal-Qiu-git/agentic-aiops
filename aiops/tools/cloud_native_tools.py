"""私有云 + 分布式数据库 + 可观测性补全

OpenStack: 私有云事实标准 (CNCF 项目)
Cassandra: 分布式 NoSQL (Netflix/Apple 大规模使用)
Grafana Tempo: 分布式追踪 (CNCF 孵化)
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


class OpenStackServer(BaseTool):
    """OpenStack 虚拟机管理"""
    name = "openstack_server"
    description = "OpenStack Nova 虚拟机管理 (list/start/stop/delete)"
    category = ToolCategory.CLOUD_API
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/show/start/stop/delete/flavors", "default": "list"},
        "server_id": {"type": "string"},
        "project": {"type": "string"},
    }}

    def execute(self, action: str = "list", server_id: str = "", project: str = "", **kwargs) -> ToolResult:
        proj = f"--project {project}" if project else ""
        actions = {
            "list": "openstack server list -f json",
            "flavors": "openstack flavor list -f json",
            "images": "openstack image list -f json",
        }
        if action in ("start", "stop") and server_id:
            return _run_cmd(f"openstack server {action} {server_id} {proj}")
        if action == "delete" and server_id:
            return _run_cmd(f"openstack server delete {server_id}")
        if action == "show" and server_id:
            return _run_cmd(f"openstack server show {server_id} -f json")
        return _run_cmd(actions.get(action, actions["list"]))


class OpenStackNetwork(BaseTool):
    """OpenStack 网络管理"""
    name = "openstack_network"
    description = "OpenStack Neutron 网络/子网/路由管理"
    category = ToolCategory.CLOUD_API
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "networks/subnets/routers/floating-ips", "default": "networks"},
    }}

    def execute(self, action: str = "networks", **kwargs) -> ToolResult:
        actions = {
            "networks": "openstack network list -f json",
            "subnets": "openstack subnet list -f json",
            "routers": "openstack router list -f json",
            "floating-ips": "openstack floating ip list -f json",
        }
        return _run_cmd(actions.get(action, actions["networks"]))


class OpenStackVolume(BaseTool):
    """OpenStack 存储管理"""
    name = "openstack_volume"
    description = "OpenStack Cinder 卷管理"
    category = ToolCategory.CLOUD_API
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/snapshots", "default": "list"},
    }}

    def execute(self, action: str = "list", **kwargs) -> ToolResult:
        return _run_cmd(f"openstack volume {action} -f json")


class CassandraTool(BaseTool):
    """Apache Cassandra 分布式数据库"""
    name = "cassandra_db"
    description = "Cassandra 集群管理: 节点状态/表/查询"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "status/keyspaces/tables/query/nodetool", "default": "status"},
        "keyspace": {"type": "string"},
        "sql": {"type": "string", "description": "CQL 语句"},
        "host": {"type": "string", "default": "localhost"},
    }}

    def execute(self, action: str = "status", keyspace: str = "", sql: str = "",
                host: str = "localhost", **kwargs) -> ToolResult:
        if action == "status":
            return _run_cmd(f"nodetool status 2>/dev/null || echo 'nodetool not found'")
        if action == "keyspaces":
            return _run_cmd(f"cqlsh {host} -e \"DESCRIBE KEYSPACES;\" 2>/dev/null")
        if action == "tables" and keyspace:
            return _run_cmd(f"cqlsh {host} -e \"USE {keyspace}; DESCRIBE TABLES;\" 2>/dev/null")
        if action == "query" and sql:
            return _run_cmd(f"cqlsh {host} -e \"{sql}\" 2>/dev/null")
        if action == "nodetool":
            return _run_cmd(f"nodetool tpstats 2>/dev/null")
        return _run_cmd(f"cqlsh {host} -e \"DESCRIBE KEYSPACES;\" 2>/dev/null")


class TempoTraces(BaseTool):
    """Grafana Tempo 分布式追踪"""
    name = "tempo_traces"
    description = "查询 Grafana Tempo 追踪数据"
    category = ToolCategory.APM
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "search/trace/status", "default": "search"},
        "trace_id": {"type": "string"},
        "service": {"type": "string"},
        "tags": {"type": "string", "description": "标签过滤 (如 http.method=GET)"},
    }}

    def execute(self, action: str = "search", trace_id: str = "", service: str = "",
                tags: str = "", **kwargs) -> ToolResult:
        import os
        url = os.environ.get("TEMPO_URL", "http://localhost:3200")
        if action == "trace" and trace_id:
            return _run_cmd(f"curl -s '{url}/api/traces/{trace_id}'")
        if action == "status":
            return _run_cmd(f"curl -s '{url}/status/ready'")
        # search
        params = []
        if service:
            params.append(f"service={service}")
        if tags:
            params.append(f"tags={tags}")
        query = "&".join(params)
        return _run_cmd(f"curl -s '{url}/api/search?{query}'")


class TempoMetrics(BaseTool):
    """Tempo 指标汇总"""
    name = "tempo_metrics"
    description = "查询 Tempo 追踪统计 (RED 指标)"
    category = ToolCategory.APM
    parameters = {"type": "object", "properties": {
        "service": {"type": "string"},
    }, "required": ["service"]}

    def execute(self, service: str, **kwargs) -> ToolResult:
        import os
        url = os.environ.get("TEMPO_URL", "http://localhost:3200")
        return _run_cmd(f"curl -s '{url}/api/metrics/summary?service={service}'")
