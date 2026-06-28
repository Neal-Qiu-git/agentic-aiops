"""成本优化模块"""
from ..collectors.system import SystemCollector

class CostOptimizeModule:
    name = "cost-optimize"
    def run(self, ctx):
        ssh, server = ctx["ssh"], ctx["server"]
        sd = SystemCollector().collect(ssh,server)
        cpu = sd.get("cpu",{}).get("usage_percent",0); mem = sd.get("memory",{}).get("used_percent",0)
        suggestions = []
        if cpu < 20: suggestions.append({"priority":"medium","message":f"CPU {cpu}% - 可降配"})
        if mem < 30: suggestions.append({"priority":"low","message":f"内存 {mem}% - 可减少"})
        if not suggestions: suggestions.append({"priority":"info","message":"资源使用正常"})
        return {"utilization":{"cpu":cpu,"memory":mem},"suggestions":suggestions}
