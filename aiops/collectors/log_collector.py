"""日志采集器"""
from .base import BaseCollector

class LogCollector(BaseCollector):
    name = "log"
    def __init__(self, log_files=None, error_patterns=None):
        self.log_files = log_files or ["/var/log/syslog","/var/log/auth.log"]
        self.error_patterns = error_patterns or ["ERROR","FATAL","OOM","Connection refused"]
    def collect(self, ssh, server):
        errors = []
        for pattern in self.error_patterns:
            for lf in self.log_files:
                count = int(self._exec(ssh,server,f"grep -c '{pattern}' {lf} 2>/dev/null").strip() or 0)
                if count > 0: errors.append({"pattern":pattern,"file":lf,"count":count})
        auth = int(self._exec(ssh,server,"grep -c 'Failed password' /var/log/auth.log 2>/dev/null || echo 0").strip() or 0)
        return {"errors": errors, "auth_failures": auth}
