"""Memory 基类"""
import time
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """记忆类型"""
    SHORT_TERM = "short_term"      # 短期记忆（当前会话）
    LONG_TERM = "long_term"        # 长期记忆（持久化）
    EPISODIC = "episodic"          # 情景记忆（具体事件）
    SEMANTIC = "semantic"          # 语义记忆（知识）
    PROCEDURAL = "procedural"      # 程序记忆（操作步骤）


class MemoryImportance(Enum):
    """记忆重要性"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    memory_type: MemoryType
    importance: MemoryImportance = MemoryImportance.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    embedding: Optional[List[float]] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "importance": self.importance.value,
            "metadata": self.metadata,
            "tags": self.tags,
            "timestamp": self.timestamp,
            "last_accessed": self.last_accessed,
            "access_count": self.access_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryEntry":
        """从字典创建"""
        return cls(
            id=data["id"],
            content=data["content"],
            memory_type=MemoryType(data["memory_type"]),
            importance=MemoryImportance(data.get("importance", "medium")),
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
            timestamp=data.get("timestamp", time.time()),
            last_accessed=data.get("last_accessed", time.time()),
            access_count=data.get("access_count", 0),
        )


class BaseMemory(ABC):
    """记忆基类"""

    def __init__(self, max_size: int = 1000, name: str = "base"):
        self.max_size = max_size
        self.name = name
        self._entries: Dict[str, MemoryEntry] = {}

    @abstractmethod
    def add(self, entry: MemoryEntry) -> bool:
        """添加记忆"""
        pass

    @abstractmethod
    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取记忆"""
        pass

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """搜索记忆"""
        pass

    @abstractmethod
    def delete(self, entry_id: str) -> bool:
        """删除记忆"""
        pass

    def update_access(self, entry_id: str):
        """更新访问记录"""
        if entry_id in self._entries:
            entry = self._entries[entry_id]
            entry.last_accessed = time.time()
            entry.access_count += 1

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "name": self.name,
            "total_entries": len(self._entries),
            "max_size": self.max_size,
            "by_type": {
                t.value: sum(1 for e in self._entries.values() if e.memory_type == t)
                for t in MemoryType
            },
            "by_importance": {
                i.value: sum(1 for e in self._entries.values() if e.importance == i)
                for i in MemoryImportance
            },
        }

    def clear(self):
        """清空记忆"""
        self._entries.clear()
        logger.info(f"清空记忆: {self.name}")
