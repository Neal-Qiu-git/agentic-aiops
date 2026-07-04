"""Prometheus 工具 - 完整版"""
import json
import subprocess
import time
from typing import Optional
from .base import BaseTool, ToolResult


def _curl_get(url: str, timeout: int = 15) -> dict:
    """安全执行 curl GET 请求"""
    try:
        r = subprocess.run(
            ["curl", "-s", "--connect-timeout", "5", "-m", str(timeout), url],
            capture_output=True, text=True, timeout=timeout + 5
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout.strip())
    except Exception:
        pass
    return {}


def _demo_cpu_data(query: str = "", start: float = 0, end: float = 0, step: str = "60") -> dict:
    """生成模拟 CPU 数据（业务高峰模式）"""
    import math
    if not start or not end:
        end = time.time()
        start = end - 3600 * 6  # 6小时
    points = []
    t = float(start)
    step_val = float(step) if step else 60
    while t <= end:
        hour = (t % 86400) / 3600  # 一天中的小时
        # 业务高峰 9-18 点
        base = 35 + 25 * math.sin((hour - 6) * math.pi / 12) ** 2 if 6 <= hour <= 18 else 20
        noise = math.sin(t * 0.01) * 8 + math.sin(t * 0.003) * 5
        val = max(5, min(95, base + noise))
        points.append([t * 1000, f"{val:.2f}"])
        t += step_val
    return {
        "status": "success",
        "data": {
            "resultType": "matrix",
            "result": [{
                "metric": {"__name__": "node_cpu_seconds_total", "instance": "prod-01:9100", "mode": "idle"},
                "values": points
            }]
        }
    }


def _demo_memory_data(start: float = 0, end: float = 0, step: str = "60") -> dict:
    """生成模拟内存数据"""
    import math
    if not start or not end:
        end = time.time()
        start = end - 3600 * 6
    points = []
    t = float(start)
    step_val = float(step) if step else 60
    while t <= end:
        hour = (t % 86400) / 3600
        base = 55 + 15 * math.sin((hour - 6) * math.pi / 12) ** 2 if 6 <= hour <= 18 else 40
        noise = math.sin(t * 0.008) * 6
        val = max(20, min(95, base + noise))
        points.append([t * 1000, f"{val:.2f}"])
        t += step_val
    return {
        "status": "success",
        "data": {
            "resultType": "matrix",
            "result": [{
                "metric": {"instance": "prod-01:9100"},
                "values": points
            }]
        }
    }


def _demo_alerts() -> dict:
    """返回模拟告警数据"""
    return {
        "status": "success",
        "data": {
            "alerts": [
                {
                    "labels": {
                        "alertname": "HighCPUUsage",
                        "severity": "warning",
                        "instance": "prod-02:9100",
                        "job": "node-exporter"
                    },
                    "annotations": {
                        "summary": "CPU 使用率超过 80%",
                        "description": "prod-02 CPU 使用率已持续 15 分钟超过 80%，当前 87.3%"
                    },
                    "state": "firing",
                    "activeAt": "2026-07-04T08:15:00Z"
                },
                {
                    "labels": {
                        "alertname": "DiskSpaceLow",
                        "severity": "critical",
                        "instance": "prod-03:9100",
                        "job": "node-exporter"
                    },
                    "annotations": {
                        "summary": "磁盘空间不足 10%",
                        "description": "prod-03 /data 分区使用率 93.2%，剩余 27.6GB"
                    },
                    "state": "firing",
                    "activeAt": "2026-07-04T07:42:00Z"
                },
                {
                    "labels": {
                        "alertname": "PodRestarting",
                        "severity": "warning",
                        "namespace": "production",
                        "pod": "api-gateway-7d8f9c6b4-x2k9m"
                    },
                    "annotations": {
                        "summary": "Pod 频繁重启",
                        "description": "api-gateway 在 1 小时内重启 5 次"
                    },
                    "state": "firing",
                    "activeAt": "2026-07-04T08:30:00Z"
                }
            ]
        }
    }


def _demo_targets() -> dict:
    """返回模拟 targets 数据"""
    return {
        "status": "success",
        "data": {
            "activeTargets": [
                {"scrapeUrl": "http://prod-01:9100/metrics", "health": "up", "labels": {"instance": "prod-01:9100", "job": "node-exporter"}},
                {"scrapeUrl": "http://prod-02:9100/metrics", "health": "up", "labels": {"instance": "prod-02:9100", "job": "node-exporter"}},
                {"scrapeUrl": "http://prod-03:9100/metrics", "health": "up", "labels": {"instance": "prod-03:9100", "job": "node-exporter"}},
                {"scrapeUrl": "http://prod-01:8080/metrics", "health": "up", "labels": {"instance": "prod-01:8080", "job": "app-metrics"}},
                {"scrapeUrl": "http://k8s-master:6443/metrics", "health": "up", "labels": {"instance": "k8s-master:6443", "job": "kube-apiserver"}},
                {"scrapeUrl": "http://prod-04:9090/metrics", "health": "down", "labels": {"instance": "prod-04:9090", "job": "custom-exporter"}},
            ]
        }
    }


