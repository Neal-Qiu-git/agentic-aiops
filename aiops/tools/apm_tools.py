"""APM 工具 - SkyWalking / Jaeger / OpenTelemetry

Apache SkyWalking: Java APM 领域事实标准 (中国最广泛)
Jaeger: CNCF 毕业项目，分布式追踪
OpenTelemetry: CNCF 孵化项目，统一遥测标准
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _apm_cmd(cmd: str, timeout: int = 20) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class SkyWalkingService(BaseTool):
    """SkyWalking 服务拓扑"""
    name = "skywalking_services"
    description = "SkyWalking 服务列表和拓扑"
    category = ToolCategory.APM
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/topology/metrics/alarms", "default": "list"},
        "service_name": {"type": "string"},
        "duration_start": {"type": "string", "description": "开始时间 (yyyy-MM-dd HHmm)"},
        "duration_end": {"type": "string", "description": "结束时间"},
        "duration_step": {"type": "string", "description": "MINUTE/HOUR/DAY", "default": "MINUTE"},
    }}

    def execute(self, action: str = "list", service_name: str = "",
                duration_start: str = "", duration_end: str = "",
                duration_step: str = "MINUTE", **kwargs) -> ToolResult:
        import os, time, urllib.parse
        url = os.environ.get("SKYWALKING_URL", "http://localhost:12800")
        if not duration_start:
            now = time.strftime("%Y-%m-%d %H%M")
            duration_start = now
            duration_end = now

        duration = urllib.parse.quote(json.dumps({
            "start": duration_start, "end": duration_end, "step": duration_step
        }))

        if action == "list":
            gql = '{"query":"{ getAllServices(duration: %s) { key: id name } }"}' % duration
        elif action == "topology" and service_name:
            gql = '{"query":"{ getServiceTopology(serviceId: \\"%s\\", duration: %s) { nodes { id name } calls { id source target } } }"}' % (service_name, duration)
        elif action == "alarms":
            gql = '{"query":"{ getAllAlarms(paging: {pageNum: 1, pageSize: 20}) { key: id message startTime } }"}'
        else:
            return ToolResult(success=False, error="参数不足")
        return _apm_cmd(f"curl -s -X POST '{url}/graphql' -H 'Content-Type: application/json' -d '{gql}'")


class SkyWalkingMetrics(BaseTool):
    """SkyWalking 指标查询"""
    name = "skywalking_metrics"
    description = "查询 SkyWalking 服务指标 (响应时间/成功率/SLA)"
    category = ToolCategory.APM
    parameters = {"type": "object", "properties": {
        "service_name": {"type": "string"},
        "metric": {"type": "string", "description": "service_resp_time/service_sla/service_cpm/service_p90", "default": "service_resp_time"},
    }, "required": ["service_name"]}

    def execute(self, service_name: str, metric: str = "service_resp_time", **kwargs) -> ToolResult:
        import os, time, urllib.parse
        url = os.environ.get("SKYWALKING_URL", "http://localhost:12800")
        now = time.strftime("%Y-%m-%d %H%M")
        duration = urllib.parse.quote(json.dumps({"start": now, "end": now, "step": "MINUTE"}))
        gql = '{"query":"{ readMetricsValues(condition: {name: \\"%s\\", entity: {scope: Service, serviceName: \\"%s\\", normal: true}}, duration: %s) { label values { values { id value } } } }"}' % (metric, service_name, duration)
        return _apm_cmd(f"curl -s -X POST '{url}/graphql' -H 'Content-Type: application/json' -d '{gql}'")


class JaegerTraces(BaseTool):
    """Jaeger 分布式追踪"""
    name = "jaeger_traces"
    description = "查询 Jaeger 分布式追踪数据"
    category = ToolCategory.APM
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "services/operations/traces/trace", "default": "services"},
        "service": {"type": "string"},
        "trace_id": {"type": "string", "description": "Trace ID (查询单条)"},
        "limit": {"type": "integer", "default": 20},
    }}

    def execute(self, action: str = "services", service: str = "",
                trace_id: str = "", limit: int = 20, **kwargs) -> ToolResult:
        import os, time
        url = os.environ.get("JAEGER_URL", "http://localhost:16686")
        if action == "services":
            return _apm_cmd(f"curl -s '{url}/api/services'")
        if action == "operations" and service:
            return _apm_cmd(f"curl -s '{url}/api/services/{service}/operations'")
        if action == "trace" and trace_id:
            return _apm_cmd(f"curl -s '{url}/api/traces/{trace_id}'")
        if action == "traces" and service:
            now = int(time.time() * 1e6)
            start = now - 3600 * 1e6
            return _apm_cmd(f"curl -s '{url}/api/traces?service={service}&start={int(start)}&end={int(now)}&limit={limit}'")
        return ToolResult(success=False, error="参数不足")


class OpenTelemetryCollector(BaseTool):
    """OpenTelemetry Collector 状态"""
    name = "otel_collector"
    description = "查询 OTel Collector 运行状态和指标"
    category = ToolCategory.APM
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "status/pipelines/extensions", "default": "status"},
    }}

    def execute(self, action: str = "status", **kwargs) -> ToolResult:
        import os
        url = os.environ.get("OTEL_COLLECTOR_URL", "http://localhost:8888")
        if action == "status":
            return _apm_cmd(f"curl -s '{url}/'")
        if action == "pipelines":
            return _apm_cmd(f"curl -s '{url}/metrics' | grep -E 'otelcol_accepted|otelcol_refused|otelcol_sent'")
        if action == "extensions":
            return _apm_cmd(f"curl -s '{url}/metrics' | grep 'otelcol_' | head -30")
        return ToolResult(success=False, error="参数不足")
