"""systemd 服务状态采集器"""
from .base import BaseCollector

class ServiceCollector(BaseCollector):
    name = "service"
    def collect(self, ssh, server):
        out = self._exec(ssh,server,"systemctl list-units --state=failed --no-legend --no-pager 2>/dev/null")
        failed = [l.split()[0] for l in out.strip().split("\n") if l.strip()]
        total = int(self._exec(ssh,server,"systemctl list-units --type=service --no-legend --no-pager 2>/dev/null | wc -l").strip() or 0)
        return {"failed": failed, "total": total}
