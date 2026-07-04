"""Cost Agent - 云成本优化"""
from .base import BaseAgent, AgentResult


class CostAgent(BaseAgent):
    """Cost Agent - 负责云成本优化"""

    name = "cost"
    description = "Cost Agent - 云成本优化"
    role = "成本优化专家"
    task_description = "负责云资源成本分析和优化建议"
    tools = ["ssh_exec", "aws_cli", "aliyun_cli", "tencent_cli"]
    max_steps = 10

    def run(self, task: str, context: dict = None) -> AgentResult:
        """执行成本优化任务"""
        context = context or {}

        prompt = f"""作为云成本优化专家，请分析以下任务：

任务: {task}

请提供：
1. 当前成本分析
2. 闲置资源识别
3. 优化建议
4. 预计节省
5. 实施步骤
"""
        return super().run(prompt, context)
