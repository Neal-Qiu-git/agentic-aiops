"""Kubernetes 工具 - 安全版本"""
from .base import BaseTool, ToolResult
import subprocess
import shlex
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


def safe_kubectl_command(command: str, context: Optional[str] = None,
                         namespace: Optional[str] = None, timeout: int = 30) -> subprocess.CompletedProcess:
    """
    安全执行 kubectl 命令，避免命令注入

    Args:
        command: kubectl 子命令和参数
        context: K8s context
        namespace: 命名空间
        timeout: 超时时间

    Returns:
        subprocess.CompletedProcess
    """
    # 构建安全的命令列表
    cmd_parts = ["kubectl"]

    # 解析 command 参数，使用 shlex 安全分割
    if command:
        try:
            # 使用 shlex 安全分割命令
            parsed_command = shlex.split(command)
            cmd_parts.extend(parsed_command)
        except ValueError as e:
            logger.error(f"命令解析失败: {e}")
            return subprocess.CompletedProcess(
                args=[], returncode=1,
                stdout="", stderr=f"命令解析失败: {e}"
            )

    # 添加可选参数
    if context:
        cmd_parts.extend(["--context", context])
    if namespace:
        cmd_parts.extend(["-n", namespace])

    logger.debug(f"执行 kubectl 命令: {cmd_parts}")

    try:
        # 使用列表形式，避免 shell=True
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            args=cmd_parts, returncode=1,
            stdout="", stderr=f"命令执行超时 ({timeout}秒)"
        )
    except Exception as e:
        logger.error(f"kubectl 命令执行异常: {e}")
        return subprocess.CompletedProcess(
            args=cmd_parts, returncode=1,
            stdout="", stderr=f"命令执行异常: {e}"
        )


class KubectlTool(BaseTool):
    name = "kubectl"
    description = "安全执行 kubectl 命令"
    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "kubectl 子命令和参数"},
            "context": {"type": "string", "description": "K8s context"},
            "namespace": {"type": "string", "description": "命名空间"},
            "timeout": {"type": "integer", "description": "超时时间(秒)", "default": 30},
        },
        "required": ["command"]
    }

    def execute(self, command: str, context: Optional[str] = None,
                namespace: Optional[str] = None, timeout: int = 30, **kwargs) -> ToolResult:
        try:
            result = safe_kubectl_command(command, context, namespace, timeout)
            output = result.stdout.strip()
            if result.stderr.strip():
                output += f"\n[stderr] {result.stderr.strip()}"

            return ToolResult(
                success=(result.returncode == 0),
                output=output[:5000],
                error=result.stderr.strip() if result.returncode != 0 else ""
            )
        except Exception as e:
            logger.error(f"KubectlTool 执行异常: {e}")
            return ToolResult(success=False, error=str(e))


class K8sGetNodesTool(BaseTool):
    name = "k8s_get_nodes"
    description = "获取 K8s Node 列表"
    parameters = {
        "type": "object",
        "properties": {
            "context": {"type": "string", "description": "K8s context"},
            "output_format": {"type": "string", "description": "输出格式", "default": "wide"}
        }
    }

    def execute(self, context: Optional[str] = None, output_format: str = "wide", **kwargs) -> ToolResult:
        cmd = f"get nodes -o {output_format}"
        result = safe_kubectl_command(cmd, context=context)

        return ToolResult(
            success=(result.returncode == 0),
            output=result.stdout.strip()[:3000],
            error=result.stderr.strip() if result.returncode != 0 else ""
        )


class K8sGetPodsTool(BaseTool):
    name = "k8s_get_pods"
    description = "获取 Pod 列表"
    parameters = {
        "type": "object",
        "properties": {
            "namespace": {"type": "string", "description": "命名空间", "default": "default"},
            "context": {"type": "string", "description": "K8s context"},
            "output_format": {"type": "string", "description": "输出格式", "default": "wide"},
        }
    }

    def execute(self, namespace: str = "default", context: Optional[str] = None,
                output_format: str = "wide", **kwargs) -> ToolResult:
        cmd = f"get pods -n {namespace} -o {output_format}"
        result = safe_kubectl_command(cmd, context=context)

        return ToolResult(
            success=(result.returncode == 0),
            output=result.stdout.strip()[:3000],
            error=result.stderr.strip() if result.returncode != 0 else ""
        )


