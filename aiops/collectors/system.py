"""系统指标采集器"""
from .base import BaseCollector

class SystemCollector(BaseCollector):
    name = "system"
    def collect(self, ssh, server):
        return {"memory": self._mem(ssh,server), "disk": self._disk(ssh,server),
                "cpu": self._cpu(ssh,server), "load": self._load(ssh,server),
                "swap": self._swap(ssh,server), "hostname": self._exec(ssh,server,"hostname").strip(),
                "os": self._exec(ssh,server,"cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d'\"' -f2").strip(),
                "uptime": self._exec(ssh,server,"uptime -p 2>/dev/null || uptime").strip()}

    def _mem(self, ssh, server):
        p = self._exec(ssh,server,"free -b | grep Mem").split()
        if len(p)<7: return {"error":"parse"}
        total,used,avail = int(p[1]),int(p[2]),int(p[6])
        return {"total":total,"used":used,"available":avail,"used_percent":round(used/total*100,1) if total else 0}

    def _disk(self, ssh, server):
        out = self._exec(ssh,server,"df -B1 --output=source,size,used,avail,pcent,target -x tmpfs -x devtmpfs 2>/dev/null")
        disks = []
        for line in out.strip().split("\n")[1:]:
            p = line.split()
            if len(p)>=6 and p[0].startswith("/"):
                disks.append({"device":p[0],"mount":p[5],"used_percent":float(p[4].rstrip("%")),
                    "total":self._psize(p[1]),"used":self._psize(p[2]),"available":self._psize(p[3])})
        return disks

    def _cpu(self, ssh, server):
        cores = int(self._exec(ssh,server,"nproc").strip() or 0)
        out = self._exec(ssh,server,"cat /proc/stat | head -1 && sleep 1 && cat /proc/stat | head -1")
        lines = out.strip().split("\n"); usage = 0
        if len(lines)>=2:
            v1=[int(x) for x in lines[0].split()[1:]]; v2=[int(x) for x in lines[1].split()[1:]]
            d=[b-a for a,b in zip(v1,v2)]; t=sum(d)
            usage = round((t-d[3])/t*100,1) if t else 0
        return {"cores":cores,"usage_percent":usage}

    def _load(self, ssh, server):
        p = self._exec(ssh,server,"cat /proc/loadavg").split()
        return {"load1":float(p[0]),"load5":float(p[1]),"load15":float(p[2])} if len(p)>=3 else {"error":"parse"}

    def _swap(self, ssh, server):
        p = self._exec(ssh,server,"free -b | grep Swap").split()
        total,used = int(p[1]),int(p[2]) if len(p)>=3 else (0,0)
        return {"total":total,"used":used,"used_percent":round(used/total*100,1) if total else 0}

    def _psize(self, s):
        s=s.strip().upper(); m={"K":1024,"M":1024**2,"G":1024**3}
        return int(float(s[:-1])*m[s[-1]]) if s and s[-1] in m else (int(s) if s.isdigit() else 0)
