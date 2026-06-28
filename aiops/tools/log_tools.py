from .base import BaseTool, ToolResult

class LogSearchTool(BaseTool):
    name = "log_search"
    description = "在服务器上搜索日志"
    parameters = {"type": "object", "properties": {"file": {"type": "string"}, "pattern": {"type": "string"}, "tail": {"type": "integer", "default": 1000}}, "required": ["file", "pattern"]}
    def execute(self, file, pattern, tail=1000, **kw):
        if not self._registry or not self._registry.ssh: return ToolResult(success=False, error="SSH未配置")
        ssh = self._registry.ssh; config = self._registry.config; server = config.servers[0] if config.servers else None
        if not server: return ToolResult(success=False, error="无服务器")
        try:
            out, err, code = ssh.exec_command(server, f"tail -n {tail} {file} | grep -i {pattern} | tail -50", timeout=30)
            return ToolResult(success=(code==0), output=out.strip()[:5000])
        except Exception as e: return ToolResult(success=False, error=str(e))
