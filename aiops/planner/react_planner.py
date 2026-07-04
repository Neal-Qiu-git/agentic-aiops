"""ReAct Planner - 基于 ReAct 的规划器"""
import time
import uuid
import logging
from typing import Any, Dict, List, Optional
from .base import BasePlanner, Plan, PlanStep, PlanStatus, StepStatus

logger = logging.getLogger(__name__)


class ReActPlanner(BasePlanner):
    """ReAct Planner - 思考-行动-观察循环"""

    def __init__(self, ai_client=None, tool_registry=None):
        self.ai = ai_client
        self.tool_registry = tool_registry

    def create_plan(self, goal: str, context: Dict[str, Any] = None) -> Plan:
        """创建计划"""
        context = context or {}

        # 使用 LLM 分解目标
        steps = self.decompose_goal(goal, context)

        plan = Plan(
            goal=goal,
            steps=steps,
            metadata=context,
        )

        logger.info(f"创建计划: {plan.id}, 目标: {goal}, 步骤数: {len(steps)}")
        return plan

    def decompose_goal(self, goal: str, context: Dict[str, Any] = None) -> List[PlanStep]:
        """将目标分解为步骤"""
        # 如果有 LLM，使用 LLM 分解
        if self.ai and self.ai.available:
            return self._decompose_with_llm(goal, context)

        # 否则使用预定义的模板
        return self._decompose_with_template(goal, context)

    def _decompose_with_llm(self, goal: str, context: Dict[str, Any]) -> List[PlanStep]:
        """使用 LLM 分解目标"""
        # 构建 prompt
        tools_desc = ""
        if self.tool_registry:
            tools = self.tool_registry.list_tools()
            tools_desc = "\n".join([f"- {t['name']}: {t['description']}" for t in tools[:20]])

        prompt = f"""你是一个运维专家，请将以下目标分解为具体的执行步骤。

目标: {goal}

可用工具:
{tools_desc}

请按以下格式输出步骤（每行一个步骤，格式：步骤名称 | 步骤描述 | 需要的工具）:
"""

        try:
            response = self.ai.analyze(str(context), prompt)
            steps = self._parse_llm_response(response)
            return steps
        except Exception as e:
            logger.error(f"LLM 分解失败: {e}")
            return self._decompose_with_template(goal, context)

    def _parse_llm_response(self, response: str) -> List[PlanStep]:
        """解析 LLM 响应"""
        steps = []
        lines = response.strip().split("\n")

        for i, line in enumerate(lines):
            line = line.strip()
            if not line or "|" not in line:
                continue

            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2:
                continue

            name = parts[0]
            description = parts[1] if len(parts) > 1 else ""
            tools = parts[2].split(",") if len(parts) > 2 and parts[2] else []

            step = PlanStep(
                id=f"step_{i+1}",
                name=name,
                description=description,
                tools=tools,
                dependencies=[f"step_{i}"] if i > 0 else [],
            )
            steps.append(step)

        return steps

    def _decompose_with_template(self, goal: str, context: Dict[str, Any]) -> List[PlanStep]:
        """使用模板分解目标"""
        # 根据关键词匹配模板
        goal_lower = goal.lower()

        if "pod" in goal_lower and ("crash" in goal_lower or "restart" in goal_lower):
            return self._k8s_pod_troubleshoot()
        elif "cpu" in goal_lower and "高" in goal_lower:
            return self._high_cpu_diagnose()
        elif "disk" in goal_lower and ("满" in goal_lower or "空间" in goal_lower):
            return self._disk_full_diagnose()
        elif "service" in goal_lower and ("down" in goal_lower or "停止" in goal_lower):
            return self._service_down_diagnose()
        elif "redis" in goal_lower:
            return self._redis_diagnose()
        elif "mysql" in goal_lower or "数据库" in goal_lower:
            return self._mysql_diagnose()
        else:
            return self._generic_diagnose()

    def _k8s_pod_troubleshoot(self) -> List[PlanStep]:
        """K8s Pod 故障排查"""
        return [
            PlanStep(id="step_1", name="查看 Pod 状态", description="获取 Pod 列表和状态", tools=["k8s_get_pods"]),
            PlanStep(id="step_2", name="查看事件", description="获取 Pod 相关事件", tools=["k8s_get_events"], dependencies=["step_1"]),
            PlanStep(id="step_3", name="查看日志", description="获取 Pod 日志", tools=["k8s_logs"], dependencies=["step_1"]),
            PlanStep(id="step_4", name="查看详情", description="获取 Pod 详细信息", tools=["k8s_describe_pod"], dependencies=["step_1"]),
            PlanStep(id="step_5", name="综合分析", description="分析所有信息，给出结论", dependencies=["step_2", "step_3", "step_4"]),
        ]

    def _high_cpu_diagnose(self) -> List[PlanStep]:
        """CPU 高诊断"""
        return [
            PlanStep(id="step_1", name="查看 CPU 使用率", description="获取当前 CPU 使用情况", tools=["ssh_exec"]),
            PlanStep(id="step_2", name="查看进程", description="找出占用 CPU 最高的进程", tools=["ssh_exec"]),
            PlanStep(id="step_3", name="分析进程", description="分析进程详细信息", tools=["ssh_exec"], dependencies=["step_2"]),
            PlanStep(id="step_4", name="给出建议", description="根据分析结果给出处理建议", dependencies=["step_1", "step_3"]),
        ]

    def _disk_full_diagnose(self) -> List[PlanStep]:
        """磁盘满诊断"""
        return [
            PlanStep(id="step_1", name="查看磁盘使用", description="获取磁盘使用情况", tools=["ssh_exec"]),
            PlanStep(id="step_2", name="查找大文件", description="找出占用空间最大的文件", tools=["ssh_exec"]),
            PlanStep(id="step_3", name="检查日志", description="检查日志文件大小", tools=["ssh_exec"]),
            PlanStep(id="step_4", name="给出清理建议", description="根据分析结果给出清理方案", dependencies=["step_1", "step_2", "step_3"]),
        ]

    def _service_down_diagnose(self) -> List[PlanStep]:
        """服务停止诊断"""
        return [
            PlanStep(id="step_1", name="检查服务状态", description="查看服务是否在运行", tools=["ssh_exec"]),
            PlanStep(id="step_2", name="查看日志", description="查看服务日志", tools=["ssh_exec"]),
            PlanStep(id="step_3", name="检查端口", description="检查服务端口是否监听", tools=["ssh_exec"]),
            PlanStep(id="step_4", name="分析原因", description="综合分析服务停止原因", dependencies=["step_1", "step_2", "step_3"]),
        ]

    def _redis_diagnose(self) -> List[PlanStep]:
        """Redis 诊断"""
        return [
            PlanStep(id="step_1", name="检查 Redis 状态", description="查看 Redis 是否运行", tools=["ssh_exec"]),
            PlanStep(id="step_2", name="检查连接", description="测试 Redis 连接", tools=["ssh_exec"]),
            PlanStep(id="step_3", name="查看信息", description="获取 Redis 信息", tools=["ssh_exec"]),
            PlanStep(id="step_4", name="分析内存", description="分析 Redis 内存使用", tools=["ssh_exec"]),
            PlanStep(id="step_5", name="给出建议", description="根据分析结果给出建议", dependencies=["step_1", "step_2", "step_3", "step_4"]),
        ]

    def _mysql_diagnose(self) -> List[PlanStep]:
        """MySQL 诊断"""
        return [
            PlanStep(id="step_1", name="检查 MySQL 状态", description="查看 MySQL 是否运行", tools=["ssh_exec"]),
            PlanStep(id="step_2", name="检查连接", description="测试 MySQL 连接", tools=["ssh_exec"]),
            PlanStep(id="step_3", name="查看进程", description="查看 MySQL 进程列表", tools=["ssh_exec"]),
            PlanStep(id="step_4", name="分析慢查询", description="分析慢查询日志", tools=["ssh_exec"]),
            PlanStep(id="step_5", name="给出建议", description="根据分析结果给出建议", dependencies=["step_1", "step_2", "step_3", "step_4"]),
        ]

    def _generic_diagnose(self) -> List[PlanStep]:
        """通用诊断"""
        return [
            PlanStep(id="step_1", name="收集信息", description="收集系统基本信息", tools=["ssh_exec"]),
            PlanStep(id="step_2", name="查看日志", description="查看系统日志", tools=["ssh_exec"]),
            PlanStep(id="step_3", name="分析问题", description="分析收集到的信息", dependencies=["step_1", "step_2"]),
            PlanStep(id="step_4", name="给出建议", description="根据分析结果给出建议", dependencies=["step_3"]),
        ]

    def update_plan(self, plan: Plan, step_result: Dict[str, Any]) -> Plan:
        """根据执行结果更新计划"""
        # 更新当前步骤状态
        current_steps = [s for s in plan.steps if s.status == StepStatus.RUNNING]
        for step in current_steps:
            if step_result.get("success"):
                step.status = StepStatus.COMPLETED
                step.result = step_result.get("result")
            else:
                step.status = StepStatus.FAILED
                step.error = step_result.get("error")

        # 检查是否有下一步
        next_steps = plan.get_next_steps()
        if not next_steps:
            # 检查是否所有步骤都完成
            all_completed = all(s.status == StepStatus.COMPLETED for s in plan.steps)
            all_failed = any(s.status == StepStatus.FAILED for s in plan.steps)

            if all_completed:
                plan.status = PlanStatus.COMPLETED
                plan.completed_at = time.time()
            elif all_failed:
                plan.status = PlanStatus.FAILED
                plan.error = "所有步骤都失败"
                plan.completed_at = time.time()

        return plan
