"""AIOps 引擎"""
from .config import Config, ServerConfig
from .ssh_manager import SSHManager
from .ai_agent import AIAgent

class AIOpsEngine:
    def __init__(self, config=None, server=None):
        self.config = config or Config(); self.server = server
        self.ssh = SSHManager(timeout=self.config.defaults.get("timeout", 10))
        self.ai = AIAgent(self.config.ai); self._modules = {}

    def register_module(self, name, module): self._modules[name] = module

    def run_module(self, module_name, **kwargs):
        ctx = {"engine": self, "ssh": self.ssh, "server": self.server,
               "config": self.config, "ai": self.ai, "thresholds": self.config.thresholds, **kwargs}
        return self._modules[module_name].run(ctx)

    def close(self): self.ssh.close()
