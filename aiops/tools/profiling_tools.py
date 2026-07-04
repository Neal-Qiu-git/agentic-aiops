"""Prometheus 长期存储 + 性能分析

Mimir: Grafana 长期存储 (CNCF 孵化, Cortex 继任)
Pyroscope: 持续性能分析 (CNCF 孵化)
"""
import subprocess, json, os
from .base import BaseTool, ToolResult, ToolCategory


def _run(cmd: str, t: int = 20) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=t)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


def _api(url: str, endpoint: str, t: int = 15) -> ToolResult:
    return _run(f"curl -s '{url}{endpoint}'", t)


class MimirQuery(BaseTool):
    """Grafana Mimir 长期存储查询"""
    name = "mimir_query"
    description = "查询 Grafana Mimir 长期指标存储"
    category = ToolCategory.MONITORING
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "ready/tenants/config/query", "default": "ready"},
        "query": {"type": "string", "description": "PromQL 查询"},
        "tenant": {"type": "string", "description": "租户 ID"},
    }}

    def execute(self, action: str = "ready", query: str = "", tenant: str = "", **kw) -> ToolResult:
        url = os.environ.get("MIMIR_URL", "http://localhost:8080")
        hdr = f"-H 'X-Scope-OrgID: {tenant}'" if tenant else ""
        if action == "query" and query:
            return _run(f"curl -s {hdr} '{url}/prometheus/api/v1/query?query={query}'")
        endpoints = {"ready": "/ready", "tenants": "/api/v1/tenants", "config": "/runtime_config"}
        return _api(url, endpoints.get(action, "/ready"))


class PyroscopeProfiles(BaseTool):
    """Pyroscope 持续性能分析"""
    name = "pyroscope_profiles"
    description = "查询 Pyroscope 持续性能分析数据 (CPU/内存/锁分析)"
    category = ToolCategory.PROFILING
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "apps/profiles标签/query", "default": "apps"},
        "app": {"type": "string", "description": "应用名称"},
        "query": {"type": "string", "description": "标签查询 (如 {app=\"nginx\"})"},
    }}

    def execute(self, action: str = "apps", app: str = "", query: str = "", **kw) -> ToolResult:
        url = os.environ.get("PYROSCOPE_URL", "http://localhost:4040")
        if action == "apps":
            return _api(url, "/api/apps")
        if action == "profiles" and app:
            return _api(url, f"/api/apps/{app}/profiles")
        if action == "query" and query:
            return _api(url, f"/querier.v1.QuerierService/SelectMergeStacktraces?query={query}")
        return _api(url, "/ready")


class PyroscopeMetrics(BaseTool):
    """Pyroscope 分析指标"""
    name = "pyroscope_metrics"
    description = "查询 Pyroscope 应用性能指标 (采样率/标签)"
    category = ToolCategory.PROFILING
    parameters = {"type": "object", "properties": {
        "app": {"type": "string", "description": "应用名称"},
    }, "required": ["app"]}

    def execute(self, app: str, **kw) -> ToolResult:
        url = os.environ.get("PYROSCOPE_URL", "http://localhost:4040")
        return _api(url, f"/api/apps/{app}/labels")
