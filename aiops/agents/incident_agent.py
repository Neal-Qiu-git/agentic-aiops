"""Incident Agent - 故障管理"""
from .base import BaseAgent, AgentResult


class IncidentAgent(BaseAgent):
    """Incident Agent - 负责故障事件管理"""

    name = "incident"
    description = "Incident Agent - 故障事件管理"
    role = "故障管理专家"
    task_description = "负责故障检测、响应、Timeline 生成和 RCA 报告"
    tools = ["ssh_exec", "k8s_get_events", "k8s_get_pods"]
    max_steps = 15

    def run(self, task: str, context: dict = None) -> AgentResult:
        """执行故障管理任务"""
        context = context or {}

        prompt = f"""作为故障管理专家，请处理以下事件：

任务: {task}

请提供：
1. 故障分类（P0/P1/P2/P3）
2. 影响范围评估
3. Timeline 生成
4. 根因分析
5. 修复建议
6. 复盘报告
"""
        return super().run(prompt, context)
