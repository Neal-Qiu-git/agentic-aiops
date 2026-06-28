"""采集器基类"""
from abc import ABC, abstractmethod

class BaseCollector(ABC):
    name: str = "base"
    @abstractmethod
    def collect(self, ssh, server) -> dict: pass
    def _exec(self, ssh, server, command, timeout=30):
        out, _, _ = ssh.exec_command(server, command, timeout); return out
