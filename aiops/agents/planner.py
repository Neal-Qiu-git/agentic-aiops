"""PlannerAgent + 所有专业 Agent"""
from .base import BaseAgent, AgentResult


class PlannerAgent(BaseAgent):
    name = "planner"
    description = "总控 Agent，负责任务分解和调度"
    role = "运维总控"
    task_description = "接收运维任务，分解为子任务，分配给专业 Agent 执行，汇总结果"
    tools = ["ssh_exec", "k8s_get_nodes", "k8s_get_pods", "docker_ps", "prometheus_query"]
    max_steps = 10

    def run(self, task, context=None):
        context = context or {}
        context["available_agents"] = ["linux_agent", "k8s_agent", "db_agent", "log_agent", "monitor_agent", "security_agent", "devops_agent", "docker_agent"]
        context["instruction"] = "你是总控Agent。分析任务后用合适的工具执行，逐步推进，最终给出完整报告。"
        return super().run(task, context)


class LinuxAgent(BaseAgent):
    name = "linux_agent"
    description = "Linux 系统运维专家"
    role = "Linux SRE"
    task_description = "处理 Linux 服务器性能问题、故障排查、系统优化"
    tools = ["ssh_exec"]
    max_steps = 12

    def run(self, task, context=None):
        context = context or {}
        context["expertise"] = "你是Linux运维专家。用top/vmstat/iostat/pidstat/netstat/dmesg诊断，给出修复建议。"
        return super().run(task, context)


class K8sAgent(BaseAgent):
    name = "k8s_agent"
    description = "Kubernetes 管理专家"
    role = "K8s 运维"
    task_description = "处理 K8s 集群管理、Pod 故障诊断、Deployment 管理"
    tools = ["k8s_get_nodes", "k8s_get_pods", "k8s_get_events", "k8s_logs", "k8s_describe_pod", "k8s_restart", "k8s_rollback"]
    max_steps = 12

    def run(self, task, context=None):
        context = context or {}
        context["expertise"] = "你是K8s专家。诊断流程:get_pods→get_events→describe_pod→logs→修复(重启/回滚/扩容)"
        return super().run(task, context)


class DBAgent(BaseAgent):
    name = "db_agent"
    description = "数据库运维专家"
    role = "DBA"
    task_description = "处理 MySQL/Redis 的性能问题和故障"
    tools = ["mysql_query", "redis_query", "ssh_exec"]
    max_steps = 10

    def run(self, task, context=None):
        context = context or {}
        context["expertise"] = "你是DBA。MySQL: SHOW PROCESSLIST/STATUS; Redis: INFO/SLOWLOG"
        return super().run(task, context)


class LogAgent(BaseAgent):
    name = "log_agent"
    description = "日志分析专家"
    role = "日志分析"
    task_description = "分析应用日志，追踪错误链路，定位根因"
    tools = ["ssh_exec", "log_search"]
    max_steps = 10

    def run(self, task, context=None):
        context = context or {}
        context["expertise"] = "你是日志分析专家。搜索ERROR/FATAL/OOM，追踪链路，关联时间线，定位根因。"
        return super().run(task, context)


class MonitorAgent(BaseAgent):
    name = "monitor_agent"
    description = "监控分析专家"
    role = "监控运维"
    task_description = "分析 Prometheus/Grafana 监控数据"
    tools = ["prometheus_query", "prometheus_alerts", "ssh_exec"]
    max_steps = 10

    def run(self, task, context=None):
        context = context or {}
        context["expertise"] = "你是监控分析专家。分析CPU/内存/磁盘/网络指标，识别异常趋势。"
        return super().run(task, context)


class SecurityAgent(BaseAgent):
    name = "security_agent"
    description = "安全巡检专家"
    role = "安全运维"
    task_description = "执行安全基线检查、漏洞扫描、入侵检测"
    tools = ["ssh_exec", "log_search"]
    max_steps = 10

    def run(self, task, context=None):
        context = context or {}
        context["expertise"] = "你是安全专家。检查SSH配置/防火墙/端口/用户权限/入侵痕迹。"
        return super().run(task, context)


class DevOpsAgent(BaseAgent):
    name = "devops_agent"
    description = "CI/CD 发布专家"
    role = "DevOps"
    task_description = "处理应用发布、回滚、CI/CD 流水线"
    tools = ["kubectl", "docker_ps", "docker_logs", "http_get", "ssh_exec"]
    max_steps = 10

    def run(self, task, context=None):
        context = context or {}
        context["expertise"] = "你是DevOps专家。发布流程:构建→镜像扫描→推送→更新Deployment→健康检查→失败回滚"
        return super().run(task, context)
