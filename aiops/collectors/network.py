"""网络信息采集器"""
from .base import BaseCollector

class NetworkCollector(BaseCollector):
    name = "network"
    def collect(self, ssh, server):
        out = self._exec(ssh,server,"ss -tunlp 2>/dev/null | tail -n +2 | head -30")
        ports = []
        for line in out.strip().split("\n"):
            if line.strip():
                p = line.split()
                if len(p)>=5: ports.append({"proto":p[0],"local":p[4],"process":p[-1] if "users:" in line else ""})
        return {"listening_ports": ports}
