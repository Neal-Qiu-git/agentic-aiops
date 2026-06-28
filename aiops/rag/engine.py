"""RAG 引擎"""
import logging
from typing import List, Optional
from .base import BaseRetriever, BaseGenerator, Document, RAGResponse

logger = logging.getLogger(__name__)


class RAGEngine:
    """RAG 引擎 - 检索增强生成"""

    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        """
        初始化 RAG 引擎

        Args:
            retriever: 检索器
            generator: 生成器
        """
        self.retriever = retriever
        self.generator = generator

    def query(self, question: str, top_k: int = 5, **kwargs) -> RAGResponse:
        """
        查询

        Args:
            question: 问题
            top_k: 返回的文档数量

        Returns:
            RAG 响应
        """
        logger.info(f"RAG 查询: {question[:50]}...")

        # 1. 检索相关文档
        documents = self.retriever.retrieve(question, limit=top_k)
        logger.info(f"检索到 {len(documents)} 个文档")

        # 2. 生成回答
        answer = self.generator.generate(question, documents, **kwargs)

        # 3. 计算置信度
        confidence = self._calculate_confidence(documents)

        # 4. 构建响应
        response = RAGResponse(
            answer=answer,
            sources=documents,
            confidence=confidence,
            metadata={
                "question": question,
                "num_documents": len(documents),
            }
        )

        return response

    def add_knowledge(self, content: str, metadata: dict = None, doc_id: str = None):
        """添加知识"""
        import uuid
        document = Document(
            id=doc_id or f"doc_{uuid.uuid4().hex[:8]}",
            content=content,
            metadata=metadata or {},
        )
        self.retriever.add_document(document)
        logger.info(f"添加知识: {document.id}")

    def remove_knowledge(self, doc_id: str):
        """移除知识"""
        self.retriever.remove_document(doc_id)
        logger.info(f"移除知识: {doc_id}")

    def _calculate_confidence(self, documents: List[Document]) -> float:
        """计算置信度"""
        if not documents:
            return 0.0

        # 基于文档相似度计算置信度
        scores = [doc.score for doc in documents if doc.score is not None]
        if not scores:
            return 0.5

        # 平均分
        avg_score = sum(scores) / len(scores)

        # 数量加成
        count_bonus = min(len(documents) / 5, 1.0)

        return min(avg_score * 0.7 + count_bonus * 0.3, 1.0)


class SimpleRetriever(BaseRetriever):
    """简单检索器 - 基于关键词匹配"""

    def __init__(self):
        self._documents: List[Document] = []

    def retrieve(self, query: str, limit: int = 5) -> List[Document]:
        """检索相关文档"""
        query_lower = query.lower()
        results = []

        for doc in self._documents:
            # 简单的关键词匹配
            content_lower = doc.content.lower()
            if query_lower in content_lower:
                # 计算匹配分数
                score = content_lower.count(query_lower) / len(content_lower)
                doc_copy = Document(
                    id=doc.id,
                    content=doc.content,
                    metadata=doc.metadata,
                    score=score,
                )
                results.append(doc_copy)

        # 按分数排序
        results.sort(key=lambda d: d.score or 0, reverse=True)
        return results[:limit]

    def add_document(self, document: Document):
        """添加文档"""
        self._documents.append(document)

    def remove_document(self, doc_id: str):
        """移除文档"""
        self._documents = [d for d in self._documents if d.id != doc_id]


class SimpleGenerator(BaseGenerator):
    """简单生成器 - 直接返回上下文"""

    def generate(self, query: str, context: List[Document], **kwargs) -> str:
        """生成回答"""
        if not context:
            return "未找到相关信息"

        # 构建上下文
        context_text = "\n\n".join([doc.content for doc in context[:3]])

        # 生成回答（这里只是简单拼接，实际应该调用 LLM）
        answer = f"根据知识库中的信息：\n\n{context_text}"

        return answer
