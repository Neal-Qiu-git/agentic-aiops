"""审批管理器"""
import time
import logging
import threading
from typing import Any, Callable, Dict, List, Optional
from .base import ApprovalRequest, ApprovalStatus, ApprovalType
from ..eventbus import get_event_bus, EventType

logger = logging.getLogger(__name__)


class ApprovalManager:
    """审批管理器"""

    def __init__(self, auto_approve_threshold: str = "low"):
        """
        初始化审批管理器

        Args:
            auto_approve_threshold: 自动审批阈值（low, medium, high, critical）
        """
        self._requests: Dict[str, ApprovalRequest] = {}
        self._callbacks: Dict[str, Callable] = {}
        self._auto_approve_threshold = auto_approve_threshold
        self._lock = threading.Lock()
        self._event_bus = get_event_bus()

        # 风险等级排序
        self._risk_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}

    def create_request(self, approval_type: ApprovalType, title: str,
                      description: str, command: str = "",
                      risk_level: str = "medium", context: Dict[str, Any] = None,
                      timeout: int = 300) -> ApprovalRequest:
        """
        创建审批请求

        Args:
            approval_type: 审批类型
            title: 标题
            description: 描述
            command: 命令
            risk_level: 风险等级
            context: 上下文
            timeout: 超时时间

        Returns:
            审批请求
        """
        request = ApprovalRequest(
            approval_type=approval_type,
            title=title,
            description=description,
            command=command,
            risk_level=risk_level,
            context=context or {},
            timeout=timeout,
        )

        with self._lock:
            self._requests[request.id] = request

        # 发布审批请求事件
        self._event_bus.emit(
            EventType.APPROVAL_REQUEST,
            source="approval_manager",
            request_id=request.id,
            title=title,
            risk_level=risk_level,
        )

        logger.info(f"创建审批请求: {request.id} - {title}")

        # 检查是否可以自动审批
        if self._should_auto_approve(request):
            self.approve(request.id, system="auto_approve")
            logger.info(f"自动审批: {request.id}")

        return request

    def approve(self, request_id: str, reviewer: str = "user",
                comments: str = "") -> bool:
        """
        审批通过

        Args:
            request_id: 请求 ID
            reviewer: 审批人
            comments: 备注

        Returns:
            是否成功
        """
        with self._lock:
            request = self._requests.get(request_id)
            if not request:
                logger.warning(f"审批请求不存在: {request_id}")
                return False

            if request.status != ApprovalStatus.PENDING:
                logger.warning(f"审批请求状态不是 pending: {request_id}")
                return False

            request.status = ApprovalStatus.APPROVED
            request.reviewed_by = reviewer
            request.reviewed_at = time.time()
            request.comments = comments
            request.updated_at = time.time()

        # 发布审批通过事件
        self._event_bus.emit(
            EventType.APPROVAL_GRANTED,
            source="approval_manager",
            request_id=request_id,
            reviewer=reviewer,
        )

        # 执行回调
        self._execute_callback(request_id)

        logger.info(f"审批通过: {request_id}")
        return True

    def reject(self, request_id: str, reviewer: str = "user",
               comments: str = "") -> bool:
        """
        审批拒绝

        Args:
            request_id: 请求 ID
            reviewer: 审批人
            comments: 备注

        Returns:
            是否成功
        """
        with self._lock:
            request = self._requests.get(request_id)
            if not request:
                logger.warning(f"审批请求不存在: {request_id}")
                return False

            if request.status != ApprovalStatus.PENDING:
                logger.warning(f"审批请求状态不是 pending: {request_id}")
                return False

            request.status = ApprovalStatus.REJECTED
            request.reviewed_by = reviewer
            request.reviewed_at = time.time()
            request.comments = comments
            request.updated_at = time.time()

        # 发布审批拒绝事件
        self._event_bus.emit(
            EventType.APPROVAL_REJECTED,
            source="approval_manager",
            request_id=request_id,
            reviewer=reviewer,
        )

        logger.info(f"审批拒绝: {request_id}")
        return True

    def cancel(self, request_id: str) -> bool:
        """取消审批请求"""
        with self._lock:
            request = self._requests.get(request_id)
            if not request:
                return False

            if request.status != ApprovalStatus.PENDING:
                return False

            request.status = ApprovalStatus.CANCELLED
            request.updated_at = time.time()

        logger.info(f"取消审批请求: {request_id}")
        return True

    def get_request(self, request_id: str) -> Optional[ApprovalRequest]:
        """获取审批请求"""
        return self._requests.get(request_id)

    def get_pending_requests(self) -> List[ApprovalRequest]:
        """获取待审批请求"""
        with self._lock:
            return [
                r for r in self._requests.values()
                if r.status == ApprovalStatus.PENDING and not r.is_expired
            ]

    def get_request_history(self, limit: int = 100) -> List[ApprovalRequest]:
        """获取审批历史"""
        with self._lock:
            requests = sorted(
                self._requests.values(),
                key=lambda r: r.created_at,
                reverse=True
            )
            return requests[:limit]

    def register_callback(self, request_id: str, callback: Callable):
        """注册审批回调"""
        self._callbacks[request_id] = callback

    def _execute_callback(self, request_id: str):
        """执行回调"""
        callback = self._callbacks.get(request_id)
        if callback:
            try:
                request = self._requests.get(request_id)
                callback(request)
            except Exception as e:
                logger.error(f"执行回调失败: {e}")
            finally:
                del self._callbacks[request_id]

    def _should_auto_approve(self, request: ApprovalRequest) -> bool:
        """检查是否应该自动审批"""
        request_level = self._risk_order.get(request.risk_level, 0)
        threshold_level = self._risk_order.get(self._auto_approve_threshold, 0)
        return request_level <= threshold_level

    def check_expired(self):
        """检查过期请求"""
        with self._lock:
            for request in self._requests.values():
                if request.status == ApprovalStatus.PENDING and request.is_expired:
                    request.status = ApprovalStatus.EXPIRED
                    request.updated_at = time.time()
                    logger.info(f"审批请求过期: {request.id}")

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            stats = {
                "total": len(self._requests),
                "pending": sum(1 for r in self._requests.values() if r.status == ApprovalStatus.PENDING),
                "approved": sum(1 for r in self._requests.values() if r.status == ApprovalStatus.APPROVED),
                "rejected": sum(1 for r in self._requests.values() if r.status == ApprovalStatus.REJECTED),
                "expired": sum(1 for r in self._requests.values() if r.status == ApprovalStatus.EXPIRED),
            }
        return stats


# 全局审批管理器实例
_global_manager: Optional[ApprovalManager] = None
_manager_lock = threading.Lock()


def get_approval_manager() -> ApprovalManager:
    """获取全局审批管理器"""
    global _global_manager
    if _global_manager is None:
        with _manager_lock:
            if _global_manager is None:
                _global_manager = ApprovalManager()
    return _global_manager