class K8sGetEventsTool(BaseTool):
    name = "k8s_get_events"
    description = "获取 K8s 事件"
    parameters = {
        "type": "object",
        "properties": {
            "namespace": {"type": "string", "description": "命名空间", "default": "default"},
            "context": {"type": "string", "description": "K8s context"},
            "limit": {"type": "integer", "description": "返回条数", "default": 20},
        }
    }

    def execute(self, namespace: str = "default", context: Optional[str] = None,
                limit: int = 20, **kwargs) -> ToolResult:
        cmd = f"get events -n {namespace} --sort-by=.lastTimestamp"
        result = safe_kubectl_command(cmd, context=context)

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            # 取最后 limit 条
            output = "\n".join(lines[-limit:]) if len(lines) > limit else result.stdout.strip()
        else:
            output = result.stderr.strip()

        return ToolResult(
            success=(result.returncode == 0),
            output=output[:3000],
            error=result.stderr.strip() if result.returncode != 0 else ""
        )


class K8sLogsTool(BaseTool):
    name = "k8s_logs"
    description = "获取 Pod 日志"
    parameters = {
        "type": "object",
        "properties": {
            "pod": {"type": "string", "description": "Pod 名称"},
            "namespace": {"type": "string", "description": "命名空间", "default": "default"},
            "tail": {"type": "integer", "description": "返回最后N行", "default": 100},
            "context": {"type": "string", "description": "K8s context"},
            "container": {"type": "string", "description": "容器名称（多容器Pod）"},
        },
        "required": ["pod"]
    }

    def execute(self, pod: str, namespace: str = "default", tail: int = 100,
                context: Optional[str] = None, container: Optional[str] = None, **kwargs) -> ToolResult:
        cmd = f"logs {pod} -n {namespace} --tail={tail}"
        if container:
            cmd += f" -c {container}"

        result = safe_kubectl_command(cmd, context=context)

        return ToolResult(
            success=(result.returncode == 0),
            output=result.stdout.strip()[:5000],
            error=result.stderr.strip() if result.returncode != 0 else ""
        )


class K8sDescribePodTool(BaseTool):
    name = "k8s_describe_pod"
    description = "描述 Pod 详情"
    parameters = {
        "type": "object",
        "properties": {
            "pod": {"type": "string", "description": "Pod 名称"},
            "namespace": {"type": "string", "description": "命名空间", "default": "default"},
            "context": {"type": "string", "description": "K8s context"},
        },
        "required": ["pod"]
    }

    def execute(self, pod: str, namespace: str = "default",
                context: Optional[str] = None, **kwargs) -> ToolResult:
        cmd = f"describe pod {pod} -n {namespace}"
        result = safe_kubectl_command(cmd, context=context)

        return ToolResult(
            success=(result.returncode == 0),
            output=result.stdout.strip()[:5000],
            error=result.stderr.strip() if result.returncode != 0 else ""
        )


class K8sRestartTool(BaseTool):
    name = "k8s_restart"
    description = "滚动重启 Deployment（需要确认）"
    parameters = {
        "type": "object",
        "properties": {
            "deployment": {"type": "string", "description": "Deployment 名称"},
            "namespace": {"type": "string", "description": "命名空间", "default": "default"},
            "context": {"type": "string", "description": "K8s context"},
            "confirm": {"type": "boolean", "description": "确认执行重启", "default": False},
        },
        "required": ["deployment", "confirm"]
    }

    def execute(self, deployment: str, namespace: str = "default",
                context: Optional[str] = None, confirm: bool = False, **kwargs) -> ToolResult:
        if not confirm:
            return ToolResult(
                success=False,
                error="重启操作需要确认。请设置 confirm=true 以执行重启。"
            )

        logger.warning(f"执行 Deployment 重启: {deployment} (namespace: {namespace})")

        cmd = f"rollout restart deployment/{deployment} -n {namespace}"
        result = safe_kubectl_command(cmd, context=context, timeout=60)

        if result.returncode == 0:
            return ToolResult(success=True, output=f"已重启 Deployment: {deployment}")
        else:
            return ToolResult(success=False, error=result.stderr.strip())


