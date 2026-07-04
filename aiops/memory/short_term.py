"""短期记忆 - 当前会话"""
import time
import uuid
from typing import List, Optional
from .base import BaseMemory, MemoryEntry, MemoryType, MemoryImportance


class ShortTermMemory(BaseMemory):
    """短期记忆 - 存储当前会话的上下文"""

    def __init__(self, max_size: int = 100, ttl: int = 3600):
        """
        初始化短期记忆

        Args:
            max_size: 最大容量
            ttl: 生存时间（秒）
        """
        super().__init__(max_size=max_size, name="short_term")
        self.ttl = ttl

    def add(self, entry: MemoryEntry) -> bool:
        """添加记忆"""
        # 如果超过容量，移除最旧的
        if len(self._entries) >= self.max_size:
            self._evict_oldest()

        # 设置类型为短期
        entry.memory_type = MemoryType.SHORT_TERM
        self._entries[entry.id] = entry
        return True

    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取记忆"""
        entry = self._entries.get(entry_id)
        if entry and not self._is_expired(entry):
            self.update_access(entry_id)
            return entry
        elif entry:
            # 已过期，删除
            del self._entries[entry_id]
        return None

    def search(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """搜索记忆"""
        self._cleanup_expired()

        results = []
        query_lower = query.lower()

        for entry in self._entries.values():
            if self._is_expired(entry):
                continue

            # 简单的关键词匹配
            if query_lower in entry.content.lower():
                results.append(entry)
            elif any(query_lower in tag.lower() for tag in entry.tags):
                results.append(entry)

        # 按相关性排序
        results.sort(key=lambda e: e.importance.value, reverse=True)
        return results[:limit]

    def delete(self, entry_id: str) -> bool:
        """删除记忆"""
        if entry_id in self._entries:
            del self._entries[entry_id]
            return True
        return False

    def add_conversation(self, role: str, content: str, metadata: dict = None):
        """添加对话记录"""
        entry = MemoryEntry(
            id=f"conv_{uuid.uuid4().hex[:8]}",
            content=content,
            memory_type=MemoryType.SHORT_TERM,
            importance=MemoryImportance.MEDIUM,
            metadata={"role": role, **(metadata or {})},
            tags=["conversation", role],
        )
        self.add(entry)

    def add_observation(self, observation: str, source: str = "system"):
        """添加观察记录"""
        entry = MemoryEntry(
            id=f"obs_{uuid.uuid4().hex[:8]}",
            content=observation,
            memory_type=MemoryType.SHORT_TERM,
            importance=MemoryImportance.LOW,
            metadata={"source": source},
            tags=["observation", source],
        )
        self.add(entry)

    def get_conversation_history(self, limit: int = 20) -> List[dict]:
        """获取对话历史"""
        conversations = []
        for entry in self._entries.values():
            if entry.metadata.get("role") and not self._is_expired(entry):
                conversations.append({
                    "role": entry.metadata["role"],
                    "content": entry.content,
                    "timestamp": entry.timestamp,
                })
        conversations.sort(key=lambda x: x["timestamp"])
        return conversations[-limit:]

    def _is_expired(self, entry: MemoryEntry) -> bool:
        """检查是否过期"""
        return time.time() - entry.timestamp > self.ttl

    def _cleanup_expired(self):
        """清理过期记忆"""
        expired_ids = [
            entry_id for entry_id, entry in self._entries.items()
            if self._is_expired(entry)
        ]
        for entry_id in expired_ids:
            del self._entries[entry_id]

    def _evict_oldest(self):
        """移除最旧的记忆"""
        if not self._entries:
            return
        oldest_id = min(self._entries.keys(), key=lambda k: self._entries[k].timestamp)
        del self._entries[oldest_id]
