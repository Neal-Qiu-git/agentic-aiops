"""CMDB Agent - 配置管理"""
from .base import BaseAgent, AgentResult


class CMDBAgent(BaseAgent):
    """CMDB Agent - 负责配置管理"""

    name = "cmdb"
    description = "CMDB Agent - 配置管理"
    role = "配置管理专家"
    task_description = "负责资产发现、依赖关系分析和影响评估"
    tools = ["ssh_exec", "k8s_get_pods", "k8s_get_nodes"]
    max_steps = 10

    def run(self, task: str, context: dict = None) -> AgentResult:
        """执行配置管理任务"""
        context = context or {}

        prompt = f"""作为配置管理专家，请分析以下任务：

任务: {task}

请提供：
1. 资产发现
2. 依赖关系分析
3. 影响评估
4. 变更建议
5. 风险评估
"""
        return super().run(prompt, context)
