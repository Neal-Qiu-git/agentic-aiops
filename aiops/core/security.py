"""安全验证模块 - 命令检查和输入验证"""
import re
import shlex
import logging
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """安全级别"""
    SAFE = "safe"
    WARNING = "warning"
    DANGEROUS = "dangerous"
    BLOCKED = "blocked"


@dataclass
class SecurityCheckResult:
    """安全检查结果"""
    level: SecurityLevel
    message: str
    command: str
    reason: Optional[str] = None

    @property
    def is_safe(self) -> bool:
        return self.level == SecurityLevel.SAFE

    @property
    def is_blocked(self) -> bool:
        return self.level == SecurityLevel.BLOCKED


class CommandValidator:
    """命令验证器"""

    # 危险命令模式
    DANGEROUS_PATTERNS = [
        # 文件系统破坏
        (r'rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+|-f\s+|)\s*/', "删除根目录文件"),
        (r'rm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+|-r\s+|)\s*/', "递归删除根目录"),
        (r'mkfs\.', "格式化文件系统"),
        (r'dd\s+if=', "直接磁盘写入"),
        (r'>\s*/dev/sd', "写入磁盘设备"),

        # 系统关闭
        (r'shutdown', "关闭系统"),
        (r'reboot', "重启系统"),
        (r'init\s+[06]', "切换到关机/重启运行级别"),
        (r'systemctl\s+(poweroff|reboot|shutdown)', "系统关机/重启"),

        # 进程管理
        (r'kill\s+-9\s+1\b', "终止 init 进程"),
        (r'killall', "终止所有进程"),
        (r'pkill', "按模式终止进程"),

        # 权限修改
        (r'chmod\s+777', "设置不安全的权限"),
        (r'chmod\s+[0-7]*7[0-7]*7\s+/', "设置根目录权限"),
        (r'chown\s+.*:.*\s*/etc/', "修改系统目录所有者"),

        # 网络
        (r'iptables\s+-F', "清空防火墙规则"),
        (r'echo\s+.*>\s*/etc/hosts', "修改 hosts 文件"),

        # 敏感文件
        (r'cat\s+/etc/shadow', "读取密码哈希"),
        (r'cat\s+/etc/sudoers', "读取 sudoers"),
        (r'visudo', "编辑 sudoers"),

        # 危险的管道
        (r'\|\s*sh', "通过管道执行 shell"),
        (r'\|\s*bash', "通过管道执行 bash"),
        (r'eval\s+', "执行动态命令"),
    ]

    # 敏感路径
    SENSITIVE_PATHS = [
        "/etc/shadow",
        "/etc/passwd",
        "/etc/sudoers",
        "/root/.ssh",
        "/etc/ssh/sshd_config",
        "/var/log/auth.log",
        "/etc/krb5.conf",
        "/etc/pam.d",
    ]

    # 危险字符
    DANGEROUS_CHARS = [";", "&&", "||", "|", "`", "$(", "${"]

    def __init__(self, allowed_commands: Optional[List[str]] = None,
                 blocked_commands: Optional[List[str]] = None,
                 blocked_paths: Optional[List[str]] = None):
        """
        初始化命令验证器

        Args:
            allowed_commands: 允许的命令白名单
            blocked_commands: 禁止的命令黑名单
            blocked_paths: 禁止访问的路径
        """
        self.allowed_commands = allowed_commands or []
        self.blocked_commands = blocked_commands or []
        self.blocked_paths = blocked_paths or self.SENSITIVE_PATHS

    def validate(self, command: str) -> SecurityCheckResult:
        """
        验证命令安全性

        Args:
            command: 要执行的命令

        Returns:
            SecurityCheckResult
        """
        if not command or not command.strip():
            return SecurityCheckResult(
                level=SecurityLevel.WARNING,
                message="空命令",
                command=command
            )

        command = command.strip()

        # 1. 检查命令黑名单
        for blocked in self.blocked_commands:
            if blocked.lower() in command.lower():
                return SecurityCheckResult(
                    level=SecurityLevel.BLOCKED,
                    message=f"命令被黑名单禁止: {blocked}",
                    command=command,
                    reason="匹配黑名单规则"
                )

        # 2. 检查危险命令模式
        for pattern, reason in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return SecurityCheckResult(
                    level=SecurityLevel.BLOCKED,
                    message=f"检测到危险命令: {reason}",
                    command=command,
                    reason=reason
                )

        # 3. 检查敏感路径访问
        for path in self.blocked_paths:
            if path in command:
                return SecurityCheckResult(
                    level=SecurityLevel.BLOCKED,
                    message=f"禁止访问敏感路径: {path}",
                    command=command,
                    reason=f"路径 {path} 在黑名单中"
                )

        # 4. 检查危险字符
        for char in self.DANGEROUS_CHARS:
            if char in command:
                return SecurityCheckResult(
                    level=SecurityLevel.WARNING,
                    message=f"包含潜在危险字符: {char}",
                    command=command,
                    reason="可能的命令注入风险"
                )

        # 5. 检查命令白名单（如果配置了）
        if self.allowed_commands:
            try:
                # 安全地分割命令
                parts = shlex.split(command)
                if parts and parts[0] not in self.allowed_commands:
                    return SecurityCheckResult(
                        level=SecurityLevel.WARNING,
                        message=f"命令不在白名单中: {parts[0]}",
                        command=command,
                        reason=f"允许的命令: {', '.join(self.allowed_commands[:5])}..."
                    )
            except ValueError:
                # shlex 分割失败，可能包含特殊字符
                return SecurityCheckResult(
                    level=SecurityLevel.WARNING,
                    message="命令解析失败，可能包含特殊字符",
                    command=command
                )

        # 6. 检查命令长度
        if len(command) > 1000:
            return SecurityCheckResult(
                level=SecurityLevel.WARNING,
                message=f"命令过长: {len(command)} 字符",
                command=command[:100] + "..."
            )

        # 7. 检查嵌套 shell
        if command.count("sh -c") > 0 or command.count("bash -c") > 0:
            return SecurityCheckResult(
                level=SecurityLevel.WARNING,
                message="检测到嵌套 shell 执行",
                command=command
            )

        # 通过所有检查
        return SecurityCheckResult(
            level=SecurityLevel.SAFE,
            message="命令验证通过",
            command=command
        )

    def sanitize_command(self, command: str) -> str:
        """
        清理命令（移除危险字符）

        Args:
            command: 原始命令

        Returns:
            清理后的命令
        """
        # 移除注释
        command = command.split("#")[0].strip()

        # 移除危险字符
        for char in self.DANGEROUS_CHARS:
            command = command.replace(char, "")

        return command


