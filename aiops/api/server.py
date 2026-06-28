"""REST API Server"""
import json
import logging
from typing import Dict, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


class AIOpsHandler(BaseHTTPRequestHandler):
    """AIOps HTTP Handler"""

    def __init__(self, *args, engine=None, **kwargs):
        self.engine = engine
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """处理 GET 请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/api/v1/health":
            self._respond(200, {"status": "healthy"})
        elif path == "/api/v1/version":
            from aiops import __version__
            self._respond(200, {"version": __version__})
        elif path == "/api/v1/tools":
            self._list_tools()
        elif path == "/api/v1/agents":
            self._list_agents()
        else:
            self._respond(404, {"error": "Not found"})

    def do_POST(self):
        """处理 POST 请求"""
        parsed = urlparse(self.path)
        path = parsed.path

        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''

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
        else:
            self._respond(404, {"error": "Not found"})

    def _respond(self, status: int, data: Dict[str, Any]):
        """发送响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def _list_tools(self):
        """列出工具"""
        if self.engine:
            tools = self.engine.tool_registry.list_tools()
            self._respond(200, {"tools": tools})
        else:
            self._respond(200, {"tools": []})

    def _list_agents(self):
        """列出 Agent"""
        agents = [
            {"name": "linux", "description": "System operations"},
            {"name": "k8s", "description": "Kubernetes operations"},
            {"name": "db", "description": "Database operations"},
            {"name": "log", "description": "Log analysis"},
            {"name": "monitor", "description": "Monitoring analysis"},
            {"name": "security", "description": "Security operations"},
            {"name": "sre", "description": "SRE operations"},
            {"name": "cost", "description": "Cost optimization"},
            {"name": "incident", "description": "Incident management"},
            {"name": "devops", "description": "DevOps operations"},
            {"name": "cmdb", "description": "Configuration management"},
            {"name": "planner", "description": "Task planning"},
        ]
        self._respond(200, {"agents": agents})

    def _diagnose(self, data: Dict[str, Any]):
        """执行诊断"""
        host = data.get("host")
        symptom = data.get("symptom", "")

        if not host:
            self._respond(400, {"error": "Missing host"})
            return

        # 模拟诊断结果
        result = {
            "status": "completed",
            "host": host,
            "symptom": symptom,
            "root_cause": "Analysis completed",
            "confidence": 0.85,
        }
        self._respond(200, result)

    def _execute_tool(self, data: Dict[str, Any]):
        """执行工具"""
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

    def _run_workflow(self, data: Dict[str, Any]):
        """运行工作流"""
        workflow_name = data.get("workflow")
        variables = data.get("variables", {})

        if not workflow_name:
            self._respond(400, {"error": "Missing workflow name"})
            return

        self._respond(200, {"status": "started", "workflow": workflow_name})

    def _create_approval(self, data: Dict[str, Any]):
        """创建审批"""
        title = data.get("title")
        command = data.get("command")

        if not title or not command:
            self._respond(400, {"error": "Missing title or command"})
            return

        from aiops.approval.manager import get_approval_manager
        from aiops.approval.base import ApprovalType

        manager = get_approval_manager()
        request = manager.create_request(
            approval_type=ApprovalType.COMMAND,
            title=title,
            description=data.get("description", ""),
            command=command,
            risk_level=data.get("risk_level", "medium"),
        )

        self._respond(200, {"request_id": request.id, "status": "pending"})

    def log_message(self, format, *args):
        """自定义日志"""
        logger.debug(f"{self.address_string()} - {format % args}")


def create_app(host: str = "0.0.0.0", port: int = 8000, engine=None):
    """
    创建 API 应用

    Args:
        host: 监听地址
        port: 监听端口
        engine: AIOps 引擎实例
    """
    def handler(*args, **kwargs):
        return AIOpsHandler(*args, engine=engine, **kwargs)

    server = HTTPServer((host, port), handler)
    logger.info(f"AIOps API server starting on {host}:{port}")

    return server


def run_server(host: str = "0.0.0.0", port: int = 8000, engine=None):
    """运行 API 服务器"""
    server = create_app(host, port, engine)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        logger.info("API server stopped")
