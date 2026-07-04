"""中间件工具 - Nginx/Tomcat/RabbitMQ/Kafka/ES"""
import json
import logging
import subprocess
from typing import Optional
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _mw_cmd(cmd: str, timeout: int = 15) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class NginxTool(BaseTool):
    """Nginx 管理"""
    name = "nginx_manage"
    description = "Nginx 配置/状态/日志管理"
    category = ToolCategory.MIDDLEWARE
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "status/config/test/reload/connections/topsites", "default": "status"}}}

    def execute(self, action: str = "status", **kwargs) -> ToolResult:
        cmds = {
            "status": "systemctl status nginx 2>/dev/null; nginx -t 2>/dev/null",
            "config": "nginx -T 2>/dev/null | head -300",
            "test": "nginx -t 2>/dev/null",
            "reload": "nginx -s reload 2>/dev/null",
            "connections": "ss -s 2>/dev/null | head -5; echo '---'; netstat -an | grep :80 | wc -l",
            "topsites": "awk '{print $1}' /var/log/nginx/access.log 2>/dev/null | sort | uniq -c | sort -rn | head -20",
        }
        return _mw_cmd(cmds.get(action, cmds["status"]))


class TomcatTool(BaseTool):
    """Tomcat 管理"""
    name = "tomcat_manage"
    description = "Tomcat 状态/日志/线程管理"
    category = ToolCategory.MIDDLEWARE
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "status/threads/heap/logs", "default": "status"}, "catalina_home": {"type": "string", "default": "/opt/tomcat"}}}

    def execute(self, action: str = "status", catalina_home: str = "/opt/tomcat", **kwargs) -> ToolResult:
        if action == "status":
            return _mw_cmd(f"ps aux | grep -i tomcat | grep -v grep; ls {catalina_home}/logs/catalina.out 2>/dev/null && tail -5 {catalina_home}/logs/catalina.out")
        elif action == "threads":
            return _mw_cmd(f"jstack $(pgrep -f tomcat) 2>/dev/null | grep -c 'TIMED_WAITING\|WAITING\|RUNNABLE' || echo 'Tomcat not running'")
        elif action == "heap":
            return _mw_cmd(f"jmap -heap $(pgrep -f tomcat) 2>/dev/null || echo 'Cannot get heap info'")
        elif action == "logs":
            return _mw_cmd(f"tail -100 {catalina_home}/logs/catalina.out 2>/dev/null")
        return ToolResult(success=False, error="Invalid action")


class RabbitMQTool(BaseTool):
    """RabbitMQ 管理"""
    name = "rabbitmq_manage"
    description = "RabbitMQ 状态/队列/连接管理"
    category = ToolCategory.MIDDLEWARE
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "status/queues/connections/policies", "default": "status"}}}

    def execute(self, action: str = "status", **kwargs) -> ToolResult:
        cmds = {
            "status": "rabbitmqctl status 2>/dev/null || rabbitmqctl cluster_status 2>/dev/null",
            "queues": "rabbitmqctl list_queues name messages consumers memory 2>/dev/null",
            "connections": "rabbitmqctl list_connections name state 2>/dev/null",
            "policies": "rabbitmqctl list_policies 2>/dev/null",
        }
        return _mw_cmd(cmds.get(action, cmds["status"]), timeout=20)


class KafkaTool(BaseTool):
    """Kafka 管理"""
    name = "kafka_manage"
    description = "Kafka Topic/Consumer/Broker 管理"
    category = ToolCategory.MIDDLEWARE
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "topics/consumers/broker/offsets", "default": "topics"}, "kafka_home": {"type": "string", "default": "/opt/kafka"}, "topic": {"type": "string"}}}

    def execute(self, action: str = "topics", kafka_home: str = "/opt/kafka", topic: str = "", **kwargs) -> ToolResult:
        bin_path = f"{kafka_home}/bin"
        if action == "topics":
            return _mw_cmd(f"{bin_path}/kafka-topics.sh --list --bootstrap-server localhost:9092 2>/dev/null")
        elif action == "consumers":
            return _mw_cmd(f"{bin_path}/kafka-consumer-groups.sh --list --bootstrap-server localhost:9092 2>/dev/null")
        elif action == "broker":
            return _mw_cmd(f"{bin_path}/kafka-broker-api-versions.sh --bootstrap-server localhost:9092 2>/dev/null | head -20")
        elif action == "offsets" and topic:
            return _mw_cmd(f"{bin_path}/kafka-consumer-groups.sh --describe --group {topic} --bootstrap-server localhost:9092 2>/dev/null")
        return ToolResult(success=False, error="Invalid params")


class ElasticsearchTool(BaseTool):
    """Elasticsearch 管理"""
    name = "elasticsearch_manage"
    description = "Elasticsearch 集群/索引/搜索管理"
    category = ToolCategory.MIDDLEWARE
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "health/indices/stats/nodes", "default": "health"}, "es_url": {"type": "string", "default": "http://localhost:9200"}}}

    def execute(self, action: str = "health", es_url: str = "http://localhost:9200", **kwargs) -> ToolResult:
        endpoints = {
            "health": "_cluster/health",
            "indices": "_cat/indices?v&s=index:desc&h=index,health,docs.count,store.size",
            "stats": "_cluster/stats",
            "nodes": "_cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,disk.used_percent",
        }
        url = f"{es_url}/{endpoints.get(action, endpoints['health'])}"
        return _mw_cmd(f"curl -s '{url}' | head -100", timeout=10)


class TongWebTool(BaseTool):
    """东方通 TongWeb 管理"""
    name = "tongweb_manage"
    description = "TongWeb 应用服务器管理"
    category = ToolCategory.MIDDLEWARE
    requires_ssh = True
    is_readonly = True
    parameters = {"type": "object", "properties": {"action": {"type": "string", "description": "status/threads/deploy", "default": "status"}, "tongweb_home": {"type": "string", "default": "/opt/TongWeb"}}}

    def execute(self, action: str = "status", tongweb_home: str = "/opt/TongWeb", **kwargs) -> ToolResult:
        if action == "status":
            return _mw_cmd(f"ps aux | grep -i tongweb | grep -v grep; {tongweb_home}/bin/startup.sh status 2>/dev/null")
        elif action == "threads":
            return _mw_cmd(f"jstack $(pgrep -f TongWeb) 2>/dev/null | grep -c 'RUNNABLE\|WAITING' || echo 'TongWeb not running'")
        return ToolResult(success=False, error="Invalid action")
