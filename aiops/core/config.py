"""配置管理 - 安全版本"""
import os
import yaml
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ServerConfig:
    """服务器配置"""
    name: str = "default"
    host: str = ""
    port: int = 22
    user: str = "root"
    # 敏感信息：优先从环境变量读取
    password: Optional[str] = None
    key_file: Optional[str] = None

    def __post_init__(self):
        """初始化后从环境变量加载敏感信息"""
        # 密码: 环境变量 > 配置文件
        env_key = f"AIOPS_SERVER_{self.name.upper()}_PASSWORD"
        if env_key in os.environ:
            self.password = os.environ[env_key]
        elif self.password:
            logger.warning(f"警告: 服务器 {self.name} 的密码存储在配置文件中，建议使用环境变量 {env_key}")

        # 密钥文件: 环境变量 > 配置文件
        env_key_file = f"AIOPS_SERVER_{self.name.upper()}_KEY_FILE"
        if env_key_file in os.environ:
            self.key_file = os.environ[env_key_file]

    @property
    def has_auth(self) -> bool:
        """检查是否有认证信息"""
        return bool(self.password or self.key_file)

    def get_connection_params(self) -> Dict[str, Any]:
        """获取连接参数"""
        params = {
            "hostname": self.host,
            "port": self.port,
            "username": self.user,
        }
        if self.key_file:
            params["key_filename"] = os.path.expanduser(self.key_file)
        elif self.password:
            params["password"] = self.password
        return params


@dataclass
class AIConfig:
    """AI 配置"""
    enabled: bool = False
    provider: str = "deepseek"
    api_key: str = ""
    model: str = "deepseek-chat"
    base_url: str = "https://api.deepseek.com/v1"
    # 安全配置
    max_tokens: int = 4096
    temperature: float = 0.2
    timeout: int = 30

    def __post_init__(self):
        """初始化后从环境变量加载敏感信息"""
        # API Key: 环境变量 > 配置文件
        env_key = "AIOPS_AI_API_KEY"
        if env_key in os.environ:
            self.api_key = os.environ[env_key]
        elif self.api_key:
            logger.warning("警告: AI API Key 存储在配置文件中，建议使用环境变量 AIOPS_AI_API_KEY")

        # Provider 特定的环境变量
        provider_env_keys = {
            "deepseek": "DEEPSEEK_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
        }
        if not self.api_key and self.provider in provider_env_keys:
            self.api_key = os.environ.get(provider_env_keys[self.provider], "")

    @property
    def is_configured(self) -> bool:
        """检查是否已配置"""
        return self.enabled and bool(self.api_key)


@dataclass
class Thresholds:
    """告警阈值配置"""
    cpu_warning: int = 70
    cpu_critical: int = 90
    mem_warning: int = 75
    mem_critical: int = 90
    disk_warning: int = 75
    disk_critical: int = 90
    load_warning: float = 2.0
    load_critical: float = 5.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Thresholds":
        """从字典创建配置"""
        cpu = data.get("cpu", {})
        memory = data.get("memory", {})
        disk = data.get("disk", {})
        load = data.get("load", {})
        return cls(
            cpu_warning=cpu.get("warning", 70),
            cpu_critical=cpu.get("critical", 90),
            mem_warning=memory.get("warning", 75),
            mem_critical=memory.get("critical", 90),
            disk_warning=disk.get("warning", 75),
            disk_critical=disk.get("critical", 90),
            load_warning=load.get("warning", 2.0),
            load_critical=load.get("critical", 5.0),
        )


@dataclass
class SecurityConfig:
    """安全配置"""
    # 命令白名单
    allowed_commands: List[str] = field(default_factory=lambda: [
        "kubectl", "docker", "systemctl", "journalctl", "ps", "top", "htop",
        "df", "free", "uptime", "whoami", "id", "uname", "cat", "grep",
        "head", "tail", "wc", "ls", "find", "du", "stat",
    ])
    # 命令黑名单
    blocked_commands: List[str] = field(default_factory=lambda: [
        "rm -rf", "mkfs", "dd", "format", "shutdown", "reboot", "init",
        "kill -9", "killall", "pkill", "chmod 777", "chown",
    ])
    # 危险路径
    blocked_paths: List[str] = field(default_factory=lambda: [
        "/etc/shadow", "/etc/passwd", "/root/.ssh", "/etc/sudoers",
    ])
    # 最大输出大小
    max_output_size: int = 10000
    # 命令执行超时
    command_timeout: int = 60
    # 启用审计日志
    audit_logging: bool = True