class InputValidator:
    """输入验证器"""

    # 正则表达式模式
    PATTERNS = {
        "ip": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        "hostname": r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$",
        "port": r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$",
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "path": r"^(/[a-zA-Z0-9._-]+)+/?$",
    }

    @classmethod
    def validate_ip(cls, ip: str) -> bool:
        """验证 IP 地址"""
        return bool(re.match(cls.PATTERNS["ip"], ip))

    @classmethod
    def validate_hostname(cls, hostname: str) -> bool:
        """验证主机名"""
        return bool(re.match(cls.PATTERNS["hostname"], hostname))

    @classmethod
    def validate_port(cls, port: str) -> bool:
        """验证端口号"""
        return bool(re.match(cls.PATTERNS["port"], str(port)))

    @classmethod
    def validate_path(cls, path: str) -> bool:
        """验证文件路径"""
        # 检查路径遍历
        if ".." in path:
            return False
        return bool(re.match(cls.PATTERNS["path"], path))

    @classmethod
    def validate_server_host(cls, host: str) -> Tuple[bool, str]:
        """
        验证服务器主机名

        Returns:
            (是否有效, 错误信息)
        """
        if not host:
            return False, "主机名不能为空"

        if cls.validate_ip(host):
            return True, ""

        if cls.validate_hostname(host):
            return True, ""

        return False, f"无效的主机名或 IP: {host}"


class OutputSanitizer:
    """输出清理器"""

    # 敏感信息模式
    SENSITIVE_PATTERNS = [
        (r'password[=:]\s*\S+', "password=***"),
        (r'passwd[=:]\s*\S+', "passwd=***"),
        (r'secret[=:]\s*\S+', "secret=***"),
        (r'token[=:]\s*\S+', "token=***"),
        (r'api[_-]?key[=:]\s*\S+', "api_key=***"),
        (r'access[_-]?key[=:]\s*\S+', "access_key=***"),
        (r'-----BEGIN\s+(RSA|DSA|EC|OPENSSH)\s+PRIVATE\s+KEY-----', "[私钥内容已隐藏]"),
    ]

    @classmethod
    def sanitize(cls, output: str, remove_sensitive: bool = True) -> str:
        """
        清理输出

        Args:
            output: 原始输出
            remove_sensitive: 是否移除敏感信息

        Returns:
            清理后的输出
        """
        if not output:
            return output

        # 限制输出长度
        if len(output) > 10000:
            output = output[:10000] + "\n... [输出已截断]"

        if remove_sensitive:
            for pattern, replacement in cls.SENSITIVE_PATTERNS:
                output = re.sub(pattern, replacement, output, flags=re.IGNORECASE)

        return output


def create_command_validator_from_config(config) -> CommandValidator:
    """从配置创建命令验证器"""
    return CommandValidator(
        allowed_commands=config.security.allowed_commands if hasattr(config, 'security') else None,
        blocked_commands=config.security.blocked_commands if hasattr(config, 'security') else None,
        blocked_paths=config.security.blocked_paths if hasattr(config, 'security') else None,
    )
