from .base import BaseTool, ToolResult
import subprocess

class HTTPGetTool(BaseTool):
    name = "http_get"
    description = "HTTP GET 请求"
    parameters = {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}
    def execute(self, url, **kw):
        try:
            r = subprocess.run(f"curl -s -o /dev/null -w %{{http_code}} {url}", shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=True, output=f"HTTP {r.stdout.strip()}")
        except Exception as e: return ToolResult(success=False, error=str(e))
