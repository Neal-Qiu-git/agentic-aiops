"""Approval 基类"""
import time
import uuid
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ApprovalStatus(Enum):
    """审批状态"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class ApprovalType(Enum):
    """审批类型"""
    COMMAND = "command"           # 命令执行
    DEPLOYMENT = "deployment"     # 部署操作
    CONFIGURATION = "configuration"  # 配置变更
    SECURITY = "security"         # 安全操作
    FINANCIAL = "financial"       # 费用相关
    INFRASTRUCTURE = "infrastructure"  # 基础设施变更


@dataclass
class ApprovalRequest:
    """审批请求"""
    id: str = field(default_factory=lambda: f"apr_{uuid.uuid4().hex[:8]}")
    approval_type: ApprovalType = ApprovalType.COMMAND
    title: str = ""
    description: str = ""
    requester: str = "aiops-agent"
    command: str = ""
    risk_level: str = "medium"  # low, medium, high, critical
    context: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 300  # 超时时间（秒）
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[float] = None
    comments: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "approval_type": self.approval_type.value,
            "title": self.title,
            "description": self.description,
            "requester": self.requester,
            "command": self.command,
            "risk_level": self.risk_level,
            "context": self.context,
            "timeout": self.timeout,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at,
            "comments": self.comments,
        }

    @property
    def is_expired(self) -> bool:
        """检查是否已过期"""
        return time.time() - self.created_at > self.timeout

    @property
    def wait_time(self) -> float:
        """等待时间（秒）"""
        return time.time() - self.created_at
