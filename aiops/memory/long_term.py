"""长期记忆 - 持久化存储"""
import json
import time
import uuid
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from .base import BaseMemory, MemoryEntry, MemoryType, MemoryImportance

logger = logging.getLogger(__name__)


class LongTermMemory(BaseMemory):
    """长期记忆 - 持久化存储到文件"""

    def __init__(self, storage_path: str = "./data/memory", max_size: int = 10000):
        """
        初始化长期记忆

        Args:
            storage_path: 存储路径
            max_size: 最大容量
        """
        super().__init__(max_size=max_size, name="long_term")
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._index_file = self.storage_path / "index.json"
        self._load_index()

    def _load_index(self):
        """加载索引"""
        if self._index_file.exists():
            try:
                with open(self._index_file, "r", encoding="utf-8") as f:
                    index_data = json.load(f)
                for entry_id, entry_data in index_data.items():
                    self._entries[entry_id] = MemoryEntry.from_dict(entry_data)
                logger.info(f"加载了 {len(self._entries)} 条长期记忆")
            except Exception as e:
                logger.error(f"加载索引失败: {e}")

    def _save_index(self):
        """保存索引"""
        try:
            index_data = {eid: entry.to_dict() for eid, entry in self._entries.items()}
            with open(self._index_file, "w", encoding="utf-8") as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存索引失败: {e}")

    def add(self, entry: MemoryEntry) -> bool:
        """添加记忆"""
        if len(self._entries) >= self.max_size:
            self._evict_least_important()

        entry.memory_type = MemoryType.LONG_TERM
        self._entries[entry.id] = entry

        # 保存内容到单独文件
        self._save_entry_content(entry)

        # 更新索引
        self._save_index()
        return True

    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取记忆"""
        entry = self._entries.get(entry_id)
        if entry:
            # 尝试加载内容
            if not entry.content:
                entry.content = self._load_entry_content(entry_id)
            self.update_access(entry_id)
            self._save_index()
        return entry

    def search(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """搜索记忆"""
        results = []
        query_lower = query.lower()

        for entry in self._entries.values():
            # 加载内容
            if not entry.content:
                entry.content = self._load_entry_content(entry.id)

            # 关键词匹配
            if query_lower in entry.content.lower():
                results.append(entry)
            elif any(query_lower in tag.lower() for tag in entry.tags):
                results.append(entry)
            elif any(query_lower in str(v).lower() for v in entry.metadata.values()):
                results.append(entry)

        # 按重要性和访问频率排序
        results.sort(
            key=lambda e: (
                {"critical": 4, "high": 3, "medium": 2, "low": 1}[e.importance.value],
                e.access_count
            ),
            reverse=True
        )
        return results[:limit]

    def delete(self, entry_id: str) -> bool:
        """删除记忆"""
        if entry_id in self._entries:
            # 删除内容文件
            content_file = self.storage_path / f"{entry_id}.json"
            if content_file.exists():
                content_file.unlink()

            del self._entries[entry_id]
            self._save_index()
            return True
        return False

    def _save_entry_content(self, entry: MemoryEntry):
        """保存条目内容"""
        content_file = self.storage_path / f"{entry.id}.json"
        content_data = {
            "id": entry.id,
            "content": entry.content,
            "metadata": entry.metadata,
        }
        with open(content_file, "w", encoding="utf-8") as f:
            json.dump(content_data, f, ensure_ascii=False, indent=2)

    def _load_entry_content(self, entry_id: str) -> str:
        """加载条目内容"""
        content_file = self.storage_path / f"{entry_id}.json"
        if content_file.exists():
            try:
                with open(content_file, "r", encoding="utf-8") as f:
                    content_data = json.load(f)
                return content_data.get("content", "")
            except Exception as e:
                logger.error(f"加载内容失败: {e}")
        return ""

    def _evict_least_important(self):
        """移除最不重要的记忆"""
        if not self._entries:
            return

        # 按重要性排序
        importance_order = {
            MemoryImportance.CRITICAL: 0,
            MemoryImportance.HIGH: 1,
            MemoryImportance.MEDIUM: 2,
            MemoryImportance.LOW: 3,
        }

        # 找到最不重要的
        least_important_id = min(
            self._entries.keys(),
            key=lambda k: (
                importance_order[self._entries[k].importance],
                self._entries[k].access_count
            )
        )
        self.delete(least_important_id)

    def add_task_result(self, task_id: str, task: str, result: str,
                        success: bool, tools_used: List[str] = None):
        """添加任务执行结果"""
        entry = MemoryEntry(
            id=f"task_{task_id}",
            content=f"任务: {task}\n结果: {result}",
            memory_type=MemoryType.EPISODIC,
            importance=MemoryImportance.HIGH if success else MemoryImportance.CRITICAL,
            metadata={
                "task_id": task_id,
                "success": success,
                "tools_used": tools_used or [],
            },
            tags=["task_result", "success" if success else "failure"],
        )
        self.add(entry)

    def add故障经验(self, fault_type: str, symptoms: List[str],
                   root_cause: str, solution: str):
        """添加故障经验"""
        content = f"""故障类型: {fault_type}
症状: {', '.join(symptoms)}
根本原因: {root_cause}
解决方案: {solution}"""

        entry = MemoryEntry(
            id=f"fault_{uuid.uuid4().hex[:8]}",
            content=content,
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            metadata={
                "fault_type": fault_type,
                "symptoms": symptoms,
                "root_cause": root_cause,
                "solution": solution,
            },
            tags=["fault", fault_type] + symptoms,
        )
        self.add(entry)