@dataclass
class Config:
    """主配置"""
    servers: List[ServerConfig] = field(default_factory=list)
    defaults: Dict[str, Any] = field(default_factory=lambda: {
        "timeout": 10,
        "retry": 3,
        "retry_delay": 5,
    })
    ai: AIConfig = field(default_factory=AIConfig)
    thresholds: Thresholds = field(default_factory=Thresholds)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    log_files: List[str] = field(default_factory=lambda: [
        "/var/log/syslog",
        "/var/log/auth.log",
        "/var/log/nginx/error.log",
    ])
    error_patterns: List[str] = field(default_factory=lambda: [
        "ERROR", "FATAL", "OOM", "Connection refused",
        "timeout", "permission denied", " segmentation fault",
    ])
    sensitive_ports: List[int] = field(default_factory=lambda: [
        22, 3306, 5432, 6379, 27017, 8080, 443,
    ])

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """
        加载配置文件

        优先级: 环境变量 > 配置文件 > 默认值
        """
        if config_path is None:
            config_path = os.environ.get("AIOPS_CONFIG", "config.yaml")

        cfg = cls()

        # 检查配置文件是否存在
        config_file = Path(config_path)
        if not config_file.exists():
            logger.info(f"配置文件 {config_path} 不存在，使用默认配置")
            return cfg

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            logger.error(f"配置文件解析失败: {e}")
            return cfg
        except Exception as e:
            logger.error(f"配置文件读取失败: {e}")
            return cfg

        # 加载服务器配置
        for s in data.get("servers", []):
            server = ServerConfig(
                name=s.get("name", "default"),
                host=s.get("host", ""),
                port=s.get("port", 22),
                user=s.get("user", "root"),
                password=s.get("password"),  # 注意：这会被环境变量覆盖
                key_file=s.get("key_file"),
            )
            if server.host:  # 只添加有效的服务器
                cfg.servers.append(server)

        # 加载 AI 配置
        ai_data = data.get("ai", {})
        cfg.ai = AIConfig(
            enabled=ai_data.get("enabled", False),
            provider=ai_data.get("provider", "deepseek"),
            api_key=ai_data.get("api_key", ""),  # 注意：这会被环境变量覆盖
            model=ai_data.get("model", "deepseek-chat"),
            base_url=ai_data.get("base_url", "https://api.deepseek.com/v1"),
            max_tokens=ai_data.get("max_tokens", 4096),
            temperature=ai_data.get("temperature", 0.2),
            timeout=ai_data.get("timeout", 30),
        )

        # 加载阈值配置
        cfg.thresholds = Thresholds.from_dict(data.get("thresholds", {}))

        # 加载安全配置
        security_data = data.get("security", {})
        cfg.security = SecurityConfig(
            allowed_commands=security_data.get("allowed_commands", cfg.security.allowed_commands),
            blocked_commands=security_data.get("blocked_commands", cfg.security.blocked_commands),
            blocked_paths=security_data.get("blocked_paths", cfg.security.blocked_paths),
            max_output_size=security_data.get("max_output_size", 10000),
            command_timeout=security_data.get("command_timeout", 60),
            audit_logging=security_data.get("audit_logging", True),
        )

        # 加载其他配置
        cfg.log_files = data.get("log_files", cfg.log_files)
        cfg.error_patterns = data.get("error_patterns", cfg.error_patterns)
        cfg.sensitive_ports = data.get("sensitive_ports", cfg.sensitive_ports)

        logger.info(f"配置加载完成: {len(cfg.servers)} 个服务器, AI {'已启用' if cfg.ai.is_configured else '未配置'}")
        return cfg

    def get_server(self, name: Optional[str] = None, host: Optional[str] = None) -> Optional[ServerConfig]:
        """获取服务器配置"""
        for s in self.servers:
            if name and s.name == name:
                return s
            if host and s.host == host:
                return s
        return None

    def get_default_server(self) -> Optional[ServerConfig]:
        """获取默认服务器"""
        return self.servers[0] if self.servers else None

    def validate(self) -> List[str]:
        """验证配置，返回警告列表"""
        warnings = []

        if not self.servers:
            warnings.append("未配置任何服务器")

        for server in self.servers:
            if not server.host:
                warnings.append(f"服务器 {server.name} 缺少 host 配置")
            if not server.has_auth:
                warnings.append(f"服务器 {server.name} 缺少认证信息 (password 或 key_file)")

        if self.ai.enabled and not self.ai.api_key:
            warnings.append("AI 已启用但未配置 API Key")

        return warnings

    def save(self, config_path: str):
        """保存配置到文件（敏感信息会被清理）"""
        data = {
            "servers": [],
            "ai": {
                "enabled": self.ai.enabled,
                "provider": self.ai.provider,
                "model": self.ai.model,
                "base_url": self.ai.base_url,
            },
            "thresholds": {
                "cpu": {"warning": self.thresholds.cpu_warning, "critical": self.thresholds.cpu_critical},
                "memory": {"warning": self.thresholds.mem_warning, "critical": self.thresholds.mem_critical},
                "disk": {"warning": self.thresholds.disk_warning, "critical": self.thresholds.disk_critical},
            },
            "log_files": self.log_files,
            "error_patterns": self.error_patterns,
            "sensitive_ports": self.sensitive_ports,
        }

        # 服务器配置（不保存密码）
        for server in self.servers:
            server_data = {
                "name": server.name,
                "host": server.host,
                "port": server.port,
                "user": server.user,
            }
            # 只保存 key_file 路径，不保存密码
            if server.key_file:
                server_data["key_file"] = server.key_file
            data["servers"].append(server_data)

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

        logger.info(f"配置已保存到 {config_path}")
