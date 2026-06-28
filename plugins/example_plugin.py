"""示例插件"""
from aiops.plugins.loader import BasePlugin

class ExamplePlugin(BasePlugin):
    name = "example"
    def register(self, engine): pass
