"""RAG 基类"""
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """文档"""
    id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    score: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
            "score": self.score,
        }


@dataclass
class RAGResponse:
    """RAG 响应"""
    answer: str
    sources: List[Document] = field(default_factory=list)
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "answer": self.answer,
            "sources": [s.to_dict() for s in self.sources],
            "confidence": self.confidence,
            "metadata": self.metadata,
        }


class BaseRetriever(ABC):
    """检索器基类"""

    @abstractmethod
    def retrieve(self, query: str, limit: int = 5) -> List[Document]:
        """
        检索相关文档

        Args:
            query: 查询
            limit: 返回数量

        Returns:
            文档列表
        """
        pass

    @abstractmethod
    def add_document(self, document: Document):
        """添加文档"""
        pass

    @abstractmethod
    def remove_document(self, doc_id: str):
        """移除文档"""
        pass


class BaseGenerator(ABC):
    """生成器基类"""

    @abstractmethod
    def generate(self, query: str, context: List[Document], **kwargs) -> str:
        """
        生成回答

        Args:
            query: 查询
            context: 上下文文档

        Returns:
            生成的回答
        """
        pass
