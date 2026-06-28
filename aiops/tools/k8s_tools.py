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
