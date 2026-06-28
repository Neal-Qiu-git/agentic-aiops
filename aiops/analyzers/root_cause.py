"""根因分析器"""

class RootCauseAnalyzer:
    RULES = [
        {"name":"disk_full","conditions":["disk.full"],"description":"磁盘空间不足","fix":"du -sh /* | sort -rh | head"},
        {"name":"memory_leak","conditions":["memory.high"],"description":"内存泄漏","fix":"ps aux --sort=-%mem | head"},
        {"name":"service_down","conditions":["service.failed"],"description":"服务宕机","fix":"systemctl status"},
    ]
    def analyze(self, anomalies, correlations):
        features = set()
        for a in anomalies:
            if a.get("type")=="disk": features.add("disk.full")
            if a.get("type")=="memory" and a.get("level")=="critical": features.add("memory.high")
            if a.get("type")=="service": features.add("service.failed")
        matched = [{"rule":r["name"],"description":r["description"],"fix":r["fix"]} for r in self.RULES if all(c in features for c in r["conditions"])]
        return {"root_causes": matched, "features": list(features)}
