"""关联分析器"""

class CorrelationAnalyzer:
    def analyze(self, data):
        findings = []
        cpu = data.get("cpu", {}).get("usage_percent", 0)
        mem = data.get("memory", {}).get("used_percent", 0)
        load = data.get("load", {}).get("load1", 0)
        cores = data.get("cpu", {}).get("cores", 1)
        if cpu > 70 and mem < 30: findings.append({"type":"cpu_mem_inverse","message":"CPU高内存低"})
        if load > cores*2 and cpu < 50: findings.append({"type":"io_wait","message":"负载高CPU低,IO等待"})
        return findings
