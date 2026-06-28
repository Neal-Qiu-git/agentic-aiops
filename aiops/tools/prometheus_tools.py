from .base import BaseTool, ToolResult
import subprocess

class PrometheusQueryTool(BaseTool):
    name = "prometheus_query"
    description = "执行 PromQL 查询"
    parameters = {"type": "object", "properties": {"url": {"type": "string", "default": "http://localhost:9090"}, "query": {"type": "string"}}, "required": ["query"]}
    def execute(self, query, url="http://localhost:9090", **kw):
        try:
            r = subprocess.run(f"curl -s "{url}/api/v1/query?query={query}"", shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:5000])
        except Exception as e: return ToolResult(success=False, error=str(e))
