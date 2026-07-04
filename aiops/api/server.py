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
        else:
            self._respond(404, {"error": "API not found"})

    def _respond(self, status: int, data: Dict[str, Any]):
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
