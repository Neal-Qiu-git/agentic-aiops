"""EventBus 基类"""
import time
import uuid
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from enum import Enum

logger = logging.getLogger(__name__)


class EventType(Enum):
    """事件类型"""
    # 系统事件
    SYSTEM_START = "system.start"
    SYSTEM_STOP = "system.stop"
    SYSTEM_ERROR = "system.error"

    # 监控事件
    METRIC_ALERT = "metric.alert"
    METRIC_RECOVERY = "metric.recovery"
    LOG_ERROR = "log.error"
    LOG_WARNING = "log.warning"

    # 告警事件
    ALARM_FIRED = "alarm.fired"
    ALARM_RESOLVED = "alarm.resolved"
    ALARM_ACKNOWLEDGED = "alarm.acknowledged"

    # Agent 事件
    AGENT_START = "agent.start"
    AGENT_COMPLETE = "agent.complete"
    AGENT_ERROR = "agent.error"
    AGENT_TIMEOUT = "agent.timeout"

    # 工作流事件
    WORKFLOW_START = "workflow.start"
    WORKFLOW_COMPLETE = "workflow.complete"
    WORKFLOW_FAILED = "workflow.failed"
    WORKFLOW_STEP = "workflow.step"

    # 审批事件
    APPROVAL_REQUEST = "approval.request"
    APPROVAL_GRANTED = "approval.granted"
    APPROVAL_REJECTED = "approval.rejected"

    # 运维事件
    INCIDENT_CREATED = "incident.created"
    INCIDENT_UPDATED = "incident.updated"
    INCIDENT_RESOLVED = "incident.resolved"

    # 工具事件
    TOOL_EXECUTION = "tool.execution"
    TOOL_SUCCESS = "tool.success"
    TOOL_FAILURE = "tool.failure"

    # 自定义事件
    CUSTOM = "custom"


@dataclass
class BaseEvent:
    """事件基类"""
    id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    event_type: EventType = EventType.CUSTOM
    source: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "event_type": self.event_type.value,
            "source": self.source,
            "data": self.data,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class EventHandler:
    """事件处理器"""
    handler: Callable
    event_types: List[EventType]
    priority: int = 0
    filter_func: Optional[Callable] = None

    def should_handle(self, event: BaseEvent) -> bool:
        """检查是否应该处理此事件"""
        if event.event_type not in self.event_types:
            return False
        if self.filter_func and not self.filter_func(event):
            return False
        return True
