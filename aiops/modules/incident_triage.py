"""事件分诊模块"""
from ..collectors.system import SystemCollector
from ..collectors.service import ServiceCollector
from ..collectors.log_collector import LogCollector
from ..analyzers.anomaly import AnomalyAnalyzer

class IncidentTriageModule:
    name = "incident-triage"
    def run(self, ctx):
        ssh, server = ctx["ssh"], ctx["server"]
        symptom = ctx.get("symptom","")
        sys_d = SystemCollector().collect(ssh,server)
        svc_d = ServiceCollector().collect(ssh,server)
        log_d = LogCollector().collect(ssh,server)
        flat = {"cpu":sys_d.get("cpu",{}),"memory":sys_d.get("memory",{}),"disk":sys_d.get("disk",[]),
                "load":sys_d.get("load",{}),"swap":sys_d.get("swap",{}),"service":svc_d,"log":log_d}
        anomalies = AnomalyAnalyzer(ctx.get("thresholds")).analyze(flat)
        crit = anomalies["critical"]
        failed = len(svc_d.get("failed",[]))
        severity = "SEV1" if failed>3 or crit>=3 else "SEV2" if failed>0 or crit>=1 else "SEV3" if anomalies["warning"]>0 else "SEV4"
        return {"severity":severity,"symptom":symptom,"anomalies":anomalies,
                "actions":["通知相关人员","记录事件时间线"] if severity in("SEV1","SEV2") else ["继续观察"]}