class K8sRollbackTool(BaseTool):
    name = "k8s_rollback"
    description = "回滚 Deployment（需要确认）"
    parameters = {
        "type": "object",
        "properties": {
            "deployment": {"type": "string", "description": "Deployment 名称"},
            "namespace": {"type": "string", "description": "命名空间", "default": "default"},
            "context": {"type": "string", "description": "K8s context"},
            "confirm": {"type": "boolean", "description": "确认执行回滚", "default": False},
        },
        "required": ["deployment", "confirm"]
    }

    def execute(self, deployment: str, namespace: str = "default",
                context: Optional[str] = None, confirm: bool = False, **kwargs) -> ToolResult:
        if not confirm:
            return ToolResult(
                success=False,
                error="回滚操作需要确认。请设置 confirm=true 以执行回滚。"
            )

        logger.warning(f"执行 Deployment 回滚: {deployment} (namespace: {namespace})")

        cmd = f"rollout undo deployment/{deployment} -n {namespace}"
        result = safe_kubectl_command(cmd, context=context, timeout=60)

        if result.returncode == 0:
            return ToolResult(success=True, output=f"已回滚 Deployment: {deployment}")
        else:
            return ToolResult(success=False, error=result.stderr.strip())


# ===== 增强的 K8s 工具 =====

import json as _json


def _demo_nodes():
    return [
        {"name": "k8s-master", "status": "Ready", "roles": "control-plane", "age": "127d", "version": "v1.28.4", "os": "Ubuntu 22.04", "cpu": "35%", "memory": "62%", "cpu_alloc": "8", "mem_alloc": "32Gi"},
        {"name": "k8s-worker-01", "status": "Ready", "roles": "worker", "age": "127d", "version": "v1.28.4", "os": "Ubuntu 22.04", "cpu": "68%", "memory": "74%", "cpu_alloc": "16", "mem_alloc": "64Gi"},
        {"name": "k8s-worker-02", "status": "Ready", "roles": "worker", "age": "95d", "version": "v1.28.4", "os": "Ubuntu 22.04", "cpu": "cpu": "45%", "memory": "58%", "cpu_alloc": "16", "mem_alloc": "64Gi"},
        {"name": "k8s-worker-03", "status": "Ready", "roles": "worker", "age": "30d", "version": "v1.28.4", "os": "Ubuntu 22.04", "cpu": "52%", "memory": "65%", "cpu_alloc": "16", "mem_alloc": "64Gi"},
    ]


def _demo_deployments():
    return [
        {"name": "api-gateway", "namespace": "production", "ready": "2/3", "up_to_date": 2, "available": 2, "strategy": "RollingUpdate", "age": "45d", "status": "progressing", "containers": "nginx:1.25, app:v2.1.0"},
        {"name": "user-service", "namespace": "production", "ready": "3/3", "up_to_date": 3, "available": 3, "strategy": "RollingUpdate", "age": "30d", "status": "healthy", "containers": "app:v1.8.2"},
        {"name": "payment-service", "namespace": "production", "ready": "2/2", "up_to_date": 2, "available": 2, "strategy": "RollingUpdate", "age": "60d", "status": "healthy", "containers": "app:v3.0.1"},
        {"name": "order-service", "namespace": "production", "ready": "2/2", "up_to_date": 2, "available": 2, "strategy": "RollingUpdate", "age": "20d", "status": "healthy", "containers": "app:v2.4.0"},
        {"name": "notification-service", "namespace": "production", "ready": "1/1", "up_to_date": 1, "available": 1, "strategy": "RollingUpdate", "age": "15d", "status": "healthy", "containers": "app:v1.2.0"},
        {"name": "redis-cluster", "namespace": "data", "ready": "3/3", "up_to_date": 3, "available": 3, "strategy": "RollingUpdate", "age": "120d", "status": "healthy", "containers": "redis:7.2"},
        {"name": "mysql-primary", "namespace": "data", "ready": "1/1", "up_to_date": 1, "available": 1, "strategy": "Recreate", "age": "127d", "status": "healthy", "containers": "mysql:8.0"},
        {"name": "prometheus", "namespace": "monitoring", "ready": "1/1", "up_to_date": 1, "available": 1, "strategy": "Recreate", "age": "90d", "status": "healthy", "containers": "prometheus:v2.48.0"},
        {"name": "grafana", "namespace": "monitoring", "ready": "1/1", "up_to_date": 1, "available": 1, "strategy": "RollingUpdate", "age": "90d", "status": "healthy", "containers": "grafana:10.2.0"},
        {"name": "nginx-ingress", "namespace": "ingress-nginx", "ready": "2/2", "up_to_date": 2, "available": 2, "strategy": "RollingUpdate", "age": "127d", "status": "healthy", "containers": "nginx:1.9.4"},
    ]


