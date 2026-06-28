"""AICopilot - 运维问答助手"""
from .base import BaseAgent, AgentResult


COPILOT_SYSTEM = """你是一个 AI 运维助手（AICopilot），帮助用户：
1. 生成 Linux/K8s/Docker/SQL/PromQL 命令
2. 解答运维问题
3. 推荐排查步骤

规则：
- 直接给出可执行的命令
- 解释每个命令的作用
- 如果需要执行，询问用户是否确认
- 用中文回答
"""


class AICopilot(BaseAgent):
    name = "copilot"
    description = "AI 运维问答助手 - 生成命令和解答问题"
    role = "AI 运维助手"
    task_description = "回答运维问题，生成命令，推荐排查步骤"
    tools = ["ssh_exec"]  # 可选：直接执行命令
    max_steps = 5

    def run(self, task, context=None):
        context = context or {}
        context["copilot_mode"] = True
        # Copilot 模式：优先回答问题，不主动执行
        return super().run(task, context)
