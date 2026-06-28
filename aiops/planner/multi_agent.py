"""Multi-Agent Planner - 多 Agent 协同规划"""
import logging
from typing import Any, Dict, List, Optional
from .base import BasePlanner, Plan, PlanStep, PlanStatus, StepStatus

logger = logging.getLogger(__name__)


class MultiAgentPlanner(BasePlanner):
    """Multi-Agent Planner - 多 Agent 协同规划"""

    # Agent 能力映射
    AGENT_CAPABILITIES = {
        "linux_agent": ["cpu", "memory", "disk", "network", "process", "service", "system"],
        "k8s_agent": ["pod", "deployment", "service", "node", "namespace", "kubectl", "kubernetes"],
        "db_agent": ["mysql", "redis", "mongodb", "postgresql", "database", "sql"],
        "log_agent": ["log", "logs", "error", "exception", "trace"],
        "monitor_agent": ["prometheus", "grafana", "metrics", "alert", "monitoring"],
        "security_agent": ["security", "vulnerability", "compliance", "audit", "permission"],
        "devops_agent": ["ci", "cd", "deploy", "release", "pipeline", "git", "docker"],
    }

    def __init__(self, agent_registry=None):
        self.agent_registry = agent_registry

    def create_plan(self, goal: str, context: Dict[str, Any] = None) -> Plan:
        """创建计划"""
        context = context or {}

        # 分解目标
        steps = self.decompose_goal(goal, context)

        plan = Plan(
            goal=goal,
            steps=steps,
            metadata=context,
        )

        logger.info(f"创建多 Agent 计划: {plan.id}, 目标: {goal}")
        return plan

    def decompose_goal(self, goal: str, context: Dict[str, Any] = None) -> List[PlanStep]:
        """将目标分解为多 Agent 协同步骤"""
        context = context or {}

        # 识别需要的 Agent
        required_agents = self._identify_agents(goal)

        # 根据 Agent 能力分配任务
        steps = self._assign_tasks(goal, required_agents, context)

        return steps

    def _identify_agents(self, goal: str) -> List[str]:
        """识别需要的 Agent"""
        goal_lower = goal.lower()
        required_agents = []

        for agent, keywords in self.AGENT_CAPABILITIES.items():
            if any(keyword in goal_lower for keyword in keywords):
                required_agents.append(agent)

        # 如果没有匹配到，使用通用 Agent
        if not required_agents:
            required_agents = ["linux_agent"]

        return required_agents

    def _assign_tasks(self, goal: str, agents: List[str],
                     context: Dict[str, Any]) -> List[PlanStep]:
        """分配任务给 Agent"""
        steps = []
        step_num = 1

        # 为每个 Agent 创建任务
        for agent in agents:
            agent_tasks = self._get_agent_tasks(agent, goal, context)

            for task_name, task_desc, tools, deps in agent_tasks:
                step = PlanStep(
                    id=f"step_{step_num}",
                    name=task_name,
                    description=task_desc,
                    agent=agent,
                    tools=tools,
                    dependencies=[f"step_{d}" for d in deps],
                )
                steps.append(step)
                step_num += 1

        # 添加综合分析步骤
        if len(steps) > 1:
            steps.append(PlanStep(
                id=f"step_{step_num}",
                name="综合分析",
                description="综合所有 Agent 的分析结果，给出最终结论",
                dependencies=[f"step_{i}" for i in range(1, step_num)],
            ))

        return steps

    def _get_agent_tasks(self, agent: str, goal: str,
                        context: Dict[str, Any]) -> List[tuple]:
        """获取 Agent 的任务"""
        tasks = []

        if agent == "linux_agent":
            tasks = [
                ("收集系统信息", "收集 CPU、内存、磁盘等系统信息", ["ssh_exec"], []),
                ("分析进程", "分析占用资源的进程", ["ssh_exec"], [1]),
                ("检查服务", "检查相关服务状态", ["ssh_exec"], [1]),
            ]
        elif agent == "k8s_agent":
            tasks = [
                ("查看 Pod 状态", "获取 Pod 列表和状态", ["k8s_get_pods"], []),
                ("查看事件", "获取 K8s 事件", ["k8s_get_events"], [1]),
                ("查看日志", "获取 Pod 日志", ["k8s_logs"], [1]),
                ("查看详情", "获取 Pod 详细信息", ["k8s_describe_pod"], [1]),
            ]
        elif agent == "db_agent":
            tasks = [
                ("检查数据库状态", "检查数据库是否运行", ["ssh_exec"], []),
                ("检查连接", "测试数据库连接", ["ssh_exec"], [1]),
                ("分析查询", "分析慢查询和性能", ["ssh_exec"], [1]),
            ]
        elif agent == "log_agent":
            tasks = [
                ("收集日志", "收集相关日志", ["ssh_exec"], []),
                ("分析日志", "分析日志中的错误", ["ssh_exec"], [1]),
                ("追踪链路", "追踪请求链路", ["ssh_exec"], [1]),
            ]
        elif agent == "monitor_agent":
            tasks = [
                ("查询指标", "查询监控指标", ["ssh_exec"], []),
                ("分析趋势", "分析指标趋势", ["ssh_exec"], [1]),
                ("检查告警", "检查相关告警", ["ssh_exec"], [1]),
            ]
        elif agent == "security_agent":
            tasks = [
                ("安全扫描", "执行安全扫描", ["ssh_exec"], []),
                ("检查权限", "检查系统权限", ["ssh_exec"], [1]),
                ("审计日志", "审计系统日志", ["ssh_exec"], [1]),
            ]
        elif agent == "devops_agent":
            tasks = [
                ("检查部署", "检查部署状态", ["ssh_exec"], []),
                ("查看流水线", "查看 CI/CD 流水线", ["ssh_exec"], [1]),
                ("检查版本", "检查代码版本", ["ssh_exec"], [1]),
            ]

        return tasks

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
            all_completed = all(s.status == StepStatus.COMPLETED for s in plan.steps)
            all_failed = any(s.status == StepStatus.FAILED for s in plan.steps)

            if all_completed:
                plan.status = PlanStatus.COMPLETED
            elif all_failed:
                plan.status = PlanStatus.FAILED
                plan.error = "所有步骤都失败"

        return plan

    def get_agent_assignment(self, plan: Plan) -> Dict[str, List[PlanStep]]:
        """获取 Agent 任务分配"""
        assignment = {}
        for step in plan.steps:
            agent = step.agent or "default"
            if agent not in assignment:
                assignment[agent] = []
            assignment[agent].append(step)
        return assignment
