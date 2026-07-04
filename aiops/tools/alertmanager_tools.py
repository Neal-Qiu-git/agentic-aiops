"""Alertmanager 工具 - 告警管理

Prometheus Alertmanager 是云原生告警的事实标准。
支持告警路由、分组、抑制、静默。
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _am_api(method: str, endpoint: str, body: str = "", timeout: int = 15) -> ToolResult:
    try:
        import os
        url = os.environ.get("ALERTMANAGER_URL", "http://localhost:9093")
        cmd = f"curl -s -X {method} {url}{endpoint}"
        if body:
            cmd += f" -H 'Content-Type: application/json' -d '{body}'"
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class AlertmanagerAlerts(BaseTool):
    """查询当前活跃告警"""
    name = "alertmanager_alerts"
    description = "获取 Alertmanager 当前活跃/待处理告警"
    category = ToolCategory.MONITORING
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "active/silenced/inhibited", "default": "active"},
    }}

    def execute(self, action: str = "active", **kwargs) -> ToolResult:
        return _am_api("GET", f"/api/v2/alerts?silenced=false&inhibited=false")


class AlertmanagerSilence(BaseTool):
    """创建/删除静默规则"""
    name = "alertmanager_silence"
    description = "管理 Alertmanager 静默规则"
    category = ToolCategory.MONITORING
    is_destructive = True
    requires_confirmation = True
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "create/delete/list"},
        "matchers": {"type": "string", "description": "告警匹配器 (如 alertname=HighCPU)"},
        "duration": {"type": "string", "description": "静默时长 (如 2h, 1d)", "default": "2h"},
        "silence_id": {"type": "string", "description": "静默 ID (删除时)"},
        "comment": {"type": "string", "description": "静默原因"},
    }, "required": ["action"]}

    def execute(self, action: str = "list", matchers: str = "", duration: str = "2h",
                silence_id: str = "", comment: str = "", **kwargs) -> ToolResult:
        if action == "list":
            return _am_api("GET", "/api/v2/silences")
        if action == "delete" and silence_id:
            return _am_api("DELETE", f"/api/v2/silence/{silence_id}")
        if action == "create" and matchers:
            import time
            now = int(time.time())
            dur_seconds = self._parse_duration(duration)
            matchers_list = []
            for m in matchers.split(","):
                if "=" in m:
                    k, v = m.strip().split("=", 1)
                    matchers_list.append({"name": k.strip(), "value": v.strip(), "isRegex": False})
            body = json.dumps({
                "matchers": matchers_list,
                "startsAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
                "endsAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now + dur_seconds)),
                "createdBy": "agentic-aiops",
                "comment": comment or f"Auto silence by Agentic AIOps",
            })
            return _am_api("POST", "/api/v2/silences", body)
        return ToolResult(success=False, error="参数不足")

    @staticmethod
    def _parse_duration(d: str) -> int:
        d = d.strip().lower()
        if d.endswith("h"):
            return int(d[:-1]) * 3600
        if d.endswith("d"):
            return int(d[:-1]) * 86400
        if d.endswith("m"):
            return int(d[:-1]) * 60
        return 7200


class AlertmanagerStatus(BaseTool):
    """Alertmanager 状态"""
    name = "alertmanager_status"
    description = "获取 Alertmanager 运行状态"
    category = ToolCategory.MONITORING
    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> ToolResult:
        return _am_api("GET", "/api/v2/status")