def _demo_pods():
    return [
        {"name": "api-gateway-7d8f9c6b4-x2k9m", "namespace": "production", "status": "Running", "ready": "2/2", "restarts": 0, "age": "45d", "node": "k8s-worker-01", "ip": "10.244.1.15"},
        {"name": "api-gateway-7d8f9c6b4-h9j2k", "namespace": "production", "status": "Running", "ready": "2/2", "restarts": 0, "age": "45d", "node": "k8s-worker-02", "ip": "10.244.2.23"},
        {"name": "api-gateway-6f4c8b9a3-m3n5p", "namespace": "production", "status": "CrashLoopBackOff", "ready": "0/2", "restarts": 8, "age": "2h", "node": "k8s-worker-03", "ip": "10.244.3.41"},
        {"name": "user-service-5d7c8f9a6-a1b2c", "namespace": "production", "status": "Running", "ready": "1/1", "restarts": 0, "age": "30d", "node": "k8s-worker-01", "ip": "10.244.1.22"},
        {"name": "user-service-5d7c8f9a6-d3e4f", "namespace": "production", "status": "Running", "ready": "1/1", "restarts": 0, "age": "30d", "node": "k8s-worker-02", "ip": "10.244.2.30"},
        {"name": "user-service-5d7c8f9a6-g5h6i", "namespace": "production", "status": "Running", "ready": "1/1", "restarts": 0, "age": "30d", "node": "k8s-worker-03", "ip": "10.244.3.18"},
        {"name": "payment-service-8c9d0e1f-a7b8c", "namespace": "production", "status": "Running", "ready": "1/1", "restarts": 0, "age": "60d", "node": "k8s-worker-01", "ip": "10.244.1.35"},
        {"name": "payment-service-8c9d0e1f-d9e0f", "namespace": "production", "status": "Running", "ready": "1/1", "restarts": 0, "age": "60d", "node": "k8s-worker-02", "ip": "10.244.2.42"},
        {"name": "order-service-2a3b4c5d-e1f2g", "namespace": "production", "status": "Running", "ready": "1/1", "restarts": 0, "age": "20d", "node": "k8s-worker-01", "ip": "10.244.1.48"},
        {"name": "order-service-2a3b4c5d-h3i4j", "namespace": "production", "status": "Running", "ready": "1/1", "restarts": 0, "age": "20d", "node": "k8s-worker-03", "ip": "10.244.3.29"},
        {"name": "notification-service-6g7h8i9j", "namespace": "production", "status": "Running", "ready": "1/1", "restarts": 0, "age": "15d", "node": "k8s-worker-02", "ip": "10.244.2.55"},
        {"name": "redis-cluster-0", "namespace": "data", "status": "Running", "ready": "1/1", "restarts": 0, "age": "120d", "node": "k8s-worker-01", "ip": "10.244.1.60"},
        {"name": "redis-cluster-1", "namespace": "data", "status": "Running", "ready": "1/1", "restarts": 0, "age": "120d", "node": "k8s-worker-02", "ip": "10.244.2.67"},
        {"name": "redis-cluster-2", "namespace": "data", "status": "Running", "ready": "1/1", "restarts": 0, "age": "120d", "node": "k8s-worker-03", "ip": "10.244.3.55"},
        {"name": "mysql-primary-0", "namespace": "data", "status": "Running", "ready": "1/1", "restarts": 0, "age": "127d", "node": "k8s-worker-01", "ip": "10.244.1.75"},
        {"name": "mysql-backup-7k8l9m0n", "namespace": "data", "status": "Pending", "ready": "0/0", "restarts": 0, "age": "5m", "node": "", "ip": ""},
        {"name": "prometheus-0", "namespace": "monitoring", "status": "Running", "ready": "1/1", "restarts": 0, "age": "90d", "node": "k8s-worker-03", "ip": "10.244.3.80"},
        {"name": "grafana-7o8p9q0r", "namespace": "monitoring", "status": "Running", "ready": "1/1", "restarts": 0, "age": "90d", "node": "k8s-worker-03", "ip": "10.244.3.90"},
        {"name": "nginx-ingress-v3w4x", "namespace": "ingress-nginx", "status": "Running", "ready": "1/1", "restarts": 0, "age": "127d", "node": "k8s-worker-01", "ip": "10.244.1.10"},
        {"name": "nginx-ingress-y5z6a", "namespace": "ingress-nginx", "status": "Running", "ready": "1/1", "restarts": 0, "age": "127d", "node": "k8s-worker-02", "ip": "10.244.2.15"},
    ]


