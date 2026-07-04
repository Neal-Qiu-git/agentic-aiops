"""Docker 信息采集器"""
import json
from .base import BaseCollector

class DockerCollector(BaseCollector):
    name = "docker"
    def collect(self, ssh, server):
        ver = self._exec(ssh,server,"docker info --format '{{.ServerVersion}}' 2>/dev/null").strip()
        if not ver: return {"available": False}
        out = self._exec(ssh,server,"docker ps -a --format '{{json .}}' 2>/dev/null")
        containers = [json.loads(l) for l in out.strip().split("\n") if l.strip()]
        return {"available": True, "version": ver, "containers": containers}
