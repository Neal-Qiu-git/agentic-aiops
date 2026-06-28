"""Semantic Memory - 语义记忆"""
import time
import uuid
import logging
from typing import List, Optional, Dict, Any
from .base import BaseMemory, MemoryEntry, MemoryType, MemoryImportance

logger = logging.getLogger(__name__)


class SemanticMemory(BaseMemory):
    """Semantic Memory - 基于向量的语义记忆"""

    def __init__(self, max_size: int = 10000, embedding_dim: int = 768):
        """
        初始化语义记忆

        Args:
            max_size: 最大容量
            embedding_dim: 向量维度
        """
        super().__init__(max_size=max_size, name="semantic")
        self.embedding_dim = embedding_dim
        self._embeddings: Dict[str, List[float]] = {}

    def add(self, entry: MemoryEntry) -> bool:
        """添加记忆"""
        if len(self._entries) >= self.max_size:
            self._evict_least_accessed()

        entry.memory_type = MemoryType.SEMANTIC
        self._entries[entry.id] = entry

        # 生成简单 embedding（实际应该使用模型）
        self._embeddings[entry.id] = self._generate_embedding(entry.content)

        return True

    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取记忆"""
        entry = self._entries.get(entry_id)
        if entry:
            self.update_access(entry_id)
        return entry

    def search(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """语义搜索"""
        query_embedding = self._generate_embedding(query)

        results = []
        for entry_id, entry in self._entries.items():
            if entry_id in self._embeddings:
                # 计算余弦相似度
                similarity = self._cosine_similarity(
                    query_embedding,
                    self._embeddings[entry_id]
                )
                if similarity > 0.3:  # 阈值
                    results.append((entry, similarity))

        # 按相似度排序
        results.sort(key=lambda x: x[1], reverse=True)

        return [entry for entry, _ in results[:limit]]

    def delete(self, entry_id: str) -> bool:
        """删除记忆"""
        if entry_id in self._entries:
            del self._entries[entry_id]
            if entry_id in self._embeddings:
                del self._embeddings[entry_id]
            return True
        return False

    def _generate_embedding(self, text: str) -> List[float]:
        """生成简单 embedding（实际应该使用模型）"""
        # 简单的 TF-based embedding
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()

        # 转换为向量
        embedding = []
        for i in range(0, min(len(hash_hex), self.embedding_dim * 2), 2):
            val = int(hash_hex[i:i+2], 16) / 255.0
            embedding.append(val)

        # 填充到指定维度
        while len(embedding) < self.embedding_dim:
            embedding.append(0.0)

        return embedding[:self.embedding_dim]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        import math

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _evict_least_accessed(self):
        """移除最少访问的记忆"""
        if not self._entries:
            return

        least_accessed_id = min(
            self._entries.keys(),
            key=lambda k: self._entries[k].access_count
        )
        self.delete(least_accessed_id)

    def add_incident_pattern(self, pattern: str, solution: str, tags: List[str] = None):
        """添加故障模式"""
        content = f"模式: {pattern}\n解决方案: {solution}"
        entry = MemoryEntry(
            id=f"pattern_{uuid.uuid4().hex[:8]}",
            content=content,
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            tags=["pattern"] + (tags or []),
        )
        self.add(entry)

    def find_similar_patterns(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """查找类似模式"""
        results = self.search(query, limit)
        return [
            {
                "id": entry.id,
                "content": entry.content,
                "tags": entry.tags,
            }
            for entry in results
        ]
