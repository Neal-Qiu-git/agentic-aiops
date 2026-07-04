"""健康巡检模块"""
from ..collectors.system import SystemCollector
from ..collectors.process import ProcessCollector
from ..collectors.docker import DockerCollector
from ..collectors.network import NetworkCollector
from ..collectors.service import ServiceCollector
from ..analyzers.anomaly import AnomalyAnalyzer

class HealthCheckModule:
    name = "health-check"
    def run(self, ctx):
        ssh, server = ctx["ssh"], ctx["server"]
        data = {"system": SystemCollector().collect(ssh,server), "process": ProcessCollector().collect(ssh,server),
                "docker": DockerCollector().collect(ssh,server), "network": NetworkCollector().collect(ssh,server),
                "service": ServiceCollector().collect(ssh,server)}
        flat = {"cpu":data["system"].get("cpu",{}), "memory":data["system"].get("memory",{}),
                "disk":data["system"].get("disk",[]), "load":data["system"].get("load",{}),
                "swap":data["system"].get("swap",{}), "service":data["service"]}
        anomalies = AnomalyAnalyzer(ctx.get("thresholds")).analyze(flat)
        overall = "CRITICAL" if anomalies["critical"]>0 else "DEGRADED" if anomalies["warning"]>0 else "HEALTHY"
        return {"overall":overall,"data":data,"anomalies":anomalies,"hostname":data["system"].get("hostname",""),"os":data["system"].get("os","")}
