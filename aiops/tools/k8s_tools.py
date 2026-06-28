"""Kubernetes 工具"""
from .base import BaseTool, ToolResult
import subprocess


class KubectlTool(BaseTool):
    name = "kubectl"
    description = "执行 kubectl 命令"
    parameters = {"type": "object", "properties": {
        "command": {"type": "string", "description": "kubectl 子命令"},
        "context": {"type": "string"}, "namespace": {"type": "string"},
    }, "required": ["command"]}
    def execute(self, command, context=None, namespace=None, **kw):
        cmd = f"kubectl {command}"
        if context: cmd += f" --context={context}"
        if namespace: cmd += f" -n {namespace}"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            out = r.stdout.strip()
            if r.stderr.strip(): out += f"
[stderr] {r.stderr.strip()}"
            return ToolResult(success=(r.returncode==0), output=out[:5000],
                            error=r.stderr.strip() if r.returncode!=0 else "")
        except Exception as e: return ToolResult(success=False, error=str(e))


class K8sGetNodesTool(BaseTool):
    name = "k8s_get_nodes"
    description = "获取 K8s Node 列表"
    parameters = {"type": "object", "properties": {"context": {"type": "string"}}}
    def execute(self, context=None, **kw):
        cmd = "kubectl get nodes -o wide"
        if context: cmd += f" --context={context}"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:3000])
        except Exception as e: return ToolResult(success=False, error=str(e))


class K8sGetPodsTool(BaseTool):
    name = "k8s_get_pods"
    description = "获取 Pod 列表"
    parameters = {"type": "object", "properties": {
        "namespace": {"type": "string", "default": "default"}, "context": {"type": "string"},
    }}
    def execute(self, namespace="default", context=None, **kw):
        cmd = f"kubectl get pods -n {namespace} -o wide"
        if context: cmd += f" --context={context}"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:3000])
        except Exception as e: return ToolResult(success=False, error=str(e))


class K8sGetEventsTool(BaseTool):
    name = "k8s_get_events"
    description = "获取 K8s 事件"
    parameters = {"type": "object", "properties": {
        "namespace": {"type": "string", "default": "default"}, "context": {"type": "string"},
    }}
    def execute(self, namespace="default", context=None, **kw):
        cmd = f"kubectl get events -n {namespace} --sort-by=.lastTimestamp"
        if context: cmd += f" --context={context}"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            lines = r.stdout.strip().split("
")
            return ToolResult(success=(r.returncode==0), output="
".join(lines[-20:])[:3000])
        except Exception as e: return ToolResult(success=False, error=str(e))


class K8sLogsTool(BaseTool):
    name = "k8s_logs"
    description = "获取 Pod 日志"
    parameters = {"type": "object", "properties": {
        "pod": {"type": "string"}, "namespace": {"type": "string", "default": "default"},
        "tail": {"type": "integer", "default": 100}, "context": {"type": "string"},
    }, "required": ["pod"]}
    def execute(self, pod, namespace="default", tail=100, context=None, **kw):
        cmd = f"kubectl logs {pod} -n {namespace} --tail={tail}"
        if context: cmd += f" --context={context}"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:5000])
        except Exception as e: return ToolResult(success=False, error=str(e))


class K8sDescribePodTool(BaseTool):
    name = "k8s_describe_pod"
    description = "描述 Pod 详情"
    parameters = {"type": "object", "properties": {
        "pod": {"type": "string"}, "namespace": {"type": "string", "default": "default"},
    }, "required": ["pod"]}
    def execute(self, pod, namespace="default", **kw):
        cmd = f"kubectl describe pod {pod} -n {namespace}"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(success=(r.returncode==0), output=r.stdout.strip()[:5000])
        except Exception as e: return ToolResult(success=False, error=str(e))


class K8sRestartTool(BaseTool):
    name = "k8s_restart"
    description = "滚动重启 Deployment"
    parameters = {"type": "object", "properties": {
        "deployment": {"type": "string"}, "namespace": {"type": "string", "default": "default"},
    }, "required": ["deployment"]}
    def execute(self, deployment, namespace="default", **kw):
        cmd = f"kubectl rollout restart deployment/{deployment} -n {namespace}"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return ToolResult(success=(r.returncode==0), output=f"已重启 {deployment}" if r.returncode==0 else r.stderr)
        except Exception as e: return ToolResult(success=False, error=str(e))


class K8sRollbackTool(BaseTool):
    name = "k8s_rollback"
    description = "回滚 Deployment"
    parameters = {"type": "object", "properties": {
        "deployment": {"type": "string"}, "namespace": {"type": "string", "default": "default"},
    }, "required": ["deployment"]}
    def execute(self, deployment, namespace="default", **kw):
        cmd = f"kubectl rollout undo deployment/{deployment} -n {namespace}"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return ToolResult(success=(r.returncode==0), output=f"已回滚 {deployment}" if r.returncode==0 else r.stderr)
        except Exception as e: return ToolResult(success=False, error=str(e))
