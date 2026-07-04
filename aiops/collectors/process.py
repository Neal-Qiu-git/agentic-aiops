"""进程信息采集器"""
from .base import BaseCollector

class ProcessCollector(BaseCollector):
    name = "process"
    def collect(self, ssh, server):
        return {"top_cpu": self._top(ssh,server,"%cpu"), "top_mem": self._top(ssh,server,"%mem"),
                "zombie_count": int(self._exec(ssh,server,"ps aux | awk '$8~/Z/{c++}END{print c+0}'").strip() or 0)}
    def _top(self, ssh, server, sort_key):
        out = self._exec(ssh,server,f"ps aux --sort=-{sort_key} | head -11")
        procs = []
        for line in out.strip().split("\n")[1:]:
            p = line.split(None, 10)
            if len(p)>=11: procs.append({"user":p[0],"pid":p[1],"cpu":float(p[2]),"mem":float(p[3]),"cmd":p[10][:80]})
        return procs