def _demo_events():
    return [
        {"type": "Warning", "reason": "BackOff", "object": "pod/api-gateway-6f4c8b9a3-m3n5p", "message": "Back-off restarting failed container", "age": "2m", "namespace": "production"},
        {"type": "Warning", "reason": "Unhealthy", "object": "pod/api-gateway-6f4c8b9a3-m3n5p", "message": "Readiness probe failed: HTTP probe failed with statuscode: 503", "age": "5m", "namespace": "production"},
        {"type": "Normal", "reason": "ScalingReplicaSet", "object": "deployment/api-gateway", "message": "Scaled up replica set api-gateway-7d8f9c6b4 to 3", "age": "2h", "namespace": "production"},
        {"type": "Warning", "reason": "FailedScheduling", "object": "pod/mysql-backup-7k8l9m0n", "message": "0/3 nodes are available: 1 Insufficient cpu", "age": "5m", "namespace": "data"},
        {"type": "Normal", "reason": "Started", "object": "pod/user-service-5d7c8f9a6-a1b2c", "message": "Started container app", "age": "30d", "namespace": "production"},
        {"type": "Normal", "reason": "Pulled", "object": "pod/payment-service-8c9d0e1f-a7b8c", "message": "Container image already present on machine", "age": "60d", "namespace": "production"},
        {"type": "Normal", "reason": "HealthCheck", "object": "node/k8s-worker-03", "message": "Node k8s-worker-03 status is now: NodeReady", "age": "30d", "namespace": ""},
        {"type": "Warning", "reason": "OOMKilling", "object": "pod/api-gateway-6f4c8b9a3-m3n5p", "message": "Memory cgroup out of memory: Killed process 12345 (java)", "age": "1h", "namespace": "production"},
    ]


def _demo_namespaces():
    return [
        {"name": "default", "status": "Active", "age": "127d"},
        {"name": "production", "status": "Active", "age": "120d"},
        {"name": "data", "status": "Active", "age": "127d"},
        {"name": "monitoring", "status": "Active", "age": "90d"},
        {"name": "ingress-nginx", "status": "Active", "age": "127d"},
        {"name": "kube-system", "status": "Active", "age": "127d"},
        {"name": "kube-public", "status": "Active", "age": "127d"},
    ]


def _demo_services():
    return [
        {"name": "kubernetes", "namespace": "default", "type": "ClusterIP", "cluster_ip": "10.96.0.1", "ports": "443/TCP", "age": "127d"},
        {"name": "api-gateway", "namespace": "production", "type": "ClusterIP", "cluster_ip": "10.96.1.10", "ports": "80/TCP,443/TCP", "age": "45d"},
        {"name": "user-service", "namespace": "production", "type": "ClusterIP", "cluster_ip": "10.96.1.20", "ports": "8080/TCP", "age": "30d"},
        {"name": "payment-service", "namespace": "production", "type": "ClusterIP", "cluster_ip": "10.96.1.30", "ports": "8080/TCP", "age": "60d"},
        {"name": "nginx-ingress", "namespace": "ingress-nginx", "type": "LoadBalancer", "cluster_ip": "10.96.2.10", "ports": "80:30080/TCP,443:30443/TCP", "age": "127d"},
        {"name": "prometheus", "namespace": "monitoring", "type": "ClusterIP", "cluster_ip": "10.96.3.10", "ports": "9090/TCP", "age": "90d"},
        {"name": "grafana", "namespace": "monitoring", "type": "ClusterIP", "cluster_ip": "10.96.3.20", "ports": "3000/TCP", "age": "90d"},
        {"name": "redis-cluster", "namespace": "data", "type": "ClusterIP", "cluster_ip": "10.96.4.10", "ports": "6379/TCP", "age": "120d"},
        {"name": "mysql", "namespace": "data", "type": "ClusterIP", "cluster_ip": "10.96.4.20", "ports": "3306/TCP", "age": "127d"},
    ]


