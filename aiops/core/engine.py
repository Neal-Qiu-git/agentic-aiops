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
        registered = 0

        # --- 基础工具 ---
        try:
            from ..tools.ssh_tools import SSHExecTool, SSHTestConnectionTool, SSHGetSystemInfoTool
            for t in [SSHExecTool(), SSHTestConnectionTool(), SSHGetSystemInfoTool()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"SSH 工具加载失败: {e}")

        try:
            from ..tools.k8s_tools import (KubectlTool, K8sGetNodesTool, K8sGetPodsTool,
                K8sGetEventsTool, K8sLogsTool, K8sDescribePodTool, K8sRestartTool, K8sRollbackTool,
                K8sGetDeploymentsTool, K8sGetNamespacesTool, K8sGetServicesTool, K8sScaleDeploymentTool)
            for t in [KubectlTool(), K8sGetNodesTool(), K8sGetPodsTool(), K8sGetEventsTool(),
                      K8sLogsTool(), K8sDescribePodTool(), K8sRestartTool(), K8sRollbackTool(),
                      K8sGetDeploymentsTool(), K8sGetNamespacesTool(), K8sGetServicesTool(), K8sScaleDeploymentTool()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"K8s 工具加载失败: {e}")

        try:
            from ..tools.docker_tools import (DockerPS, DockerLogs, DockerInspect, DockerStats,
                DockerCompose, DockerNetwork, DockerVolume)
            for t in [DockerPS(), DockerLogs(), DockerInspect(), DockerStats(),
                      DockerCompose(), DockerNetwork(), DockerVolume()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"Docker 工具加载失败: {e}")

        # --- 可观测性工具 (v4.3.0) ---
        try:
            from ..tools.prometheus_tools import (PrometheusQueryTool, PrometheusRangeQueryTool,
                PrometheusAlertsTool, PrometheusTargetsTool, PrometheusSummaryTool)
            for t in [PrometheusQueryTool(), PrometheusRangeQueryTool(),
                      PrometheusAlertsTool(), PrometheusTargetsTool(), PrometheusSummaryTool()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"Prometheus 工具加载失败: {e}")

        try:
            from ..tools.grafana_tools import GrafanaDashboards, GrafanaQuery, GrafanaAnnotations, GrafanaAlertRules
            for t in [GrafanaDashboards(), GrafanaQuery(), GrafanaAnnotations(), GrafanaAlertRules()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"Grafana 工具加载失败: {e}")

        try:
            from ..tools.loki_tools import LokiQuery, LokiLabels, LokiLabelValues, LokiSeries
            for t in [LokiQuery(), LokiLabels(), LokiLabelValues(), LokiSeries()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"Loki 工具加载失败: {e}")

        try:
            from ..tools.alertmanager_tools import AlertmanagerAlerts, AlertmanagerSilence, AlertmanagerStatus
            for t in [AlertmanagerAlerts(), AlertmanagerSilence(), AlertmanagerStatus()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"Alertmanager 工具加载失败: {e}")

        try:
            from ..tools.apm_tools import SkyWalkingService, SkyWalkingMetrics, JaegerTraces, OpenTelemetryCollector
            for t in [SkyWalkingService(), SkyWalkingMetrics(), JaegerTraces(), OpenTelemetryCollector()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"APM 工具加载失败: {e}")

        # --- 数据库工具 ---
        try:
            from ..tools.database_tools import MySQLTool, RedisTool, PostgreSQLTool, MongoDBTool, ElasticsearchTool, KafkaTool
            for t in [MySQLTool(), RedisTool(), PostgreSQLTool(), MongoDBTool(), ElasticsearchTool(), KafkaTool()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"数据库工具加载失败: {e}")

        try:
            from ..tools.enterprise_db_tools import OracleTool, ClickHouseTool, TiDBTool, DM8Tool, OceanBaseTool, KingbaseESTool
            for t in [OracleTool(), ClickHouseTool(), TiDBTool(), DM8Tool(), OceanBaseTool(), KingbaseESTool()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"企业数据库工具加载失败: {e}")

        # --- 中间件工具 ---
        try:
            from ..tools.middleware_tools import NginxTool, TomcatTool, RabbitMQTool, TongWebTool
            for t in [NginxTool(), TomcatTool(), RabbitMQTool(), TongWebTool()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"中间件工具加载失败: {e}")

        try:
            from ..tools.middleware_ext_tools import PulsarTool, NATSTool, TraefikTool, HAProxyTool, ConsulTool
            for t in [PulsarTool(), NATSTool(), TraefikTool(), HAProxyTool(), ConsulTool()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"扩展中间件工具加载失败: {e}")

        # --- 云平台工具 ---
        try:
            from ..tools.cloud_tools import AzureCLI, AliyunCLI, TencentCLI, HuaweiCLI
            for t in [AzureCLI(), AliyunCLI(), TencentCLI(), HuaweiCLI()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"云平台工具加载失败: {e}")

        # --- 虚拟化工具 ---
        try:
            from ..tools.virtual_tools import VMwareTool, LibvirtTool, ProxmoxTool
            for t in [VMwareTool(), LibvirtTool(), ProxmoxTool()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"虚拟化工具加载失败: {e}")

        # --- Windows 工具 ---
        try:
            from ..tools.windows_tools import WinRMExec, WinRMEventLog, WinRMService
            for t in [WinRMExec(), WinRMEventLog(), WinRMService()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"Windows 工具加载失败: {e}")

        # --- 网络工具 ---
        try:
            from ..tools.network_tools import FirewallTool, LoadBalancerTool, DNSTool, NetworkDiagTool, VPNTool
            for t in [FirewallTool(), LoadBalancerTool(), DNSTool(), NetworkDiagTool(), VPNTool()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"网络工具加载失败: {e}")

        # --- 日志工具 ---
        try:
            from ..tools.log_tools import LogSearchTool
            self.tool_registry.register(LogSearchTool()); registered += 1
        except ImportError as e:
            logger.warning(f"日志工具加载失败: {e}")

        # --- IaC / GitOps 工具 (v4.3.0) ---
        try:
            from ..tools.terraform_tools import TerraformInit, TerraformPlan, TerraformApply, TerraformState, TerraformOutput, TerraformValidate
            for t in [TerraformInit(), TerraformPlan(), TerraformApply(), TerraformState(), TerraformOutput(), TerraformValidate()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"Terraform 工具加载失败: {e}")

        try:
            from ..tools.gitops_tools import ArgoCDApps, ArgoCDProjects, ArgoCDRepositories, FluxGetResources, FluxReconcile
            for t in [ArgoCDApps(), ArgoCDProjects(), ArgoCDRepositories(), FluxGetResources(), FluxReconcile()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"GitOps 工具加载失败: {e}")

        # --- CI/CD 工具 (v4.3.0) ---
        try:
            from ..tools.cicd_tools import JenkinsJob, GitLabCI, GitHubActions
            for t in [JenkinsJob(), GitLabCI(), GitHubActions()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"CI/CD 工具加载失败: {e}")

        # --- 安全工具 (v4.3.0) ---
        try:
            from ..tools.security_tools import TrivyScan, TrivyRepo, FalcoRules, OPAEvaluate, KubeBench, KubescapeScan
            for t in [TrivyScan(), TrivyRepo(), FalcoRules(), OPAEvaluate(), KubeBench(), KubescapeScan()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"安全工具加载失败: {e}")

        # --- FinOps 工具 (v4.3.0) ---
        try:
            from ..tools.finops_tools import KubecostAllocation, KubecostAssets, AWSCostExplorer, AzureCost
            for t in [KubecostAllocation(), KubecostAssets(), AWSCostExplorer(), AzureCost()]:
                self.tool_registry.register(t); registered += 1
        except ImportError as e:
            logger.warning(f"FinOps 工具加载失败: {e}")

        logger.info(f"工具注册完成: {registered} 个工具")

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
