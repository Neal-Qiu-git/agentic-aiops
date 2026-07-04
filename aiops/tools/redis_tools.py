"""Redis 工具 - 单机/Cluster/Sentinel

Redis: 全球最流行的内存数据库, 用作缓存/消息/会话/排行榜
支持: 单机模式、Redis Cluster、Redis Sentinel、Redis Streams
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _redis_cmd(host: str, port: int, cmd: str, timeout: int = 15) -> ToolResult:
    try:
        r = subprocess.run(f"redis-cli -h {host} -p {port} {cmd}",
                           shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class RedisQueryTool(BaseTool):
    """Redis 通用命令"""
    name = "redis_query"
    description = "执行 Redis 命令 (GET/SET/HGET/SCAN 等)"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "command": {"type": "string", "description": "Redis 命令"},
        "host": {"type": "string", "default": "127.0.0.1"},
        "port": {"type": "integer", "default": 6379},
    }, "required": ["command"]}

    def execute(self, command: str, host: str = "127.0.0.1", port: int = 6379, **kw):
        return _redis_cmd(host, port, command)


class RedisInfo(BaseTool):
    """Redis 服务器信息"""
    name = "redis_info"
    description = "获取 Redis 服务器详细信息 (内存/连接/命中率/复制)"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "section": {"type": "string", "description": "all/server/memory/clients/stats/replication", "default": "all"},
        "host": {"type": "string", "default": "127.0.0.1"},
        "port": {"type": "integer", "default": 6379},
    }}

    def execute(self, section: str = "all", host: str = "127.0.0.1", port: int = 6379, **kw):
        return _redis_cmd(host, port, f"INFO {section}")


class RedisSlowlog(BaseTool):
    """Redis 慢查询日志"""
    name = "redis_slowlog"
    description = "查询 Redis 慢查询日志"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "count": {"type": "integer", "default": 10},
        "host": {"type": "string", "default": "127.0.0.1"},
        "port": {"type": "integer", "default": 6379},
    }}

    def execute(self, count: int = 10, host: str = "127.0.0.1", port: int = 6379, **kw):
        return _redis_cmd(host, port, f"SLOWLOG GET {count}")


class RedisClusterInfo(BaseTool):
    """Redis Cluster 状态"""
    name = "redis_cluster_info"
    description = "获取 Redis Cluster 节点/槽位/状态"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "info/nodes/slots/reshard-check", "default": "info"},
        "host": {"type": "string", "default": "127.0.0.1"},
        "port": {"type": "integer", "default": 6379},
    }}

    def execute(self, action: str = "info", host: str = "127.0.0.1", port: int = 6379, **kw):
        cmds = {
            "info": "CLUSTER INFO",
            "nodes": "CLUSTER NODES",
            "slots": "CLUSTER SLOTS",
        }
        return _redis_cmd(host, port, cmds.get(action, cmds["info"]))


class RedisKeyAnalysis(BaseTool):
    """Redis Key 分析"""
    name = "redis_key_analysis"
    description = "分析 Redis Key 使用情况 (类型分布/大 Key/TTL)"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "types/bigkeys/memory", "default": "types"},
        "host": {"type": "string", "default": "127.0.0.1"},
        "port": {"type": "integer", "default": 6379},
    }}

    def execute(self, action: str = "types", host: str = "127.0.0.1", port: int = 6379, **kw):
        cmds = {
            "bigkeys": "BIGKEYS --memkeys",
            "memory": "MEMORY DOCTOR",
        }
        if action == "types":
            return _redis_cmd(host, port, "INFO keyspace")
        return _redis_cmd(host, port, cmds.get(action, "INFO keyspace"))


class RedisSentinel(BaseTool):
    """Redis Sentinel 高可用"""
    name = "redis_sentinel"
    description = "Redis Sentinel 主从/故障转移状态"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "masters/slaves/sentinels", "default": "masters"},
        "host": {"type": "string", "default": "127.0.0.1"},
        "port": {"type": "integer", "default": 26379},
    }}

    def execute(self, action: str = "masters", host: str = "127.0.0.1", port: int = 26379, **kw):
        cmds = {
            "masters": "SENTINEL masters",
            "slaves": "SENTINEL replicas mymaster",
            "sentinels": "SENTINEL sentinels mymaster",
        }
        return _redis_cmd(host, port, cmds.get(action, cmds["masters"]))
