"""Grafana 工具 - Dashboard/API 查询

Grafana 是行业标准可视化平台，支持 Prometheus/Loki/ES 等多数据源。
实际使用：85% 云原生企业采用 Grafana 可视化。
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _grafana_api(method: str, endpoint: str, body: str = "", timeout: int = 15) -> ToolResult:
    """调用 Grafana HTTP API"""
    try:
        import os
        url = os.environ.get("GRAFANA_URL", "http://localhost:3000")
        token = os.environ.get("GRAFANA_TOKEN", "")
        auth = f"-H 'Authorization: Bearer {token}'" if token else ""
        cmd = f"curl -s -X {method} {url}/api{endpoint} {auth}"
        if body:
            cmd += f" -H 'Content-Type: application/json' -d '{body}'"
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class GrafanaDashboards(BaseTool):
    """列出/搜索 Grafana Dashboard"""
    name = "grafana_dashboards"
    description = "列出或搜索 Grafana 仪表盘"
    category = ToolCategory.MONITORING
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/search/stats", "default": "list"},
        "query": {"type": "string", "description": "搜索关键词"},
    }}

    def execute(self, action: str = "list", query: str = "", **kwargs) -> ToolResult:
        if action == "stats":
            return _grafana_api("GET", "/search?type=dash-db")
        if action == "search" and query:
            return _grafana_api("GET", f"/search?type=dash-db&query={query}")
        return _grafana_api("GET", "/search?type=dash-db")


class GrafanaQuery(BaseTool):
    """查询 Grafana 数据源 (Prometheus/Loki/ES)"""
    name = "grafana_query"
    description = "通过 Grafana 代理查询数据源 (PromQL/LogQL)"
    category = ToolCategory.MONITORING
    parameters = {"type": "object", "properties": {
        "datasource_id": {"type": "integer", "description": "数据源 ID"},
        "query": {"type": "string", "description": "PromQL 或 LogQL 查询"},
        "start": {"type": "string", "description": "开始时间 (RFC3339)"},
        "end": {"type": "string", "description": "结束时间 (RFC3339)"},
    }, "required": ["datasource_id", "query"]}

    def execute(self, datasource_id: int, query: str, start: str = "", end: str = "", **kwargs) -> ToolResult:
        import time
        if not start:
            start = str(int(time.time()) - 3600)
        if not end:
            end = str(int(time.time()))
        body = json.dumps({"queries": [{"refId": "A", "datasource": {"uid": str(datasource_id)}, "expr": query}],
                           "from": f"{int(float(start))*1000}", "to": f"{int(float(end))*1000}"})
        return _grafana_api("POST", "/ds/query", body)


class GrafanaAnnotations(BaseTool):
    """查询 Grafana 标注 (事件标记)"""
    name = "grafana_annotations"
    description = "获取 Grafana 时间线标注/事件"
    category = ToolCategory.MONITORING
    parameters = {"type": "object", "properties": {
        "limit": {"type": "integer", "default": 50},
    }}

    def execute(self, limit: int = 50, **kwargs) -> ToolResult:
        return _grafana_api("GET", f"/annotations?limit={limit}")


class GrafanaAlertRules(BaseTool):
    """查询 Grafana Unified Alerting 规则"""
    name = "grafana_alert_rules"
    description = "获取 Grafana 统一告警规则和状态"
    category = ToolCategory.MONITORING
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/evaluations", "default": "list"},
        "rule_uid": {"type": "string"},
    }}

    def execute(self, action: str = "list", rule_uid: str = "", **kwargs) -> ToolResult:
        if action == "evaluations" and rule_uid:
            return _grafana_api("GET", f"/v1/provisioning/alert-rules/{rule_uid}/evaluations")
        return _grafana_api("GET", "/v1/provisioning/alert-rules")
