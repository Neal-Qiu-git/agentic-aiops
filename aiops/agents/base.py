"""BaseAgent - ReAct 循环核心"""
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ToolCall:
    """工具调用"""
    name: str
    args: dict
    call_id: str = ""


@dataclass
class AgentResult:
    """Agent 执行结果"""
    answer: str
    steps: list = field(default_factory=list)
    tool_calls: list = field(default_factory=list)
    success: bool = True
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "answer": self.answer, "steps": self.steps,
            "tool_calls": self.tool_calls, "success": self.success,
            "metadata": self.metadata,
        }


@dataclass
class AgentStep:
    """Agent 执行步骤"""
    thought: str = ""
    action: str = ""
    action_input: dict = field(default_factory=dict)
    observation: str = ""
    step_type: str = "thought"  # thought, action, observation, final


SYSTEM_PROMPT_TEMPLATE = """你是一个专业的 {role} Agent。
你的任务是：{task_description}

你可以使用以下工具：
{tools_description}

请按照 ReAct 模式思考和行动：
1. Thought: 分析当前情况，决定下一步
2. Action: 选择要执行的工具
3. Observation: 查看工具返回结果
4. 重复直到得出最终结论

重要规则：
- 每次只执行一个工具调用
- 基于数据做判断，不猜测
- 如果工具执行失败，尝试替代方案
- 最终给出明确的结论和建议
"""


class BaseAgent(ABC):
    """Agent 基类 - 实现 ReAct 循环"""

    name: str = "base"
    description: str = ""
    role: str = "运维"
    task_description: str = "处理运维任务"
    tools: list = field(default_factory=list)  # 可用工具名列表
    max_steps: int = 15

    def __init__(self, ai_client=None, tool_registry=None):
        self.ai = ai_client
        self.tool_registry = tool_registry
        self._messages = []
        self._steps = []
        self._tool_calls_log = []

    def run(self, task: str, context: dict = None) -> AgentResult:
        """执行 ReAct 循环"""
        context = context or {}
        self._steps = []
        self._tool_calls_log = []

        # 构建系统提示
        tools_desc = self._get_tools_description()
        system = SYSTEM_PROMPT_TEMPLATE.format(
            role=self.role, task_description=self.task_description,
            tools_description=tools_desc,
        )

        self._messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": f"任务: {task}\n\n上下文: {json.dumps(context, ensure_ascii=False, default=str)[:2000]}"},
        ]

        for step_num in range(self.max_steps):
            # 调用 LLM
            response = self._call_llm()

            if not response:
                return AgentResult(answer="LLM 调用失败", success=False, steps=self._steps)

            # 检查是否有工具调用
            tool_calls = self._extract_tool_calls(response)

            if tool_calls:
                # 执行工具
                for tc in tool_calls:
                    obs = self._execute_tool(tc.name, tc.args)
                    self._steps.append(AgentStep(
                        action=tc.name, action_input=tc.args, observation=obs, step_type="action"
                    ))
                    self._messages.append({"role": "tool", "content": obs, "tool_call_id": tc.call_id})
            else:
                # 最终回答
                answer = self._extract_answer(response)
                self._steps.append(AgentStep(thought=answer, step_type="final"))
                return AgentResult(
                    answer=answer, steps=[s.__dict__ for s in self._steps],
                    tool_calls=self._tool_calls_log, success=True,
                )

        # 超过最大步数
        return AgentResult(
            answer="达到最大执行步数，未得出最终结论",
            steps=[s.__dict__ for s in self._steps],
            tool_calls=self._tool_calls_log, success=False,
        )

    def _call_llm(self) -> Optional[dict]:
        """调用 LLM"""
        if not self.ai or not self.ai.available:
            return None
        try:
            client = self.ai._get_client()
            tools = self._get_tool_schemas()
            resp = client.chat.completions.create(
                model=self.ai.config.model,
                messages=self._messages,
                tools=tools if tools else None,
                temperature=0.2,
                max_tokens=4096,
            )
            return resp.choices[0].message
        except Exception as e:
            return None

    def _extract_tool_calls(self, response) -> list:
        """从 LLM 响应中提取工具调用"""
        if not hasattr(response, 'tool_calls') or not response.tool_calls:
            return []
        calls = []
        for tc in response.tool_calls:
            args = tc.function.arguments
            if isinstance(args, str):
                try: args = json.loads(args)
                except: args = {}
            calls.append(ToolCall(name=tc.function.name, args=args, call_id=tc.id))
        return calls

    def _extract_answer(self, response) -> str:
        """提取最终回答"""
        if hasattr(response, 'content') and response.content:
            return response.content
        return str(response)

    def _execute_tool(self, name: str, args: dict) -> str:
        """执行工具并记录"""
        if not self.tool_registry:
            return f"工具 {name} 未注册"
        try:
            result = self.tool_registry.execute(name, args)
            self._tool_calls_log.append({"tool": name, "args": args, "result": result[:500]})
            return result
        except Exception as e:
            return f"工具执行失败: {e}"

    def _get_tools_description(self) -> str:
        """获取工具描述"""
        if not self.tool_registry:
            return "无可用工具"
        desc = []
        for name in self.tools:
            tool = self.tool_registry.get(name)
            if tool:
                desc.append(f"- {name}: {tool.description}")
        return "\n".join(desc) if desc else "无可用工具"

    def _get_tool_schemas(self) -> list:
        """获取工具 JSON Schema"""
        if not self.tool_registry:
            return []
        schemas = []
        for name in self.tools:
            tool = self.tool_registry.get(name)
            if tool:
                schemas.append({
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    }
                })
        return schemas

    def _delegate(self, agent_name: str, task: str, context: dict = None) -> AgentResult:
        """委派任务给其他 Agent"""
        if not self.tool_registry:
            return AgentResult(answer="无法委派: tool_registry 未配置", success=False)
        # 通过 tool_registry 调用 agent
        return self.tool_registry.execute_agent(agent_name, task, context or {})
