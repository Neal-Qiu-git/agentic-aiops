"""Workflow 基类"""
import time
import uuid
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from enum import Enum

logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """工作流状态"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NodeType(Enum):
    """节点类型"""
    ACTION = "action"           # 执行动作
    CONDITION = "condition"     # 条件判断
    PARALLEL = "parallel"       # 并行执行
    SEQUENTIAL = "sequential"   # 顺序执行
    LOOP = "loop"               # 循环
    HUMAN = "human"             # 人工审批
    SUBWORKFLOW = "subworkflow" # 子工作流


@dataclass
class WorkflowNode:
    """工作流节点"""
    id: str
    name: str
    node_type: NodeType
    action: Optional[Callable] = None
    condition: Optional[Callable] = None
    config: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 300
    retry_count: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "node_type": self.node_type.value,
            "config": self.config,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
        }


@dataclass
class WorkflowEdge:
    """工作流边"""
    source: str
    target: str
    condition: Optional[Callable] = None
    label: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "label": self.label,
        }


@dataclass
class WorkflowContext:
    """工作流上下文"""
    workflow_id: str
    variables: Dict[str, Any] = field(default_factory=dict)
    node_results: Dict[str, Any] = field(default_factory=dict)
    current_node: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def set_variable(self, key: str, value: Any):
        self.variables[key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        return self.variables.get(key, default)

    def get_node_result(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self.node_results.get(node_id)

    def set_node_result(self, node_id: str, result: Dict[str, Any]):
        self.node_results[node_id] = result


class BaseWorkflow(ABC):
    """工作流基类"""

    def __init__(self, name: str, description: str = ""):
        self.id = f"wf_{uuid.uuid4().hex[:8]}"
        self.name = name
        self.description = description
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: List[WorkflowEdge] = []
        self.status = WorkflowStatus.PENDING
        self.context: Optional[WorkflowContext] = None
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.error: Optional[str] = None

    @abstractmethod
    def build(self):
        """构建工作流"""
        pass

    @abstractmethod
    def execute(self, context: WorkflowContext) -> Dict[str, Any]:
        """执行工作流"""
        pass

    def add_node(self, node: WorkflowNode):
        """添加节点"""
        self.nodes[node.id] = node

    def add_edge(self, edge: WorkflowEdge):
        """添加边"""
        self.edges.append(edge)

    def get_node(self, node_id: str) -> Optional[WorkflowNode]:
        """获取节点"""
        return self.nodes.get(node_id)

    def get_successors(self, node_id: str) -> List[str]:
        """获取后继节点"""
        return [e.target for e in self.edges if e.source == node_id]

    def get_predecessors(self, node_id: str) -> List[str]:
        """获取前驱节点"""
        return [e.source for e in self.edges if e.target == node_id]

    def get_root_nodes(self) -> List[str]:
        """获取根节点（没有前驱的节点）"""
        nodes_with_predecessors = {e.target for e in self.edges}
        return [n for n in self.nodes if n not in nodes_with_predecessors]

    def get_leaf_nodes(self) -> List[str]:
        """获取叶节点（没有后继的节点）"""
        nodes_with_successors = {e.source for e in self.edges}
        return [n for n in self.nodes if n not in nodes_with_successors]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "edges": [e.to_dict() for e in self.edges],
            "start_time": self.start_time,
            "end_time": self.end_time,
            "error": self.error,
        }

    def update_status(self, status: WorkflowStatus, error: str = None):
        """更新状态"""
        self.status = status
        if status == WorkflowStatus.COMPLETED:
            self.end_time = time.time()
        elif status == WorkflowStatus.FAILED:
            self.end_time = time.time()
            self.error = error
        elif status == WorkflowStatus.RUNNING:
            self.start_time = time.time()