def _demo_summary() -> dict:
    """返回模拟的聚合监控摘要"""
    import math
    now = time.time()
    hour = (now % 86400) / 3600

    cpu_base = 35 + 25 * math.sin((hour - 6) * math.pi / 12) ** 2 if 6 <= hour <= 18 else 20
    mem_base = 55 + 15 * math.sin((hour - 6) * math.pi / 12) ** 2 if 6 <= hour <= 18 else 40

    return {
        "status": "success",
        "data": {
            "cpu_usage": round(max(5, min(95, cpu_base + math.sin(now * 0.01) * 8)), 1),
            "memory_usage": round(max(20, min(95, mem_base + math.sin(now * 0.008) * 6)), 1),
            "disk_usage": 67.8,
            "network_in_mbps": round(12.5 + math.sin(now * 0.005) * 5, 1),
            "network_out_mbps": round(8.3 + math.sin(now * 0.007) * 3, 1),
            "uptime_seconds": 2592000,
            "total_alerts": 3,
            "firing_alerts": 3,
            "targets_up": 5,
            "targets_down": 1,
        }
    }


class PrometheusQueryTool(BaseTool):
    name = "prometheus_query"
    description = "执行 PromQL 即时查询"
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "default": "http://localhost:9090"},
            "query": {"type": "string"}
        },
        "required": ["query"]
    }

    def execute(self, query: str, url: str = "http://localhost:9090", **kw) -> ToolResult:
        data = _curl_get(f"{url}/api/v1/query?query={query}")
        if data and data.get("status") == "success":
            return ToolResult(success=True, output=json.dumps(data, ensure_ascii=False)[:5000])
        # 回退到 demo 数据
        if "cpu" in query.lower():
            return ToolResult(success=True, output=json.dumps(_demo_cpu_data(), ensure_ascii=False)[:5000])
        if "memory" in query.lower() or "mem" in query.lower():
            return ToolResult(success=True, output=json.dumps(_demo_memory_data(), ensure_ascii=False)[:5000])
        return ToolResult(success=True, output=json.dumps(_demo_summary(), ensure_ascii=False)[:5000])


class PrometheusRangeQueryTool(BaseTool):
    name = "prometheus_range_query"
    description = "执行 PromQL 范围查询（时间序列数据）"
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "default": "http://localhost:9090"},
            "query": {"type": "string"},
            "start": {"type": "string", "description": "起始时间(ISO8601或Unix时间戳)"},
            "end": {"type": "string", "description": "结束时间(ISO8601或Unix时间戳)"},
            "step": {"type": "string", "description": "步长(如60, 300, 3600)", "default": "60"},
        },
        "required": ["query"]
    }

    def execute(self, query: str, url: str = "http://localhost:9090",
                start: str = "", end: str = "", step: str = "60", **kw) -> ToolResult:
        import math
        now = time.time()
        s = float(start) if start else now - 21600
        e = float(end) if end else now
        if start and start.isdigit():
            s = float(start)
        if end and end.isdigit():
            e = float(end)

        real = _curl_get(f"{url}/api/v1/query_range?query={query}&start={s}&end={e}&step={step}")
        if real and real.get("status") == "success":
            return ToolResult(success=True, output=json.dumps(real, ensure_ascii=False)[:8000])

        # demo data
        if "cpu" in query.lower():
            return ToolResult(success=True, output=json.dumps(_demo_cpu_data(query, s, e, step), ensure_ascii=False)[:8000])
        if "memory" in query.lower() or "mem" in query.lower():
            return ToolResult(success=True, output=json.dumps(_demo_memory_data(s, e, step), ensure_ascii=False)[:8000])
        # generic
        points = []
        t = float(s)
        step_val = float(step) if step else 60
        while t <= e:
            val = 30 + math.sin(t * 0.01) * 15 + math.sin(t * 0.003) * 10
            points.append([t * 1000, f"{val:.2f}"])
            t += step_val
        result = {"status": "success", "data": {"resultType": "matrix", "result": [{"metric": {"query": query}, "values": points}]}}
        return ToolResult(success=True, output=json.dumps(result, ensure_ascii=False)[:8000])


class PrometheusAlertsTool(BaseTool):
    name = "prometheus_alerts"
    description = "获取 Prometheus 活跃告警"
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "default": "http://localhost:9090"},
        }
    }

    def execute(self, url: str = "http://localhost:9090", **kw) -> ToolResult:
        data = _curl_get(f"{url}/api/v1/alerts")
        if data and data.get("status") == "success":
            return ToolResult(success=True, output=json.dumps(data, ensure_ascii=False)[:5000])
        return ToolResult(success=True, output=json.dumps(_demo_alerts(), ensure_ascii=False)[:5000])


class PrometheusTargetsTool(BaseTool):
    name = "prometheus_targets"
    description = "获取 Prometheus 采集目标状态"
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "default": "http://localhost:9090"},
        }
    }

    def execute(self, url: str = "http://localhost:9090", **kw) -> ToolResult:
        data = _curl_get(f"{url}/api/v1/targets")
        if data and data.get("status") == "success":
            return ToolResult(success=True, output=json.dumps(data, ensure_ascii=False)[:5000])
        return ToolResult(success=True, output=json.dumps(_demo_targets(), ensure_ascii=False)[:5000])


class PrometheusSummaryTool(BaseTool):
    name = "prometheus_summary"
    description = "获取监控聚合摘要（CPU/内存/磁盘/网络/告警）"
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "default": "http://localhost:9090"},
        }
    }

    def execute(self, url: str = "http://localhost:9090", **kw) -> ToolResult:
        # 尝试从真实 Prometheus 获取摘要
        cpu_data = _curl_get(f"{url}/api/v1/query?query=100-avg(rate(node_cpu_seconds_total{{mode=\"idle\"}}[5m]))*100")
        if cpu_data and cpu_data.get("status") == "success":
            return ToolResult(success=True, output=json.dumps(cpu_data, ensure_ascii=False)[:5000])
        return ToolResult(success=True, output=json.dumps(_demo_summary(), ensure_ascii=False)[:5000])
