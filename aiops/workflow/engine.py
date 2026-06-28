"""工作流引擎"""
import time
import logging
import concurrent.futures
from typing import Any, Dict, List, Optional
from .base import (
    BaseWorkflow, WorkflowNode, WorkflowEdge, WorkflowContext,
    WorkflowStatus, NodeType
)

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """工作流引擎"""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self._workflows: Dict[str, BaseWorkflow] = {}
        self._running_workflows: Dict[str, BaseWorkflow] = {}

    def register_workflow(self, workflow: BaseWorkflow):
        """注册工作流"""
        self._workflows[workflow.id] = workflow
        logger.info(f"注册工作流: {workflow.name} ({workflow.id})")

    def get_workflow(self, workflow_id: str) -> Optional[BaseWorkflow]:
        """获取工作流"""
        return self._workflows.get(workflow_id)

    def execute_workflow(self, workflow_id: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行工作流"""
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"工作流不存在: {workflow_id}")

        # 创建上下文
        context = WorkflowContext(
            workflow_id=workflow_id,
            variables=variables or {},
        )
        workflow.context = context

        # 更新状态
        workflow.update_status(WorkflowStatus.RUNNING)

        try:
            # 执行工作流
            result = self._execute_nodes(workflow)

            # 更新状态
            workflow.update_status(WorkflowStatus.COMPLETED)

            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "result": result,
                "duration": time.time() - workflow.start_time,
            }

        except Exception as e:
            workflow.update_status(WorkflowStatus.FAILED, str(e))
            logger.error(f"工作流执行失败: {e}")
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
            }

    def _execute_nodes(self, workflow: BaseWorkflow) -> Dict[str, Any]:
        """执行所有节点"""
        context = workflow.context
        results = {}

        # 获取根节点
        root_nodes = workflow.get_root_nodes()
        if not root_nodes:
            raise ValueError("工作流没有根节点")

        # 并行执行根节点
        queue = list(root_nodes)
        visited = set()

        while queue:
            current_batch = []
            for node_id in queue:
                if node_id not in visited:
                    current_batch.append(node_id)

            if not current_batch:
                break

            # 并行执行当前批次
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self._execute_node, workflow, node_id): node_id
                    for node_id in current_batch
                }

                for future in concurrent.futures.as_completed(futures):
                    node_id = futures[future]
                    try:
                        result = future.result()
                        results[node_id] = result
                        context.set_node_result(node_id, result)
                        visited.add(node_id)

                        # 添加后继节点到队列
                        successors = workflow.get_successors(node_id)
                        for successor in successors:
                            # 检查是否所有前驱都已完成
                            predecessors = workflow.get_predecessors(successor)
                            if all(p in visited for p in predecessors):
                                queue.append(successor)

                    except Exception as e:
                        logger.error(f"节点执行失败: {node_id}, 错误: {e}")
                        results[node_id] = {"success": False, "error": str(e)}
                        context.set_node_result(node_id, {"success": False, "error": str(e)})

            queue = [n for n in queue if n not in visited]

        return results

    def _execute_node(self, workflow: BaseWorkflow, node_id: str) -> Dict[str, Any]:
        """执行单个节点"""
        node = workflow.get_node(node_id)
        if not node:
            raise ValueError(f"节点不存在: {node_id}")

        context = workflow.context
        context.current_node = node_id

        logger.info(f"执行节点: {node.name} ({node_id})")

        # 根据节点类型执行
        if node.node_type == NodeType.ACTION:
            return self._execute_action_node(node, context)
        elif node.node_type == NodeType.CONDITION:
            return self._execute_condition_node(node, context)
        elif node.node_type == NodeType.PARALLEL:
            return self._execute_parallel_node(node, context, workflow)
        elif node.node_type == NodeType.HUMAN:
            return self._execute_human_node(node, context)
        elif node.node_type == NodeType.LOOP:
            return self._execute_loop_node(node, context, workflow)
        else:
            raise ValueError(f"不支持的节点类型: {node.node_type}")

    def _execute_action_node(self, node: WorkflowNode, context: WorkflowContext) -> Dict[str, Any]:
        """执行动作节点"""
        if not node.action:
            raise ValueError(f"节点 {node.name} 没有定义动作")

        try:
            result = node.action(context)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_condition_node(self, node: WorkflowNode, context: WorkflowContext) -> Dict[str, Any]:
        """执行条件节点"""
        if not node.condition:
            raise ValueError(f"节点 {node.name} 没有定义条件")

        try:
            condition_result = node.condition(context)
            return {"success": True, "result": condition_result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_parallel_node(self, node: WorkflowNode, context: WorkflowContext,
                              workflow: BaseWorkflow) -> Dict[str, Any]:
        """执行并行节点"""
        # 获取所有并行分支
        branches = node.config.get("branches", [])
        if not branches:
            return {"success": True, "result": []}

        # 并行执行分支
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._execute_nodes, workflow): branch
                for branch in branches
            }

            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})

        return {"success": True, "result": results}

    def _execute_human_node(self, node: WorkflowNode, context: WorkflowContext) -> Dict[str, Any]:
        """执行人工审批节点"""
        approval_info = {
            "node_id": node.id,
            "node_name": node.name,
            "prompt": node.config.get("prompt", "请确认执行"),
            "options": node.config.get("options", ["approve", "reject"]),
        }

        # 在实际实现中，这里会等待人工审批
        # 目前返回待审批状态
        return {
            "success": True,
            "result": "pending_approval",
            "approval_info": approval_info,
        }

    def _execute_loop_node(self, node: WorkflowNode, context: WorkflowContext,
                          workflow: BaseWorkflow) -> Dict[str, Any]:
        """执行循环节点"""
        max_iterations = node.config.get("max_iterations", 10)
        condition = node.config.get("condition")

        results = []
        for i in range(max_iterations):
            # 检查条件
            if condition and not condition(context):
                break

            # 执行循环体
            loop_result = self._execute_nodes(workflow)
            results.append(loop_result)

            # 更新上下文
            context.set_variable(f"loop_{node.id}_iteration", i + 1)

        return {"success": True, "result": results, "iterations": len(results)}

    def pause_workflow(self, workflow_id: str):
        """暂停工作流"""
        workflow = self._workflows.get(workflow_id)
        if workflow:
            workflow.update_status(WorkflowStatus.PAUSED)

    def resume_workflow(self, workflow_id: str):
        """恢复工作流"""
        workflow = self._workflows.get(workflow_id)
        if workflow:
            workflow.update_status(WorkflowStatus.RUNNING)

    def cancel_workflow(self, workflow_id: str):
        """取消工作流"""
        workflow = self._workflows.get(workflow_id)
        if workflow:
            workflow.update_status(WorkflowStatus.CANCELLED)

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """获取工作流状态"""
        workflow = self._workflows.get(workflow_id)
        if workflow:
            return workflow.to_dict()
        return None

    def list_workflows(self) -> List[Dict[str, Any]]:
        """列出所有工作流"""
        return [
            {
                "id": wf.id,
                "name": wf.name,
                "status": wf.status.value,
            }
            for wf in self._workflows.values()
        ]
