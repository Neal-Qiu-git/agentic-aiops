"""Runbook 管理器"""
import json
import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class RunbookManager:
    """Runbook 管理器 - 加载和搜索运维剧本"""

    def __init__(self, data_dir: str = None):
        """
        初始化 Runbook 管理器

        Args:
            data_dir: 数据目录路径
        """
        if data_dir is None:
            # 默认路径: 项目根目录/data/knowledge
            data_dir = str(Path(__file__).parent.parent.parent / "data" / "knowledge")

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._runbooks: List[Dict[str, Any]] = []
        self._load_runbooks()

    def _load_runbooks(self):
        """加载 Runbook"""
        runbook_file = self.data_dir / "runbooks.json"

        if runbook_file.exists():
            try:
                with open(runbook_file, "r", encoding="utf-8") as f:
                    self._runbooks = json.load(f)
                logger.info(f"Loaded {len(self._runbooks)} runbooks")
            except Exception as e:
                logger.error(f"Failed to load runbooks: {e}")
                self._runbooks = []
        else:
            logger.warning(f"Runbook file not found: {runbook_file}")
            self._runbooks = []

        # 加载书籍知识
        self._load_books()

    def _load_books(self):
        """加载书籍知识"""
        books_dir = self.data_dir / "books"
        if not books_dir.exists():
            books_dir.mkdir(parents=True, exist_ok=True)

        # 加载所有 JSON 书籍
        for book_file in books_dir.glob("*.json"):
            try:
                with open(book_file, "r", encoding="utf-8") as f:
                    book = json.load(f)
                    # 转换为 runbook 格式
                    runbook = self._book_to_runbook(book)
                    if runbook:
                        self._runbooks.append(runbook)
                        logger.info(f"Loaded book: {book.get('title', book_file.name)}")
            except Exception as e:
                logger.error(f"Failed to load book {book_file}: {e}")

    def _book_to_runbook(self, book: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """将书籍转换为 Runbook 格式"""
        if not book.get("id") or not book.get("title"):
            return None

        # 构建症状列表
        symptoms = []
        for chapter in book.get("chapters", []):
            for topic in chapter.get("topics", []):
                symptoms.append(topic.lower())

        # 添加关键主题
        for topic in book.get("key_topics", []):
            symptoms.append(topic.lower())

        # 构建诊断命令（基于章节）
        diagnosis_commands = []
        for chapter in book.get("chapters", []):
            diagnosis_commands.append(f"# Chapter {chapter.get('chapter')}: {chapter.get('title')}")
            for topic in chapter.get("topics", []):
                diagnosis_commands.append(f"# - {topic}")

        return {
            "id": book["id"],
            "title": book["title"],
            "category": book.get("category", "reference"),
            "severity": "info",
            "symptoms": symptoms,
            "description": book.get("description", ""),
            "diagnosis": {
                "commands": diagnosis_commands,
                "log_files": [],
                "metrics": []
            },
            "root_causes": [],
            "fixes": [],
            "verification": "",
            "prevention": [],
            "tags": book.get("tags", []),
            "source": "book",
            "author": book.get("author", ""),
            "chapters": book.get("chapters", []),
            "key_topics": book.get("key_topics", [])
        }

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        搜索 Runbook

        Args:
            query: 搜索关键词
            limit: 返回数量

        Returns:
            匹配的 Runbook 列表
        """
        query_lower = query.lower()
        results = []

        for runbook in self._runbooks:
            score = self._calculate_score(runbook, query_lower)
            if score > 0:
                results.append((score, runbook))

        # 按分数排序
        results.sort(key=lambda x: x[0], reverse=True)

        return [runbook for _, runbook in results[:limit]]

    def _calculate_score(self, runbook: Dict[str, Any], query: str) -> int:
        """计算匹配分数"""
        score = 0

        # 匹配标题
        if query in runbook.get("title", "").lower():
            score += 10

        # 匹配症状
        for symptom in runbook.get("symptoms", []):
            if query in symptom.lower():
                score += 5

        # 匹配描述
        if query in runbook.get("description", "").lower():
            score += 3

        # 匹配标签
        for tag in runbook.get("tags", []):
            if query in tag.lower():
                score += 2

        # 匹配分类
        if query in runbook.get("category", "").lower():
            score += 2

        return score

    def get_by_id(self, runbook_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 获取 Runbook"""
        for runbook in self._runbooks:
            if runbook.get("id") == runbook_id:
                return runbook
        return None

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """根据分类获取 Runbook"""
        return [
            r for r in self._runbooks
            if r.get("category") == category
        ]

    def get_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """根据严重程度获取 Runbook"""
        return [
            r for r in self._runbooks
            if r.get("severity") == severity
        ]

    def list_categories(self) -> List[str]:
        """列出所有分类"""
        categories = set()
        for runbook in self._runbooks:
            if "category" in runbook:
                categories.add(runbook["category"])
        return sorted(list(categories))

    def list_all(self) -> List[Dict[str, Any]]:
        """列出所有 Runbook"""
        return self._runbooks

    def add_runbook(self, runbook: Dict[str, Any]):
        """添加 Runbook"""
        # 检查是否已存在
        existing = self.get_by_id(runbook.get("id"))
        if existing:
            # 更新
            self._runbooks = [
                r if r.get("id") != runbook.get("id") else runbook
                for r in self._runbooks
            ]
        else:
            # 添加
            self._runbooks.append(runbook)

        self._save_runbooks()

    def remove_runbook(self, runbook_id: str) -> bool:
        """删除 Runbook"""
        original_count = len(self._runbooks)
        self._runbooks = [
            r for r in self._runbooks
            if r.get("id") != runbook_id
        ]

        if len(self._runbooks) < original_count:
            self._save_runbooks()
            return True
        return False

    def _save_runbooks(self):
        """保存 Runbook"""
        runbook_file = self.data_dir / "runbooks.json"
        try:
            with open(runbook_file, "w", encoding="utf-8") as f:
                json.dump(self._runbooks, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self._runbooks)} runbooks")
        except Exception as e:
            logger.error(f"Failed to save runbooks: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {
            "total": len(self._runbooks),
            "by_category": {},
            "by_severity": {},
        }

        for runbook in self._runbooks:
            category = runbook.get("category", "unknown")
            severity = runbook.get("severity", "unknown")

            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1

        return stats


# 全局实例
_manager: Optional[RunbookManager] = None


def get_runbook_manager() -> RunbookManager:
    """获取全局 Runbook 管理器"""
    global _manager
    if _manager is None:
        _manager = RunbookManager()
    return _manager
