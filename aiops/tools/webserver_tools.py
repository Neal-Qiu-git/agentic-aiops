"""Web 服务器扩展工具 - WildFly / Caddy

WildFly: Red Hat Java 应用服务器 (JBoss 继任)
Caddy: 现代自动 HTTPS Web 服务器 (自动证书)
"""
import subprocess
from .base import BaseTool, ToolResult, ToolCategory


def _run(cmd: str, t: int = 15) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=t)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class WildFlyTool(BaseTool):
    """WildFly / JBoss 应用服务器"""
    name = "wildfly_manage"
    description = "WildFly/JBoss 应用服务器管理"
    category = ToolCategory.REVERSE_PROXY
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "status/deployments/datasources/threads", "default": "status"},
        "host": {"type": "string", "default": "localhost"},
        "port": {"type": "integer", "default": 9990},
    }}

    def execute(self, action: str = "status", host: str = "localhost", port: int = 9990, **kw) -> ToolResult:
        cli = f"/opt/wildfly/bin/jboss-cli.sh --connect --controller=remote+http://{host}:{port}"
        cmds = {
            "status": f"{cli} ':read-resource' 2>/dev/null || systemctl status wildfly 2>/dev/null",
            "deployments": f"{cli} 'deployment-info' 2>/dev/null",
            "datasources": f"{cli} '/subsystem=datasources/data-source=*:read-resource' 2>/dev/null",
            "threads": f"{cli} '/core-service=management/management-interface=http-interface:read-resource' 2>/dev/null",
        }
        return _run(cmds.get(action, cmds["status"]))


class CaddyTool(BaseTool):
    """Caddy Web 服务器"""
    name = "caddy_manage"
    description = "Caddy 现代 Web 服务器管理 (自动 HTTPS)"
    category = ToolCategory.REVERSE_PROXY
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "status/config/routes/stop/reload", "default": "status"},
    }}

    def execute(self, action: str = "status", **kw) -> ToolResult:
        cmds = {
            "status": "systemctl status caddy 2>/dev/null || caddy version 2>/dev/null",
            "config": "caddy validate 2>/dev/null || cat /etc/caddy/Caddyfile 2>/dev/null",
            "routes": "caddy list-modules 2>/dev/null",
            "reload": "systemctl reload caddy 2>/dev/null || caddy reload 2>/dev/null",
        }
        return _run(cmds.get(action, cmds["status"]))
