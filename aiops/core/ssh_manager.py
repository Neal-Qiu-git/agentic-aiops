"""SSH 连接管理器 - 安全版本"""
import os
import time
import logging
import paramiko
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@dataclass
class SSHConnectionInfo:
    """SSH 连接信息"""
    host: str
    port: int
    user: str
    connected_at: Optional[float] = None
    last_used: Optional[float] = None
    command_count: int = 0


class SSHManager:
    """SSH 连接管理器 - 支持连接池和重试"""

    def __init__(self, timeout: int = 10, retry: int = 3, retry_delay: int = 5,
                 max_connections: int = 10):
        """
        初始化 SSH 管理器

        Args:
            timeout: 连接超时时间
            retry: 重试次数
            retry_delay: 重试间隔
            max_connections: 最大连接数
        """
        self.timeout = timeout
        self.retry = retry
        self.retry_delay = retry_delay
        self.max_connections = max_connections
        self._clients: Dict[str, paramiko.SSHClient] = {}
        self._connection_info: Dict[str, SSHConnectionInfo] = {}

    def _get_connection_key(self, host: str, port: int, user: str) -> str:
        """生成连接唯一标识"""
        return f"{user}@{host}:{port}"

    def connect(self, host: str, port: int = 22, user: str = "root",
                password: Optional[str] = None, key_file: Optional[str] = None) -> paramiko.SSHClient:
        """
        建立 SSH 连接

        Args:
            host: 主机地址
            port: 端口
            user: 用户名
            password: 密码
            key_file: 密钥文件路径

        Returns:
            SSHClient 实例
        """
        key = self._get_connection_key(host, port, user)

        # 检查是否有现有连接
        if key in self._clients:
            client = self._clients[key]
            try:
                # 测试连接是否有效
                client.exec_command("echo ok", timeout=3)
                logger.debug(f"复用现有连接: {key}")
                return client
            except Exception as e:
                logger.warning(f"连接已失效，重新连接: {key}, 错误: {e}")
                self._remove_connection(key)

        # 检查连接数限制
        if len(self._clients) >= self.max_connections:
            logger.warning(f"连接数已达上限 ({self.max_connections})，关闭最旧的连接")
            self._close_oldest_connection()

        # 创建新连接
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 设置连接参数
        connect_kwargs: Dict[str, Any] = {
            "hostname": host,
            "port": port,
            "username": user,
            "timeout": self.timeout,
        }

        if key_file:
            key_file = os.path.expanduser(key_file)
            if not os.path.exists(key_file):
                raise ConnectionError(f"密钥文件不存在: {key_file}")
            connect_kwargs["key_filename"] = key_file
        elif password:
            connect_kwargs["password"] = password
        else:
            raise ConnectionError(f"未提供认证信息: {key}")

        # 重试连接
        last_error = None
        for attempt in range(self.retry):
            try:
                logger.info(f"SSH 连接尝试 {attempt + 1}/{self.retry}: {key}")
                client.connect(**connect_kwargs)

                # 记录连接信息
                self._clients[key] = client
                self._connection_info[key] = SSHConnectionInfo(
                    host=host,
                    port=port,
                    user=user,
                    connected_at=time.time(),
                    last_used=time.time(),
                )

                logger.info(f"SSH 连接成功: {key}")
                return client

            except paramiko.AuthenticationException as e:
                last_error = e
                logger.error(f"SSH 认证失败: {key}, 错误: {e}")
                # 认证失败不重试
                break

            except paramiko.SSHException as e:
                last_error = e
                logger.warning(f"SSH 连接错误: {key}, 错误: {e}")

            except Exception as e:
                last_error = e
                logger.warning(f"SSH 连接异常: {key}, 错误: {e}")

            # 重试前等待
            if attempt < self.retry - 1:
                logger.debug(f"等待 {self.retry_delay} 秒后重试...")
                time.sleep(self.retry_delay)

        # 所有重试都失败
        raise ConnectionError(f"SSH 连接失败 {key} (尝试 {self.retry} 次): {last_error}")

    def exec_command(self, host: str, command: str, port: int = 22, user: str = "root",
                     timeout: int = 30, password: Optional[str] = None,
                     key_file: Optional[str] = None) -> Tuple[str, str, int]:
        """
        执行远程命令

        Args:
            host: 主机地址
            command: 要执行的命令
            port: 端口
            user: 用户名
            timeout: 命令超时时间
            password: 密码
            key_file: 密钥文件路径

        Returns:
            (stdout, stderr, exit_code)
        """
        key = self._get_connection_key(host, port, user)

        try:
            client = self.connect(host, port, user, password, key_file)
        except ConnectionError as e:
            logger.error(f"无法连接到服务器: {e}")
            return "", str(e), 1

        try:
            logger.debug(f"执行命令: {command[:100]}...")

            # 使用 timeout 上下文管理器
            _, stdout, stderr = client.exec_command(command, timeout=timeout)

            # 读取输出
            stdout_str = stdout.read().decode("utf-8", errors="replace")
            stderr_str = stderr.read().decode("utf-8", errors="replace")
            exit_code = stdout.channel.recv_exit_status()

            # 更新连接信息
            if key in self._connection_info:
                self._connection_info[key].last_used = time.time()
                self._connection_info[key].command_count += 1

            logger.debug(f"命令执行完成: exit_code={exit_code}, stdout_len={len(stdout_str)}, stderr_len={len(stderr_str)}")

            return stdout_str, stderr_str, exit_code

        except paramiko.SSHException as e:
            error_msg = f"SSH 命令执行失败: {e}"
            logger.error(error_msg)
            # 连接可能已失效，移除
            self._remove_connection(key)
            return "", error_msg, 1

        except Exception as e:
            error_msg = f"命令执行异常: {e}"
            logger.error(error_msg)
            return "", error_msg, 1

    def _remove_connection(self, key: str):
        """移除连接"""
        if key in self._clients:
            try:
                self._clients[key].close()
            except Exception:
                pass
            del self._clients[key]
        if key in self._connection_info:
            del self._connection_info[key]

    def _close_oldest_connection(self):
        """关闭最旧的连接"""
        if not self._connection_info:
            return

        # 找到最旧的连接
        oldest_key = min(
            self._connection_info.keys(),
            key=lambda k: self._connection_info[k].connected_at or 0
        )
        logger.info(f"关闭最旧的连接: {oldest_key}")
        self._remove_connection(oldest_key)

    def get_connection_stats(self) -> Dict[str, Any]:
        """获取连接统计信息"""
        stats = {
            "total_connections": len(self._clients),
            "max_connections": self.max_connections,
            "connections": []
        }

        for key, info in self._connection_info.items():
            stats["connections"].append({
                "key": key,
                "host": info.host,
                "port": info.port,
                "user": info.user,
                "connected_at": info.connected_at,
                "last_used": info.last_used,
                "command_count": info.command_count,
            })

        return stats

    def close_all(self):
        """关闭所有连接"""
        for key in list(self._clients.keys()):
            self._remove_connection(key)
        logger.info("所有 SSH 连接已关闭")

    def close(self):
        """关闭所有连接（兼容旧接口）"""
        self.close_all()

    @contextmanager
    def get_connection(self, host: str, port: int = 22, user: str = "root",
                       password: Optional[str] = None, key_file: Optional[str] = None):
        """
        上下文管理器：获取 SSH 连接

        Usage:
            with ssh_manager.get_connection(host) as client:
                _, stdout, _ = client.exec_command("ls -la")
        """
        client = None
        try:
            client = self.connect(host, port, user, password, key_file)
            yield client
        except Exception as e:
            logger.error(f"获取连接失败: {e}")
            raise
        finally:
            # 不关闭连接，以便复用
            pass
