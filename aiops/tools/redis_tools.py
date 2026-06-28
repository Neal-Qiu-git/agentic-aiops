from .base import BaseTool, ToolResult
import subprocess

class RedisQueryTool(BaseTool):
    name = "redis_query"
    description = "执行 Redis 命令"
    parameters = {"type": "object", "properties": {"host": {"type": "string", "default": "127.0.0.1"}, "port": {"type": "integer", "default": 6379}, "command": {"type": "string"}}, "required": ["command"]}
    def execute(self, command, host="127.0.0.1", port=6379, **kw):
        try:
            r = subprocess.run(f"redis-cli -h {host} -p {port} {command}", shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:5000])
        except Exception as e: return ToolResult(success=False, error=str(e))