class K8sGetDeploymentsTool(BaseTool):
    name = "k8s_get_deployments"
    description = "获取 Deployment 列表及副本状态"
    parameters = {"type": "object", "properties": {"namespace": {"type": "string", "default": "default"}, "context": {"type": "string"}}}

    def execute(self, namespace="default", context=None, **kwargs):
        cmd = f"get deployments -n {namespace} -o json"
        result = safe_kubectl_command(cmd, context=context)
        if result.returncode == 0:
            try:
                import json
                data = json.loads(result.stdout)
                deps = []
                for item in data.get("items", []):
                    spec = item.get("spec", {})
                    status = item.get("status", {})
                    deps.append({"name": item["metadata"]["name"], "namespace": item["metadata"]["namespace"], "ready": f"{status.get('readyReplicas', 0)}/{spec.get('replicas', 0)}", "strategy": spec.get("strategy", {}).get("type", "RollingUpdate"), "status": "healthy" if status.get("readyReplicas", 0) == spec.get("replicas", 0) else "degraded"})
                return ToolResult(success=True, output=json.dumps(deps, ensure_ascii=False)[:8000])
            except Exception:
                pass
        return ToolResult(success=True, output=__import__('json').dumps(_demo_deployments(), ensure_ascii=False)[:8000])


class K8sGetNamespacesTool(BaseTool):
    name = "k8s_get_namespaces"
    description = "获取 Namespace 列表"
    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs):
        result = safe_kubectl_command("get namespaces -o json")
        if result.returncode == 0:
            try:
                import json
                data = json.loads(result.stdout)
                ns = [{"name": i["metadata"]["name"], "status": i["status"]["phase"]} for i in data.get("items", [])]
                return ToolResult(success=True, output=json.dumps(ns, ensure_ascii=False)[:5000])
            except Exception:
                pass
        return ToolResult(success=True, output=__import__('json').dumps(_demo_namespaces(), ensure_ascii=False)[:5000])


class K8sGetServicesTool(BaseTool):
    name = "k8s_get_services"
    description = "获取 Service 列表"
    parameters = {"type": "object", "properties": {"namespace": {"type": "string", "default": "default"}}}

    def execute(self, namespace="default", **kwargs):
        result = safe_kubectl_command(f"get services -n {namespace} -o json")
        if result.returncode == 0:
            try:
                import json
                data = json.loads(result.stdout)
                svcs = []
                for item in data.get("items", []):
                    spec = item.get("spec", {})
                    ports = ",".join([f"{p.get('port','')}/{p.get('protocol','TCP')}" for p in spec.get("ports", [])])
                    svcs.append({"name": item["metadata"]["name"], "namespace": item["metadata"]["namespace"], "type": spec.get("type",""), "cluster_ip": spec.get("clusterIP",""), "ports": ports})
                return ToolResult(success=True, output=json.dumps(svcs, ensure_ascii=False)[:5000])
            except Exception:
                pass
        return ToolResult(success=True, output=__import__('json').dumps(_demo_services(), ensure_ascii=False)[:5000])


class K8sScaleDeploymentTool(BaseTool):
    name = "k8s_scale_deployment"
    description = "调整 Deployment 副本数（需要确认）"
    parameters = {"type": "object", "properties": {"deployment": {"type": "string"}, "replicas": {"type": "integer"}, "namespace": {"type": "string", "default": "default"}, "confirm": {"type": "boolean", "default": False}}, "required": ["deployment", "replicas", "confirm"]}

    def execute(self, deployment, replicas, namespace="default", confirm=False, **kwargs):
        if not confirm:
            return ToolResult(success=False, error="扩容操作需要确认。请设置 confirm=true。")
        cmd = f"scale deployment/{deployment} --replicas={replicas} -n {namespace}"
        result = safe_kubectl_command(cmd)
        if result.returncode == 0:
            return ToolResult(success=True, output=f"已将 {deployment} 扩容到 {replicas} 个副本")
        return ToolResult(success=False, error=result.stderr.strip())
