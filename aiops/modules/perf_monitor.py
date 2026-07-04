"""性能监控模块"""
from ..collectors.system import SystemCollector
from ..collectors.process import ProcessCollector
import time

class PerfMonitorModule:
    name = "perf-monitor"
    def run(self, ctx):
        ssh, server = ctx["ssh"], ctx["server"]
        interval = ctx.get("interval", 5)
        sys_c, proc_c = SystemCollector(), ProcessCollector()
        snapshots = []
        for i in range(ctx.get("count",1)):
            sd = sys_c.collect(ssh,server); pd = proc_c.collect(ssh,server)
            snapshots.append({"cpu":sd.get("cpu",{}).get("usage_percent",0),"mem":sd.get("memory",{}).get("used_percent",0),"top_cpu":pd.get("top_cpu",[])[:3]})
            if i < ctx.get("count",1)-1: time.sleep(interval)
        return {"snapshots":snapshots}
