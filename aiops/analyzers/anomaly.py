"""异常检测分析器"""

class AnomalyAnalyzer:
    def __init__(self, thresholds=None):
        t = thresholds or {}
        self.cw = getattr(t, "cpu_warning", 70); self.cc = getattr(t, "cpu_critical", 90)
        self.mw = getattr(t, "mem_warning", 75); self.mc = getattr(t, "mem_critical", 90)
        self.dw = getattr(t, "disk_warning", 75); self.dc = getattr(t, "disk_critical", 90)

    def analyze(self, data):
        anomalies = []
        cpu = data.get("cpu", {}).get("usage_percent", 0)
        if cpu >= self.cc: anomalies.append({"type":"cpu","level":"critical","message":f"CPU {cpu}%"})
        elif cpu >= self.cw: anomalies.append({"type":"cpu","level":"warning","message":f"CPU {cpu}%"})
        mem = data.get("memory", {}).get("used_percent", 0)
        if mem >= self.mc: anomalies.append({"type":"memory","level":"critical","message":f"内存 {mem}%"})
        elif mem >= self.mw: anomalies.append({"type":"memory","level":"warning","message":f"内存 {mem}%"})
        for d in data.get("disk", []):
            u = d.get("used_percent", 0)
            if u >= self.dc: anomalies.append({"type":"disk","level":"critical","message":f"磁盘 {d.get('mount','')} {u}%"})
            elif u >= self.dw: anomalies.append({"type":"disk","level":"warning","message":f"磁盘 {d.get('mount','')} {u}%"})
        failed = data.get("service", {}).get("failed", [])
        if failed: anomalies.append({"type":"service","level":"critical","message":f"{len(failed)} 个失败服务"})
        auth = data.get("log", {}).get("auth_failures", 0)
        if auth > 10: anomalies.append({"type":"auth","level":"warning","message":f"SSH认证失败 {auth} 次"})
        crit = sum(1 for a in anomalies if a["level"]=="critical")
        warn = sum(1 for a in anomalies if a["level"]=="warning")
        return {"anomalies": anomalies, "total": len(anomalies), "critical": crit, "warning": warn}
