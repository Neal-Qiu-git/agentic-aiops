"""REST API Server - Enhanced with CORS + Monitoring + Deployment + Static Dashboard"""
import json
import logging
import time
import os
import mimetypes
from typing import Dict, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

# Dashboard 静态文件目录
WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")


class AIOpsHandler(BaseHTTPRequestHandler):
    """AIOps HTTP Handler with CORS + Static file serving"""

    def __init__(self, *args, engine=None, **kwargs):
        self.engine = engine
        super().__init__(*args, **kwargs)

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # ===== API 路由 =====
        if path.startswith("/api/"):
            self._handle_api(path, params)
            return

        # ===== 静态文件服务 =====
        self._serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b""
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._respond(400, {"error": "Invalid JSON"})
            return

        if path == "/api/v1/diagnose":
            self._diagnose(data)
        elif path == "/api/v1/tools/execute":
            self._execute_tool(data)
        elif path == "/api/v1/workflow/run":
            self._run_workflow(data)
        elif path == "/api/v1/approval/create":
            self._create_approval(data)
        elif path == "/api/v1/deployment/scale":
            self._deployment_scale(data)
        else:
            self._respond(404, {"error": "Not found"})

    # ===== 静态文件服务 =====
    def _serve_static(self, path: str):
        """serve dashboard 静态文件"""
        # 移除查询参数
        path = path.split("?")[0]

        # 默认路径 -> index.html
        if path == "/" or path == "":
            path = "/index.html"

        # 映射到 web 目录
        file_path = os.path.join(WEB_DIR, path.lstrip("/"))

        # 安全检查：防止目录遍历
        real_web = os.path.realpath(WEB_DIR)
        real_file = os.path.realpath(file_path)
        if not real_file.startswith(real_web):
            self._respond(403, {"error": "Forbidden"})
            return

        # 检查文件是否存在
        if os.path.isfile(file_path):
            self._send_file(file_path)
        else:
            # SPA fallback: 不存在的路径返回 index.html（支持前端路由）
            index_path = os.path.join(WEB_DIR, "index.html")
            if os.path.isfile(index_path):
                self._send_file(index_path)
            else:
                self._respond(404, {"error": "Not found"})

    def _send_file(self, file_path: str):
        """发送静态文件"""
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            # 静态资源缓存1小时，HTML不缓存
            if file_path.endswith(".html"):
                self.send_header("Cache-Control", "no-cache")
            else:
                self.send_header("Cache-Control", "public, max-age=3600")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            logger.error(f"发送文件失败: {e}")
            self._respond(500, {"error": "Internal server error"})

    # ===== API 路由分发 =====
    def _handle_api(self, path: str, params: dict):
        if path == "/api/v1/health":
            self._respond(200, {"status": "healthy", "dashboard": True})
        elif path == "/api/v1/version":
            from aiops import __version__
            self._respond(200, {"version": __version__})
        elif path == "/api/v1/tools":
            self._list_tools()
        elif path == "/api/v1/agents":
            self._list_agents()
        elif path == "/api/v1/monitoring/summary":
            self._monitoring_summary(params)
        elif path == "/api/v1/monitoring/metrics":
            self._monitoring_metrics(params)
        elif path == "/api/v1/monitoring/alerts":
            self._monitoring_alerts(params)
        elif path == "/api/v1/monitoring/targets":
            self._monitoring_targets(params)
        elif path == "/api/v1/deployment/summary":
            self._deployment_summary(params)
        elif path == "/api/v1/deployment/nodes":
            self._deployment_nodes(params)
        elif path == "/api/v1/deployment/pods":
            self._deployment_pods(params)
        elif path == "/api/v1/deployment/deployments":
            self._deployment_deployments(params)
        elif path == "/api/v1/deployment/events":
            self._deployment_events(params)
        elif path == "/api/v1/deployment/namespaces":
            self._deployment_namespaces(params)
        elif path == "/api/v1/deployment/services":
            self._deployment_services(params)
        elif path == "/api/v1/deployment/scale":
            pass  # handled in POST
        elif path.startswith("/api/v1/environments"):
            self._handle_environments(path, params)
        elif path == "/api/v1/discovery":
            self._handle_discovery()
        elif path == "/api/v1/slo":
            self._slo_data(params)
        elif path == "/api/v1/events":
            self._event_logs(params)
        elif path == "/api/v1/workflows":
            self._workflows_data(params)
        elif path == "/api/v1/network/connections":
            self._network_connections(params)
        elif path == "/api/v1/multicloud":
            self._multicloud_data(params)
        elif path == "/api/v1/audit":
            self._audit_logs(params)
        elif path == "/api/v1/cost/summary":
            self._cost_summary(params)
        elif path == "/api/v1/security/summary":
            self._security_summary(params)
        else:
            self._respond(404, {"error": "API not found"})

    def _respond(self, status: int, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    # ===== 监控 =====
    def _monitoring_summary(self, params):
        try:
            from aiops.tools.prometheus_tools import _demo_summary
            self._respond(200, _demo_summary())
        except Exception:
            self._respond(200, {"status": "demo", "data": {"cpu_usage": 42, "memory_usage": 67, "disk_usage": 68}})

    def _monitoring_metrics(self, params):
        query = params.get("query", ["cpu"])[0]
        try:
            from aiops.tools.prometheus_tools import _demo_cpu_data, _demo_memory_data
            if "mem" in query.lower():
                self._respond(200, _demo_memory_data())
            else:
                self._respond(200, _demo_cpu_data())
        except Exception:
            self._respond(200, {"status": "demo", "data": {"resultType": "matrix", "result": []}})

    def _monitoring_alerts(self, params):
        try:
            from aiops.tools.prometheus_tools import _demo_alerts
            self._respond(200, _demo_alerts())
        except Exception:
            self._respond(200, {"status": "demo", "data": {"alerts": []}})

    def _monitoring_targets(self, params):
        try:
            from aiops.tools.prometheus_tools import _demo_targets
            self._respond(200, _demo_targets())
        except Exception:
            self._respond(200, {"status": "demo", "data": {"activeTargets": []}})

    # ===== 部署 =====
    def _deployment_summary(self, params):
        try:
            from aiops.tools.k8s_tools import _demo_pods, _demo_deployments
            pods = _demo_pods()
            deps = _demo_deployments()
            running = sum(1 for p in pods if p["status"] == "Running")
            pending = sum(1 for p in pods if p["status"] in ("Pending", "ContainerCreating"))
            failed = sum(1 for p in pods if p["status"] in ("CrashLoopBackOff", "Error", "Failed"))
            self._respond(200, {"status": "success", "data": {
                "total_pods": len(pods), "running_pods": running, "pending_pods": pending, "failed_pods": failed,
                "total_deployments": len(deps), "healthy_deployments": sum(1 for d in deps if d["status"] == "healthy"),
                "total_nodes": 4, "ready_nodes": 4, "total_namespaces": 7,
            }})
        except Exception:
            self._respond(200, {"status": "demo", "data": {"total_pods": 0}})

    def _deployment_nodes(self, params):
        try:
            from aiops.tools.k8s_tools import _demo_nodes
            self._respond(200, {"status": "success", "data": _demo_nodes()})
        except Exception:
            self._respond(200, {"status": "demo", "data": []})

    def _deployment_pods(self, params):
        try:
            from aiops.tools.k8s_tools import _demo_pods
            self._respond(200, {"status": "success", "data": _demo_pods()})
        except Exception:
            self._respond(200, {"status": "demo", "data": []})

    def _deployment_deployments(self, params):
        try:
            from aiops.tools.k8s_tools import _demo_deployments
            self._respond(200, {"status": "success", "data": _demo_deployments()})
        except Exception:
            self._respond(200, {"status": "demo", "data": []})

    def _deployment_events(self, params):
        try:
            from aiops.tools.k8s_tools import _demo_events
            self._respond(200, {"status": "success", "data": _demo_events()})
        except Exception:
            self._respond(200, {"status": "demo", "data": []})

    def _deployment_namespaces(self, params):
        try:
            from aiops.tools.k8s_tools import _demo_namespaces
            self._respond(200, {"status": "success", "data": _demo_namespaces()})
        except Exception:
            self._respond(200, {"status": "demo", "data": []})

    def _deployment_services(self, params):
        try:
            from aiops.tools.k8s_tools import _demo_services
            self._respond(200, {"status": "success", "data": _demo_services()})
        except Exception:
            self._respond(200, {"status": "demo", "data": []})

    def _deployment_scale(self, data):
        deployment = data.get("deployment")
        replicas = data.get("replicas")
        if not deployment or replicas is None:
            self._respond(400, {"error": "Missing deployment or replicas"})
            return
        self._respond(200, {"status": "success", "message": f"Scaled {deployment} to {replicas} replicas"})

    # ===== 原有方法 =====
    def _list_tools(self):
        if self.engine:
            tools = self.engine.tool_registry.list_tools()
            self._respond(200, {"tools": tools})
        else:
            self._respond(200, {"tools": []})

    def _list_agents(self):
        agents = [
            {"name": "linux", "description": "System operations"},
            {"name": "k8s", "description": "Kubernetes operations"},
            {"name": "docker", "description": "Docker container operations"},
            {"name": "db", "description": "Database operations"},
            {"name": "log", "description": "Log analysis"},
            {"name": "monitor", "description": "Monitoring analysis"},
            {"name": "security", "description": "Security operations"},
            {"name": "sre", "description": "SRE operations"},
            {"name": "cost", "description": "Cost optimization"},
            {"name": "incident", "description": "Incident management"},
            {"name": "devops", "description": "DevOps operations"},
            {"name": "cmdb", "description": "Configuration management"},
            {"name": "cloud", "description": "Multi-cloud management"},
            {"name": "windows", "description": "Windows Server operations"},
            {"name": "network", "description": "Network operations"},
            {"name": "middleware", "description": "Middleware management"},
            {"name": "servicemesh", "description": "Service mesh operations"},
            {"name": "virtual", "description": "Virtualization management"},
            {"name": "planner", "description": "Task planning"},
        ]
        self._respond(200, {"agents": agents})

    def _diagnose(self, data):
        host = data.get("host")
        symptom = data.get("symptom", "")
        if not host:
            self._respond(400, {"error": "Missing host"})
            return
        self._respond(200, {"status": "completed", "host": host, "symptom": symptom, "root_cause": "Analysis completed", "confidence": 0.85})

    def _execute_tool(self, data):
        tool_name = data.get("tool")
        params = data.get("params", {})
        if not tool_name:
            self._respond(400, {"error": "Missing tool name"})
            return
        if self.engine:
            result = self.engine.tool_registry.execute(tool_name, params)
            self._respond(200, {"result": result})
        else:
            self._respond(500, {"error": "Engine not initialized"})

    def _run_workflow(self, data):
        workflow_name = data.get("workflow")
        if not workflow_name:
            self._respond(400, {"error": "Missing workflow name"})
            return
        self._respond(200, {"status": "started", "workflow": workflow_name})

    def _create_approval(self, data):
        title = data.get("title")
        command = data.get("command")
        if not title or not command:
            self._respond(400, {"error": "Missing title or command"})
            return
        from aiops.approval.manager import get_approval_manager
        from aiops.approval.base import ApprovalType
        manager = get_approval_manager()
        request = manager.create_request(approval_type=ApprovalType.COMMAND, title=title, description=data.get("description", ""), command=command, risk_level=data.get("risk_level", "medium"))
        self._respond(200, {"request_id": request.id, "status": "pending"})

    def _handle_discovery(self):
        """环境发现 - 自动探测当前系统环境"""
        try:
            from aiops.tools.discovery_tools import full_discovery
            result = full_discovery()
            self._respond(200, result)
        except Exception as e:
            self._respond(500, {"error": str(e)})

    def _handle_environments(self, path: str, params: dict):
        """环境管理 API"""
        try:
            from aiops.environments import EnvironmentManager
        except ImportError:
            self._respond(500, {"error": "environments module not available"})
            return

        mgr = EnvironmentManager()

        # GET /api/v1/environments → 列表
        if path == "/api/v1/environments":
            self._respond(200, mgr.list_environments())

        # GET /api/v1/environments/summary → 拓扑概览
        elif path == "/api/v1/environments/summary":
            self._respond(200, mgr.get_topology_summary())

        # GET /api/v1/environments/topology → 网络拓扑
        elif path == "/api/v1/environments/topology":
            self._respond(200, mgr.get_network_topology())

        # GET /api/v1/environments/:id → 单环境详情
        elif path.startswith("/api/v1/environments/") and path.count("/") == 4:
            env_id = path.split("/")[-1]
            detail = mgr.get_environment(env_id)
            if detail:
                self._respond(200, detail)
            else:
                self._respond(404, {"error": f"Environment {env_id} not found"})
        else:
            self._respond(404, {"error": "API not found"})

    # ===== 新增企业级 API 端点 =====

    def _slo_data(self, params):
        """SLO 数据"""
        data = [
            {"name": "API 可用性", "target": 99.9, "current": 99.95, "status": "healthy", "error_budget_remaining": 95, "description": "HTTP 2xx / 总请求数", "slo_type": "availability"},
            {"name": "API 延迟 P99", "target": 200, "current": 156, "status": "healthy", "error_budget_remaining": 78, "description": "P99 响应时间 < 200ms", "slo_type": "latency"},
            {"name": "错误率", "target": 0.1, "current": 0.05, "status": "healthy", "error_budget_remaining": 90, "description": "5xx / 总请求数 < 0.1%", "slo_type": "error_rate"},
            {"name": "数据新鲜度", "target": 60, "current": 45, "status": "healthy", "error_budget_remaining": 85, "description": "指标采集延迟 < 60s", "slo_type": "freshness"},
            {"name": "批处理完成率", "target": 99, "current": 97.5, "status": "degraded", "error_budget_remaining": 30, "description": "定时任务成功完成率", "slo_type": "availability"},
        ]
        self._respond(200, {"status": "success", "data": data})

    def _event_logs(self, params):
        """事件日志"""
        data = [
            {"time": "14:32:15", "level": "error", "source": "k8s", "title": "Pod CrashLoopBackOff", "description": "user-service 容器反复崩溃，已重启8次"},
            {"time": "14:28:03", "level": "warning", "source": "monitoring", "title": "CPU 告警触发", "description": "prod-web-01 CPU使用率达到 87%"},
            {"time": "14:15:42", "level": "info", "source": "deploy", "title": "滚动更新完成", "description": "nginx-frontend 3/3 副本更新成功"},
            {"time": "14:02:18", "level": "warning", "source": "db", "title": "慢查询告警", "description": "postgres-primary 检测到3条慢查询(>2s)"},
            {"time": "13:45:00", "level": "info", "source": "sre", "title": "SLO 检查通过", "description": "API可用性 99.95%，目标 99.9%"},
        ]
        self._respond(200, {"status": "success", "data": data})

    def _workflows_data(self, params):
        """工作流数据"""
        data = [
            {"name": "P0 故障自动响应", "status": "active", "triggers": "告警触发", "steps": 8, "last_run": "2小时前", "success_rate": 98, "description": "检测→定位→隔离→通知→修复→验证→复盘"},
            {"name": "每日巡检", "status": "active", "triggers": "定时 09:00", "steps": 12, "last_run": "今天 09:00", "success_rate": 100, "description": "健康检查→安全扫描→性能基线→报告生成"},
            {"name": "自动扩缩容", "status": "active", "triggers": "CPU>80%", "steps": 5, "last_run": "30分钟前", "success_rate": 95, "description": "触发→评估→扩容→验证→通知"},
            {"name": "数据库备份验证", "status": "active", "triggers": "定时 02:00", "steps": 6, "last_run": "今天 02:00", "success_rate": 100, "description": "备份→校验→恢复测试→清理→报告"},
            {"name": "SSL证书续签", "status": "active", "triggers": "到期前30天", "steps": 4, "last_run": "3天前", "success_rate": 100, "description": "检测→申请→部署→验证"},
        ]
        self._respond(200, {"status": "success", "data": data})

    def _network_connections(self, params):
        """Agent 网络拓扑连接"""
        data = [
            {"source": "planner", "target": "linux", "label": "调度"},
            {"source": "planner", "target": "k8s", "label": "调度"},
            {"source": "planner", "target": "docker", "label": "调度"},
            {"source": "planner", "target": "db", "label": "调度"},
            {"source": "planner", "target": "monitor", "label": "调度"},
            {"source": "planner", "target": "security", "label": "调度"},
            {"source": "cloud", "target": "monitor", "label": "指标"},
            {"source": "middleware", "target": "log", "label": "日志"},
            {"source": "linux", "target": "monitor", "label": "数据"},
            {"source": "log", "target": "incident", "label": "告警"},
            {"source": "monitor", "target": "sre", "label": "SLO"},
            {"source": "incident", "target": "devops", "label": "修复"},
        ]
        self._respond(200, {"status": "success", "data": data})

    def _multicloud_data(self, params):
        """多云数据"""
        data = [
            {"provider": "阿里云", "status": "healthy", "instances": 35, "regions": ["cn-hangzhou", "cn-shanghai"], "monthly_cost": 246000, "services": ["ECS", "RDS", "Redis", "SLB", "OSS", "CDN"]},
            {"provider": "AWS", "status": "healthy", "instances": 18, "regions": ["us-east-1", "ap-southeast-1"], "monthly_cost": 135000, "services": ["EC2", "RDS", "S3", "CloudFront", "Lambda"]},
            {"provider": "华为云", "status": "healthy", "instances": 12, "regions": ["cn-north-4"], "monthly_cost": 68000, "services": ["ECS", "RDS", "OBS", "CCE"]},
            {"provider": "腾讯云", "status": "degraded", "instances": 8, "regions": ["ap-guangzhou"], "monthly_cost": 45000, "services": ["CVM", "COS", "CLB"]},
        ]
        self._respond(200, {"status": "success", "data": data})

    def _audit_logs(self, params):
        """审计日志"""
        data = [
            {"id": "LOG-001", "time": "14:32:15", "user": "admin", "action": "部署", "resource": "nginx-frontend", "detail": "滚动更新 v2.3.1 → v2.3.2", "ip": "10.0.1.100", "result": "success"},
            {"id": "LOG-002", "time": "14:28:03", "user": "sre-bot", "action": "告警处理", "resource": "HighCPUUsage", "detail": "自动扩容 worker-03", "ip": "10.0.1.50", "result": "success"},
            {"id": "LOG-003", "time": "14:15:42", "user": "devops", "action": "配置变更", "resource": "nginx.conf", "detail": "更新 upstream 配置", "ip": "10.0.1.200", "result": "success"},
        ]
        self._respond(200, {"status": "success", "data": data})

    def _cost_summary(self, params):
        """成本分析摘要"""
        data = [
            {"provider": "阿里云", "service": "ECS 计算", "monthly": 125000, "trend": "+5%", "optimization": "可优化: 3台低利用率实例", "region": "cn-hangzhou"},
            {"provider": "阿里云", "service": "RDS 数据库", "monthly": 89000, "trend": "+2%", "optimization": "存储可清理 200GB 历史数据", "region": "cn-hangzhou"},
            {"provider": "阿里云", "service": "SLB 负载均衡", "monthly": 32000, "trend": "0%", "optimization": "无优化建议", "region": "cn-hangzhou"},
            {"provider": "AWS", "service": "EC2 计算", "monthly": 98000, "trend": "-3%", "optimization": "预留实例可节省 35%", "region": "us-east-1"},
            {"provider": "AWS", "service": "S3 存储", "monthly": 15000, "trend": "+12%", "optimization": "生命周期策略迁移冷数据", "region": "us-east-1"},
            {"provider": "AWS", "service": "CloudFront", "monthly": 22000, "trend": "+8%", "optimization": "缓存命中率可提升", "region": "global"},
            {"provider": "华为云", "service": "ECS", "monthly": 68000, "trend": "+1%", "optimization": "弹性伸缩可减少闲时资源", "region": "cn-north-4"},
            {"provider": "腾讯云", "service": "CVM", "monthly": 45000, "trend": "-2%", "optimization": "无优化建议", "region": "ap-guangzhou"},
        ]
        self._respond(200, {"status": "success", "data": data})

    def _security_summary(self, params):
        """安全态势摘要"""
        data = [
            {"category": "漏洞扫描", "total": 23, "critical": 2, "high": 5, "medium": 11, "low": 5, "items": [
                {"name": "CVE-2024-3094", "severity": "critical", "status": "open", "description": "XZ Utils 后门漏洞"},
                {"name": "CVE-2024-21762", "severity": "critical", "status": "open", "description": "FortiOS 远程代码执行"},
                {"name": "OpenSSH 弱密码", "severity": "high", "status": "mitigated", "description": "部分主机仍允许密码登录"},
            ]},
            {"category": "合规检查", "total": 45, "critical": 0, "high": 3, "medium": 12, "low": 30, "items": [
                {"name": "密码策略", "severity": "high", "status": "open", "description": "3台服务器密码不符合等保要求"},
                {"name": "审计日志", "severity": "high", "status": "open", "description": "审计日志保留不足180天"},
                {"name": "文件权限", "severity": "medium", "status": "open", "description": "敏感文件权限过宽"},
            ]},
            {"category": "配置审计", "total": 67, "critical": 0, "high": 2, "medium": 8, "low": 57, "items": [
                {"name": "SSH 配置", "severity": "high", "status": "open", "description": "2台服务器允许 root SSH 登录"},
                {"name": "防火墙规则", "severity": "medium", "status": "open", "description": "5条冗余规则"},
            ]},
        ]
        self._respond(200, {"status": "success", "data": data})

    def log_message(self, format, *args):
        logger.debug(f"{self.address_string()} - {format % args}")


def create_app(host="0.0.0.0", port=8000, engine=None):
    def handler(*args, **kwargs):
        return AIOpsHandler(*args, engine=engine, **kwargs)
    server = HTTPServer((host, port), handler)
    logger.info(f"AIOps API server starting on {host}:{port}")
    return server


def run_server(host="0.0.0.0", port=8000, engine=None):
    server = create_app(host, port, engine)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        logger.info("API server stopped")
