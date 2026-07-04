from .base import BaseTool, ToolResult
import subprocess

class MySQLQueryTool(BaseTool):
    name = "mysql_query"
    description = "执行 MySQL 查询"
    parameters = {"type": "object", "properties": {"host": {"type": "string", "default": "127.0.0.1"}, "user": {"type": "string", "default": "root"}, "password": {"type": "string"}, "query": {"type": "string"}}, "required": ["query"]}
    def execute(self, query, host="127.0.0.1", user="root", password="", **kw):
        cmd = f"mysql -h {host} -u {user}"
        if password: cmd += f" -p{password}"
        cmd += f' -e "{query}"'
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:5000])
        except Exception as e: return ToolResult(success=False, error=str(e))
