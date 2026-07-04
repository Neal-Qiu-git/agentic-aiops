"""SRE Agent - SLI/SLO/Error Budget"""
from .base import BaseAgent, AgentResult


class SREAgent(BaseAgent):
    """SRE Agent - 负责 SLI/SLO/Error Budget 管理"""

    name = "sre"
    description = "SRE Agent - SLI/SLO/Error Budget 管理"
    role = "SRE"
    task_description = "负责 SLI/SLO/Error Budget 管理和可用性分析"
    tools = ["ssh_exec", "prometheus_query"]
    max_steps = 10

    def run(self, task: str, context: dict = None) -> AgentResult:
        """执行 SRE 任务"""
        context = context or {}

        # 构建分析请求
        prompt = f"""作为 SRE 专家，请分析以下任务：

任务: {task}

请提供：
1. SLI 指标分析
2. SLO 达标情况
3. Error Budget 消耗
4. 可用性评估
5. 建议措施
"""
        return super().run(prompt, context)
