"""Middleware Agent - 中间件运维专家"""
from .base import BaseAgent, AgentResult


class MiddlewareAgent(BaseAgent):
    """Middleware Agent - 负责中间件管理"""

    name = "middleware"
    description = "Middleware Agent - 中间件运维（Nginx/Tomcat/RabbitMQ/Kafka/ES）"
    role = "中间件运维专家"
    task_description = "处理 Nginx/Tomcat/RabbitMQ/Kafka/Elasticsearch/Redis 中间件管理和故障排查"
    tools = [
        "ssh_exec", "http_get", "log_search", "prometheus_query",
    ]
    max_steps = 12

    def run(self, task: str, context: dict = None) -> AgentResult:
        context = context or {}
        context["expertise"] = """你是中间件运维专家：
1. Web 服务器: Nginx/Apache/IIS/Tomcat 配置优化
2. 消息队列: RabbitMQ/Kafka/RocketMQ/Pulsar
3. 搜索引擎: Elasticsearch/Logsol/Kibana
4. 缓存: Redis/Memcached/Hazelcast
5. 应用服务器: Tomcat/WebLogic/WildFly/TongWeb
6. API 网关: Kong/APISIX/Nginx
7. 连接池: 数据库连接池/HTTP 连接池

执行流程：
1. 检查中间件服务状态和进程
2. 分析配置文件和性能指标
3. 查看日志定位错误和瓶颈
4. 调优配置参数（连接数/线程池/内存）
5. 验证修复效果
"""
        return super().run(task, context)
