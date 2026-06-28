"""Planner 基类"""
import time
import uuid
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class PlanStatus(Enum):
    """计划状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(Enum):
    """步骤状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PlanStep:
    """计划步骤"""
    id: str
    name: str
    description: str
    agent: Optional[str] = None
    tools: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    timeout: int = 300
    retry_count: int = 3
    status: StepStatus = StepStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agent": self.agent,
            "tools": self.tools,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
        }


@dataclass
class Plan:
    """计划"""
    id: str = field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    goal: str = ""
    steps: List[PlanStep] = field(default_factory=list)
    status: PlanStatus = PlanStatus.PENDING
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "goal": self.goal,
            "steps": [s.to_dict() for s in self.steps],
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
        }

    def get_step(self, step_id: str) -> Optional[PlanStep]:
        """获取步骤"""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def get_next_steps(self) -> List[PlanStep]:
        """获取下一步可执行的步骤"""
        next_steps = []
        for step in self.steps:
            if step.status == StepStatus.PENDING:
                # 检查依赖是否都已完成
                deps_met = all(
                    self.get_step(dep) and self.get_step(dep).status == StepStatus.COMPLETED
                    for dep in step.dependencies
                )
                if deps_met:
                    next_steps.append(step)
        return next_steps


class BasePlanner(ABC):
    """规划器基类"""

    @abstractmethod
    def create_plan(self, goal: str, context: Dict[str, Any] = None) -> Plan:
        """
        创建计划

        Args:
            goal: 目标
            context: 上下文

        Returns:
            计划
        """
        pass

    @abstractmethod
    def update_plan(self, plan: Plan, step_result: Dict[str, Any]) -> Plan:
        """
        根据执行结果更新计划

        Args:
            plan: 原计划
            step_result: 步骤执行结果

        Returns:
            更新后的计划
        """
        pass

    @abstractmethod
    def decompose_goal(self, goal: str, context: Dict[str, Any] = None) -> List[PlanStep]:
        """
        将目标分解为步骤

        Args:
            goal: 目标
            context: 上下文

        Returns:
            步骤列表
        """
        pass
