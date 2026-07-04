"""Loki 工具 - LogQL 日志查询

Grafana Loki 是云原生日志聚合标准，与 Prometheus 标签体系一致。
实际使用：K8s 环境下 Loki 已成为 ELK 的主流替代方案。
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _loki_query(query: str, limit: int = 100, direction: str = "backward", timeout: int = 30) -> ToolResult:
    """查询 Loki"""
    try:
        import os, time
        url = os.environ.get("LOKI_URL", "http://localhost:3100")
        ts = str(int(time.time() * 1e9))
        cmd = (f"curl -s '{url}/loki/api/v1/query_range'"
               f"?query={query}&limit={limit}&direction={direction}"
               f"&start={ts}&end={ts}")
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class LokiQuery(BaseTool):
    """LogQL 查询日志"""
    name = "loki_query"
    description = "使用 LogQL 查询 Loki 日志 (如 {job='nginx'} |= 'error')"
    category = ToolCategory.LOG
    parameters = {"type": "object", "properties": {
        "query": {"type": "string", "description": "LogQL 查询语句"},
        "limit": {"type": "integer", "default": 100},
        "direction": {"type": "string", "description": "forward/backward", "default": "backward"},
    }, "required": ["query"]}

    def execute(self, query: str, limit: int = 100, direction: str = "backward", **kwargs) -> ToolResult:
        return _loki_query(query, limit, direction)


class LokiLabels(BaseTool):
    """列出 Loki 标签"""
    name = "loki_labels"
    description = "列出所有 Loki 日志标签"
    category = ToolCategory.LOG
    parameters = {"type": "object", "properties": {
        "namespace": {"type": "string", "description": "K8s namespace 过滤"},
    }}

    def execute(self, namespace: str = "", **kwargs) -> ToolResult:
        try:
            import os
            url = os.environ.get("LOKI_URL", "http://localhost:3100")
            cmd = f"curl -s '{url}/loki/api/v1/labels'"
            if namespace:
                cmd += f"?namespace={namespace}"
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000],
                              error=r.stderr.strip() if r.returncode != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class LokiLabelValues(BaseTool):
    """查询 Loki 标签值"""
    name = "loki_label_values"
    description = "查询指定标签的所有值"
    category = ToolCategory.LOG
    parameters = {"type": "object", "properties": {
        "label": {"type": "string", "description": "标签名 (如 job, namespace)"},
    }, "required": ["label"]}

    def execute(self, label: str, **kwargs) -> ToolResult:
        try:
            import os
            url = os.environ.get("LOKI_URL", "http://localhost:3100")
            r = subprocess.run(f"curl -s '{url}/loki/api/v1/label/{label}/values'",
                               shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000],
                              error=r.stderr.strip() if r.returncode != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class LokiSeries(BaseTool):
    """Loki 时间序列查询"""
    name = "loki_series"
    description = "查询匹配的时间序列"
    category = ToolCategory.LOG
    parameters = {"type": "object", "properties": {
        "match": {"type": "string", "description": "匹配器 (如 {job='nginx'})"},
    }, "required": ["match"]}

    def execute(self, match: str, **kwargs) -> ToolResult:
        try:
            import os
            url = os.environ.get("LOKI_URL", "http://localhost:3100")
            r = subprocess.run(f"curl -s '{url}/loki/api/v1/series?match[]={match}'",
                               shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000],
                              error=r.stderr.strip() if r.returncode != 0 else "")
        except Exception as e:
            return ToolResult(success=False, error=str(e))
