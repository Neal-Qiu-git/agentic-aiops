"""EventBus 实现"""
import logging
import threading
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional
from .base import BaseEvent, EventType, EventHandler

logger = logging.getLogger(__name__)


class EventBus:
    """事件总线 - 发布/订阅模式"""

    def __init__(self):
        self._handlers: Dict[str, EventHandler] = {}
        self._event_type_handlers: Dict[EventType, List[str]] = defaultdict(list)
        self._history: List[BaseEvent] = []
        self._max_history = 1000
        self._lock = threading.Lock()
        self._async_mode = False

    def subscribe(self, event_type: EventType, handler: Callable,
                  priority: int = 0, filter_func: Callable = None) -> str:
        """
        订阅事件

        Args:
            event_type: 事件类型
            handler: 处理函数
            priority: 优先级（越大越先执行）
            filter_func: 过滤函数

        Returns:
            订阅 ID
        """
        handler_id = f"handler_{id(handler)}_{event_type.value}"

        event_handler = EventHandler(
            handler=handler,
            event_types=[event_type],
            priority=priority,
            filter_func=filter_func,
        )

        with self._lock:
            self._handlers[handler_id] = event_handler
            self._event_type_handlers[event_type].append(handler_id)
            # 按优先级排序
            self._event_type_handlers[event_type].sort(
                key=lambda hid: self._handlers[hid].priority,
                reverse=True
            )

        logger.debug(f"订阅事件: {event_type.value}, handler: {handler_id}")
        return handler_id

    def subscribe_many(self, event_types: List[EventType], handler: Callable,
                       priority: int = 0, filter_func: Callable = None) -> List[str]:
        """订阅多个事件"""
        handler_ids = []
        for event_type in event_types:
            handler_id = self.subscribe(event_type, handler, priority, filter_func)
            handler_ids.append(handler_id)
        return handler_ids

    def unsubscribe(self, handler_id: str):
        """取消订阅"""
        with self._lock:
            if handler_id in self._handlers:
                handler = self._handlers[handler_id]
                for event_type in handler.event_types:
                    if handler_id in self._event_type_handlers[event_type]:
                        self._event_type_handlers[event_type].remove(handler_id)
                del self._handlers[handler_id]
                logger.debug(f"取消订阅: {handler_id}")

    def publish(self, event: BaseEvent):
        """
        发布事件

        Args:
            event: 事件对象
        """
        # 记录历史
        with self._lock:
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]

        # 获取所有匹配的处理器
        handler_ids = self._event_type_handlers.get(event.event_type, [])

        logger.debug(f"发布事件: {event.event_type.value}, handlers: {len(handler_ids)}")

        # 执行处理器
        for handler_id in handler_ids:
            handler = self._handlers.get(handler_id)
            if handler and handler.should_handle(event):
                try:
                    handler.handler(event)
                except Exception as e:
                    logger.error(f"事件处理失败: {handler_id}, 错误: {e}")

    def publish_async(self, event: BaseEvent):
        """异步发布事件"""
        import asyncio
        asyncio.create_task(self._publish_async(event))

    async def _publish_async(self, event: BaseEvent):
        """异步发布事件"""
        self.publish(event)

    def emit(self, event_type: EventType, source: str = "", data: Dict[str, Any] = None, **kwargs):
        """便捷发布方法"""
        event = BaseEvent(
            event_type=event_type,
            source=source,
            data=data or kwargs,
        )
        self.publish(event)

    def get_history(self, event_type: Optional[EventType] = None, limit: int = 100) -> List[BaseEvent]:
        """获取事件历史"""
        with self._lock:
            if event_type:
                events = [e for e in self._history if e.event_type == event_type]
            else:
                events = self._history.copy()
            return events[-limit:]

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            stats = {
                "total_handlers": len(self._handlers),
                "total_events": len(self._history),
                "handlers_by_type": {
                    et.value: len(hids)
                    for et, hids in self._event_type_handlers.items()
                },
            }
        return stats

    def clear_history(self):
        """清空历史"""
        with self._lock:
            self._history.clear()

    def create_event(self, event_type: EventType, source: str = "", **data) -> BaseEvent:
        """创建事件"""
        return BaseEvent(
            event_type=event_type,
            source=source,
            data=data,
        )


# 全局事件总线实例
_global_bus: Optional[EventBus] = None
_bus_lock = threading.Lock()


def get_event_bus() -> EventBus:
    """获取全局事件总线"""
    global _global_bus
    if _global_bus is None:
        with _bus_lock:
            if _global_bus is None:
                _global_bus = EventBus()
    return _global_bus


def reset_event_bus():
    """重置全局事件总线"""
    global _global_bus
    with _bus_lock:
        _global_bus = None
