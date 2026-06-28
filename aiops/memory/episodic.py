"""情景记忆 - 记录具体事件"""
import time
import uuid
import logging
from typing import List, Optional, Dict, Any
from .base import BaseMemory, MemoryEntry, MemoryType, MemoryImportance

logger = logging.getLogger(__name__)


class EpisodicMemory(BaseMemory):
    """情景记忆 - 记录具体的运维事件和操作"""

    def __init__(self, max_size: int = 5000):
        super().__init__(max_size=max_size, name="episodic")

    def add(self, entry: MemoryEntry) -> bool:
        """添加记忆"""
        if len(self._entries) >= self.max_size:
            self._evict_oldest()

        entry.memory_type = MemoryType.EPISODIC
        self._entries[entry.id] = entry
        return True

    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取记忆"""
        entry = self._entries.get(entry_id)
        if entry:
            self.update_access(entry_id)
        return entry

    def search(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """搜索记忆"""
        results = []
        query_lower = query.lower()

        for entry in self._entries.values():
            # 关键词匹配
            if query_lower in entry.content.lower():
                results.append(entry)
            elif any(query_lower in tag.lower() for tag in entry.tags):
                results.append(entry)
            elif any(query_lower in str(v).lower() for v in entry.metadata.values()):
                results.append(entry)

        results.sort(key=lambda e: e.timestamp, reverse=True)
        return results[:limit]

    def delete(self, entry_id: str) -> bool:
        """删除记忆"""
        if entry_id in self._entries:
            del self._entries[entry_id]
            return True
        return False

    def record_event(self, event_type: str, description: str,
                    context: Dict[str, Any] = None, tags: List[str] = None):
        """记录事件"""
        entry = MemoryEntry(
            id=f"event_{uuid.uuid4().hex[:8]}",
            content=description,
            memory_type=MemoryType.EPISODIC,
            importance=MemoryImportance.MEDIUM,
            metadata={"event_type": event_type, **(context or {})},
            tags=[event_type] + (tags or []),
        )
        self.add(entry)
        return entry.id

    def record_incident(self, severity: str, service: str, symptoms: List[str],
                       root_cause: str = None, resolution: str = None):
        """记录故障事件"""
        content = f"""故障事件
服务: {service}
严重程度: {severity}
症状: {', '.join(symptoms)}
"""
        if root_cause:
            content += f"根本原因: {root_cause}\n"
        if resolution:
            content += f"解决方案: {resolution}\n"

        entry = MemoryEntry(
            id=f"incident_{uuid.uuid4().hex[:8]}",
            content=content,
            memory_type=MemoryType.EPISODIC,
            importance=MemoryImportance.CRITICAL if severity in ["P0", "P1"] else MemoryImportance.HIGH,
            metadata={
                "severity": severity,
                "service": service,
                "symptoms": symptoms,
                "root_cause": root_cause,
                "resolution": resolution,
            },
            tags=["incident", severity, service] + symptoms,
        )
        self.add(entry)
        return entry.id

    def record_tool_execution(self, tool_name: str, command: str,
                             result: str, success: bool, duration: float):
        """记录工具执行"""
        entry = MemoryEntry(
            id=f"exec_{uuid.uuid4().hex[:8]}",
            content=f"执行工具: {tool_name}\n命令: {command}\n结果: {result[:500]}",
            memory_type=MemoryType.EPISODIC,
            importance=MemoryImportance.LOW,
            metadata={
                "tool_name": tool_name,
                "command": command,
                "success": success,
                "duration": duration,
            },
            tags=["execution", tool_name, "success" if success else "failure"],
        )
        self.add(entry)
        return entry.id

    def record_decision(self, decision: str, reasoning: str,
                       alternatives: List[str] = None, outcome: str = None):
        """记录决策"""
        content = f"""决策: {decision}
推理: {reasoning}
"""
        if alternatives:
            content += f"备选方案: {', '.join(alternatives)}\n"
        if outcome:
            content += f"结果: {outcome}\n"

        entry = MemoryEntry(
            id=f"decision_{uuid.uuid4().hex[:8]}",
            content=content,
            memory_type=MemoryType.EPISODIC,
            importance=MemoryImportance.MEDIUM,
            metadata={
                "decision": decision,
                "reasoning": reasoning,
                "alternatives": alternatives,
                "outcome": outcome,
            },
            tags=["decision"],
        )
        self.add(entry)
        return entry.id

    def get_similar_incidents(self, symptoms: List[str], limit: int = 5) -> List[MemoryEntry]:
        """获取类似故障"""
        results = []
        symptom_set = set(s.lower() for s in symptoms)

        for entry in self._entries.values():
            entry_symptoms = set(s.lower() for s in entry.metadata.get("symptoms", []))
            # 计算相似度
            if entry_symptoms and symptom_set:
                intersection = len(symptom_set & entry_symptoms)
                union = len(symptom_set | entry_symptoms)
                if union > 0 and intersection / union > 0.3:  # Jaccard 相似度
                    results.append(entry)

        results.sort(key=lambda e: e.importance.value, reverse=True)
        return results[:limit]

    def get_incident_stats(self) -> Dict[str, Any]:
        """获取故障统计"""
        incidents = [
            e for e in self._entries.values()
            if e.metadata.get("severity")
        ]

        stats = {
            "total": len(incidents),
            "by_severity": {},
            "by_service": {},
            "by_hour": {},
        }

        for incident in incidents:
            severity = incident.metadata.get("severity", "unknown")
            service = incident.metadata.get("service", "unknown")
            hour = time.localtime(incident.timestamp).tm_hour

            stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1
            stats["by_service"][service] = stats["by_service"].get(service, 0) + 1
            stats["by_hour"][hour] = stats["by_hour"].get(hour, 0) + 1

        return stats

    def _evict_oldest(self):
        """移除最旧的记忆"""
        if not self._entries:
            return
        oldest_id = min(self._entries.keys(), key=lambda k: self._entries[k].timestamp)
        del self._entries[oldest_id]
