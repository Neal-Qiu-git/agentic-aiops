"""知识库基类"""
from abc import ABC, abstractmethod


class KnowledgeBase(ABC):
    """知识库基类 - 存储运维经验和解决方案"""

    def __init__(self):
        self._entries = []

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> list:
        """搜索相关知识"""
        pass

    def add(self, entry: dict):
        """添加知识条目"""
        self._entries.append(entry)

    def get(self, entry_id: str) -> dict:
        """获取知识条目"""
        for e in self._entries:
            if e.get("id") == entry_id:
                return e
        return None
