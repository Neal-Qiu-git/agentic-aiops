"""容量规划模块"""
from ..collectors.system import SystemCollector

class CapacityPlanModule:
    name = "capacity-plan"
    def run(self, ctx):
        ssh, server = ctx["ssh"], ctx["server"]
        sd = SystemCollector().collect(ssh,server)
        cpu = sd.get("cpu",{}).get("usage_percent",0); mem = sd.get("memory",{}).get("used_percent",0)
        recs = []
        if cpu > 80: recs.append({"resource":"CPU","urgency":"high","message":f"CPU {cpu}% - 建议扩容"})
        elif cpu < 20: recs.append({"resource":"CPU","urgency":"low","message":f"CPU {cpu}% - 可降配"})
        if mem > 85: recs.append({"resource":"Memory","urgency":"high","message":f"内存 {mem}% - 建议扩容"})
        for d in sd.get("disk",[]):
            if d.get("used_percent",0) > 85: recs.append({"resource":d.get("mount",""),"urgency":"high","message":f"磁盘满"})
        if not recs: recs.append({"resource":"Overall","urgency":"info","message":"资源充足"})
        return {"recommendations":recs}
