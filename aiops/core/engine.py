"""AIOps 引擎 - 安全版本"""
import logging
from typing import Optional, Dict, Any, List
from .config import Config, ServerConfig
from .ssh_manager import SSHManager
from .ai_agent import AIAgent
from ..tools.base import ToolRegistry, ToolCategory

logger = logging.getLogger(__name__)


class AIOpsEngine:
    """AIOps 引擎 - 核心控制中心"""

    def __init__(self, config: Optional[Config] = None, server: Optional[ServerConfig] = None):
        """
        初始化 AIOps 引擎

        Args:
            config: 配置对象
            server: 默认服务器配置
        """
        self.config = config or Config()
        self.server = server or self.config.get_default_server()

        # 初始化核心组件
        self.ssh = SSHManager(
            timeout=self.config.defaults.get("timeout", 10),
            retry=self.config.defaults.get("retry", 3),
            retry_delay=self.config.defaults.get("retry_delay", 5),
        )
        self.ai = AIAgent(self.config.ai)

        # 初始化工具注册中心
        self.tool_registry = ToolRegistry()
        self.tool_registry.config = self.config
        self.tool_registry.ssh = self.ssh

        # 模块注册
        self._modules: Dict[str, Any] = {}

        # 初始化工具
        self._init_tools()

        # 验证配置
        warnings = self.config.validate()
        if warnings:
            for warning in warnings:
                logger.warning(f"配置警告: {warning}")

        logger.info(f"AIOps 引擎初始化完成: {len(self.config.servers)} 个服务器, AI {'已启用' if self.ai.available else '未配置'}")

    def _init_tools(self):
        """初始化所有工具"""
        try:
            from ..tools.ssh_tools import SSHExecTool, SSHTestConnectionTool, SSHGetSystemInfoTool
            from ..tools.k8s_tools import (
                KubectlTool, K8sGetNodesTool, K8sGetPodsTool,
                K8sGetEventsTool, K8sLogsTool, K8sDescribePodTool,
                K8sRestartTool, K8sRollbackTool,
            )

            # SSH 工具
            self.tool_registry.register(SSHExecTool())
            self.tool_registry.register(SSHTestConnectionTool())
            self.tool_registry.register(SSHGetSystemInfoTool())

            # K8s 工具
            self.tool_registry.register(KubectlTool())
            self.tool_registry.register(K8sGetNodesTool())
            self.tool_registry.register(K8sGetPodsTool())
            self.tool_registry.register(K8sGetEventsTool())
            self.tool_registry.register(K8sLogsTool())
            self.tool_registry.register(K8sDescribePodTool())
            self.tool_registry.register(K8sRestartTool())
            self.tool_registry.register(K8sRollbackTool())

            logger.info(f"工具注册完成: {len(self.tool_registry.list_tools())} 个工具")

        except ImportError as e:
            logger.warning(f"部分工具加载失败: {e}")

    def register_module(self, name: str, module: Any):
        """注册功能模块"""
        self._modules[name] = module
        logger.debug(f"注册模块: {name}")

    def run_module(self, module_name: str, **kwargs) -> Dict[str, Any]:
        """
        运行功能模块

        Args:
            module_name: 模块名称
            **kwargs: 模块参数

        Returns:
            模块执行结果
        """
        if module_name not in self._modules:
            raise ValueError(f"模块 {module_name} 未注册")

        # 构建模块上下文
        ctx = {
            "engine": self,
            "ssh": self.ssh,
            "server": self.server,
            "config": self.config,
            "ai": self.ai,
            "tool_registry": self.tool_registry,
            "thresholds": self.config.thresholds,
            **kwargs,
        }

        logger.info(f"执行模块: {module_name}")

        try:
            module = self._modules[module_name]
            result = module.run(ctx)
            logger.info(f"模块 {module_name} 执行完成")
            return result
        except Exception as e:
            logger.error(f"模块 {module_name} 执行失败: {e}")
            raise

    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """
        执行工具

        Args:
            tool_name: 工具名称
            **kwargs: 工具参数

        Returns:
            工具执行结果
        """
        return self.tool_registry.execute(tool_name, kwargs)

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """获取所有工具的 schema"""
        return [tool.to_schema() for tool in self.tool_registry._tools.values()]

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计信息"""
        return {
            "servers": len(self.config.servers),
            "ai_enabled": self.ai.available,
            "modules": len(self._modules),
            "tools": len(self.tool_registry.list_tools()),
            "tool_stats": self.tool_registry.get_tool_stats(),
            "ssh_stats": self.ssh.get_connection_stats(),
        }

    def close(self):
        """关闭引擎，释放资源"""
        logger.info("关闭 AIOps 引擎...")
        self.ssh.close_all()
        logger.info("AIOps 引擎已关闭")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
        return False


def create_engine(config_path: Optional[str] = None, host: Optional[str] = None,
                  user: str = "root", port: int = 22) -> AIOpsEngine:
    """
    创建 AIOps 引擎的便捷函数

    Args:
        config_path: 配置文件路径
        host: 服务器地址
        user: 用户名
        port: 端口

    Returns:
        AIOpsEngine 实例
    """
    config = Config.load(config_path)

    # 如果指定了 host，创建临时服务器配置
    if host:
        server = ServerConfig(
            name="cli",
            host=host,
            port=port,
            user=user,
        )
    else:
        server = config.get_default_server()

    return AIOpsEngine(config=config, server=server)
