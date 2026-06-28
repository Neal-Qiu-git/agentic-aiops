"""日志诊断模块"""
from ..collectors.log_collector import LogCollector

class LogDiagnosisModule:
    name = "log-diagnosis"
    def run(self, ctx):
        ssh, server, config = ctx["ssh"], ctx["server"], ctx["config"]
        collector = LogCollector(config.log_files, config.error_patterns)
        log_data = collector.collect(ssh, server)
        stats = {"total_errors": sum(e.get("count",0) for e in log_data.get("errors",[])),
                 "files_with_errors": len(set(e.get("file","") for e in log_data.get("errors",[])))}
        return {"log_data": log_data, "stats": stats}
