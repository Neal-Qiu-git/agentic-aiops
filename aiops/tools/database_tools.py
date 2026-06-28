"""数据库工具 - 支持多种数据库"""
import logging
from typing import Optional, Dict, Any, List
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


class MySQLTool(BaseTool):
    """MySQL 工具"""
    name = "mysql_query"
    description = "执行 MySQL 查询"
    category = ToolCategory.DATABASE
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "host": {"type": "string", "description": "数据库地址"},
            "port": {"type": "integer", "description": "端口", "default": 3306},
            "user": {"type": "string", "description": "用户名", "default": "root"},
            "password": {"type": "string", "description": "密码"},
            "database": {"type": "string", "description": "数据库名"},
            "query": {"type": "string", "description": "SQL 查询"},
        },
        "required": ["query"],
    }

    def execute(self, query: str, host: str = "localhost", port: int = 3306,
                user: str = "root", password: str = "", database: str = "",
                **kwargs) -> ToolResult:
        # 构建 mysql 命令
        cmd = f"mysql -h {host} -P {port} -u {user}"
        if password:
            cmd += f" -p'{password}'"
        if database:
            cmd += f" {database}"
        cmd += f' -e "{query}"'

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=30)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class RedisTool(BaseTool):
    """Redis 工具"""
    name = "redis_query"
    description = "执行 Redis 命令"
    category = ToolCategory.DATABASE
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "host": {"type": "string", "description": "Redis 地址"},
            "port": {"type": "integer", "description": "端口", "default": 6379},
            "password": {"type": "string", "description": "密码"},
            "command": {"type": "string", "description": "Redis 命令"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, host: str = "localhost", port: int = 6379,
                password: str = "", **kwargs) -> ToolResult:
        cmd = f"redis-cli -h {host} -p {port}"
        if password:
            cmd += f" -a '{password}'"
        cmd += f" {command}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=30)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class PostgreSQLTool(BaseTool):
    """PostgreSQL 工具"""
    name = "postgresql_query"
    description = "执行 PostgreSQL 查询"
    category = ToolCategory.DATABASE
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "host": {"type": "string", "description": "数据库地址"},
            "port": {"type": "integer", "description": "端口", "default": 5432},
            "user": {"type": "string", "description": "用户名"},
            "database": {"type": "string", "description": "数据库名"},
            "query": {"type": "string", "description": "SQL 查询"},
        },
        "required": ["query"],
    }

    def execute(self, query: str, host: str = "localhost", port: int = 5432,
                user: str = "postgres", database: str = "", **kwargs) -> ToolResult:
        cmd = f"psql -h {host} -p {port} -U {user}"
        if database:
            cmd += f" -d {database}"
        cmd += f' -c "{query}"'

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=30)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class MongoDBTool(BaseTool):
    """MongoDB 工具"""
    name = "mongodb_query"
    description = "执行 MongoDB 查询"
    category = ToolCategory.DATABASE
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "host": {"type": "string", "description": "MongoDB 地址"},
            "port": {"type": "integer", "description": "端口", "default": 27017},
            "database": {"type": "string", "description": "数据库名"},
            "collection": {"type": "string", "description": "集合名"},
            "query": {"type": "string", "description": "查询语句 (JSON)"},
        },
        "required": ["query"],
    }

    def execute(self, query: str, host: str = "localhost", port: int = 27017,
                database: str = "", collection: str = "", **kwargs) -> ToolResult:
        cmd = f"mongosh --host {host} --port {port}"
        if database:
            cmd += f" {database}"
        if collection:
            cmd += f" --eval 'db.{collection}.find({query}).pretty()' "
        else:
            cmd += f" --eval '{query}'"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=30)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ElasticsearchTool(BaseTool):
    """Elasticsearch 工具"""
    name = "elasticsearch_query"
    description = "执行 Elasticsearch 查询"
    category = ToolCategory.DATABASE
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "host": {"type": "string", "description": "ES 地址"},
            "port": {"type": "integer", "description": "端口", "default": 9200},
            "index": {"type": "string", "description": "索引名"},
            "query": {"type": "string", "description": "查询语句 (JSON)"},
        },
        "required": ["query"],
    }

    def execute(self, query: str, host: str = "localhost", port: int = 9200,
                index: str = "", **kwargs) -> ToolResult:
        url = f"http://{host}:{port}"
        if index:
            url += f"/{index}/_search"
        else:
            url += "/_search"

        cmd = f'curl -s "{url}" -H "Content-Type: application/json" -d \'{query}\''

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=30)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class KafkaTool(BaseTool):
    """Kafka 工具"""
    name = "kafka_query"
    description = "Kafka 消息队列管理"
    category = ToolCategory.DATABASE
    requires_ssh = True
    is_readonly = True

    parameters = {
        "type": "object",
        "properties": {
            "bootstrap_servers": {"type": "string", "description": "Kafka 地址"},
            "command": {"type": "string", "description": "kafka-console-consumer 命令"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, bootstrap_servers: str = "localhost:9092",
                **kwargs) -> ToolResult:
        cmd = f"kafka-topics --bootstrap-server {bootstrap_servers} {command}"

        try:
            ssh = self._registry.ssh
            server = self._registry.config.get_default_server()
            out, err, code = ssh.exec_command(server, cmd, timeout=30)

            return ToolResult(
                success=(code == 0),
                output=out.strip()[:5000],
                error=err.strip() if code != 0 else "",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))
