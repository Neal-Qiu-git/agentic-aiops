"""插件加载器"""
import os, importlib.util
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    name: str = "base"
    @abstractmethod
    def register(self, engine): pass

class PluginLoader:
    def __init__(self, plugin_dirs=None): self.plugin_dirs = plugin_dirs or ["./plugins"]
    def load_all(self, engine):
        loaded = []
        for d in self.plugin_dirs:
            if not os.path.isdir(d): continue
            for fn in os.listdir(d):
                if fn.endswith(".py") and not fn.startswith("_"):
                    try:
                        spec = importlib.util.spec_from_file_location(fn[:-3], os.path.join(d,fn))
                        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
                        for attr in dir(mod):
                            a = getattr(mod, attr)
                            if isinstance(a,type) and issubclass(a,BasePlugin) and a is not BasePlugin:
                                p = a(); p.register(engine); loaded.append(p)
                    except Exception as e: print(f"Plugin {fn} error: {e}")
        return loaded
