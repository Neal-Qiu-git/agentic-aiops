"""配置管理"""
import os, yaml
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ServerConfig:
    name: str = "default"; host: str = ""; port: int = 22
    user: str = "root"; password: Optional[str] = None; key_file: Optional[str] = None

@dataclass
class AIConfig:
    enabled: bool = False; provider: str = "deepseek"; api_key: str = ""
    model: str = "deepseek-chat"; base_url: str = "https://api.deepseek.com/v1"

@dataclass
class Thresholds:
    cpu_warning: int = 70; cpu_critical: int = 90
    mem_warning: int = 75; mem_critical: int = 90
    disk_warning: int = 75; disk_critical: int = 90

@dataclass
class Config:
    servers: list = field(default_factory=list)
    defaults: dict = field(default_factory=lambda: {"timeout": 10, "retry": 3})
    ai: AIConfig = field(default_factory=AIConfig)
    thresholds: Thresholds = field(default_factory=Thresholds)
    log_files: list = field(default_factory=lambda: ["/var/log/syslog", "/var/log/auth.log"])
    error_patterns: list = field(default_factory=lambda: ["ERROR", "FATAL", "OOM", "Connection refused"])
    sensitive_ports: list = field(default_factory=lambda: [22, 3306, 5432, 6379, 27017])

    @classmethod
    def load(cls, config_path=None):
        if config_path is None: config_path = os.environ.get("AIOPS_CONFIG", "config.yaml")
        cfg = cls()
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            for s in data.get("servers", []):
                cfg.servers.append(ServerConfig(name=s.get("name","default"), host=s.get("host",""),
                    port=s.get("port",22), user=s.get("user","root"), password=s.get("password")))
            ai = data.get("ai", {})
            cfg.ai = AIConfig(enabled=ai.get("enabled",False), api_key=ai.get("api_key","") or os.environ.get("AIOPS_AI_API_KEY",""))
            th = data.get("thresholds", {})
            cfg.thresholds = Thresholds(cpu_warning=th.get("cpu",{}).get("warning",70), cpu_critical=th.get("cpu",{}).get("critical",90),
                mem_warning=th.get("memory",{}).get("warning",75), mem_critical=th.get("memory",{}).get("critical",90))
        return cfg

    def get_server(self, name=None, host=None):
        for s in self.servers:
            if name and s.name == name: return s
            if host and s.host == host: return s
        return None
