from .base import BaseTool, ToolResult
import subprocess

class DockerPSTool(BaseTool):
    name = "docker_ps"
    description = "查看 Docker 容器"
    parameters = {"type": "object", "properties": {"all": {"type": "boolean", "default": False}}}
    def execute(self, all=False, **kw):
        cmd = "docker ps" + (" -a" if all else "") + " --format "{{.Names}} {{.Status}} {{.Image}}""
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:3000])
        except Exception as e: return ToolResult(success=False, error=str(e))

class DockerLogsTool(BaseTool):
    name = "docker_logs"
    description = "查看容器日志"
    parameters = {"type": "object", "properties": {"container": {"type": "string"}, "tail": {"type": "integer", "default": 100}}, "required": ["container"]}
    def execute(self, container, tail=100, **kw):
        try:
            r = subprocess.run(f"docker logs {container} --tail {tail}", shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:5000])
        except Exception as e: return ToolResult(success=False, error=str(e))

class DockerStatsTool(BaseTool):
    name = "docker_stats"
    description = "容器资源使用"
    parameters = {"type": "object", "properties": {}}
    def execute(self, **kw):
        try:
            r = subprocess.run("docker stats --no-stream", shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:3000])
        except Exception as e: return ToolResult(success=False, error=str(e))
