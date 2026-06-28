"""AI 代理核心 - 安全版本"""
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 系统提示词
SYSTEM_PROMPT = """你是一位资深 SRE/DevOps 工程师，擅长运维故障排查。

重要规则：
1. 用中文回答
2. 基于数据做判断，不猜测
3. 提供具体的命令和操作建议
4. 对于危险操作，明确说明风险
5. 如果信息不足，主动询问
"""


@dataclass
class AIResponse:
    """AI 响应"""
    content: str
    success: bool = True
    error: Optional[str] = None
    usage: Optional[Dict[str, int]] = None

    @property
    def is_valid(self) -> bool:
        return self.success and bool(self.content)


class AIAgent:
    """AI 代理 - 支持多种 LLM 提供商"""

    def __init__(self, config):
        """
        初始化 AI 代理

        Args:
            config: AIConfig 实例
        """
        self.config = config
        self._client = None
        self._provider = None

    @property
    def available(self) -> bool:
        """检查 AI 是否可用"""
        return self.config.is_configured

    def _get_client(self):
        """获取 LLM 客户端"""
        if self._client is not None:
            return self._client

        if not self.available:
            raise RuntimeError("AI 未配置或 API Key 未设置")

        try:
            if self.config.provider == "deepseek":
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.config.api_key,
                    base_url=self.config.base_url,
                    timeout=self.config.timeout,
                )
                self._provider = "deepseek"

            elif self.config.provider == "openai":
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.config.api_key,
                    timeout=self.config.timeout,
                )
                self._provider = "openai"

            elif self.config.provider == "anthropic":
                try:
                    import anthropic
                    self._client = anthropic.Anthropic(
                        api_key=self.config.api_key,
                        timeout=self.config.timeout,
                    )
                    self._provider = "anthropic"
                except ImportError:
                    raise RuntimeError("未安装 anthropic 库: pip install anthropic")

            elif self.config.provider == "openrouter":
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.config.api_key,
                    base_url="https://openrouter.ai/api/v1",
                    timeout=self.config.timeout,
                )
                self._provider = "openrouter"

            else:
                # 默认使用 OpenAI 兼容接口
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.config.api_key,
                    base_url=self.config.base_url,
                    timeout=self.config.timeout,
                )
                self._provider = "openai_compatible"

            logger.info(f"AI 客户端初始化成功: provider={self._provider}")
            return self._client

        except ImportError as e:
            logger.error(f"导入 AI 库失败: {e}")
            raise RuntimeError(f"未安装 {self.config.provider} 库: {e}")

        except Exception as e:
            logger.error(f"AI 客户端初始化失败: {e}")
            raise RuntimeError(f"AI 客户端初始化失败: {e}")

    def analyze(self, data: str, question: Optional[str] = None,
                system_prompt: Optional[str] = None) -> AIResponse:
        """
        分析数据并回答问题

        Args:
            data: 要分析的数据
            question: 问题（可选）
            system_prompt: 自定义系统提示词（可选）

        Returns:
            AIResponse
        """
        if not self.available:
            return AIResponse(
                content="",
                success=False,
                error="AI 未配置，请检查配置文件"
            )

        try:
            client = self._get_client()

            # 构建消息
            messages = [
                {"role": "system", "content": system_prompt or SYSTEM_PROMPT},
            ]

            # 构建用户消息
            user_content = f"服务器数据:\n{data}"
            if question:
                user_content += f"\n\n问题: {question}"
            messages.append({"role": "user", "content": user_content})

            # 调用 API
            logger.debug(f"调用 AI API: provider={self._provider}, model={self.config.model}")

            if self._provider == "anthropic":
                response = client.messages.create(
                    model=self.config.model,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    messages=messages[1:],  # Anthropic 不支持 system 消息在 messages 中
                    system=messages[0]["content"],
                )
                content = response.content[0].text
                usage = {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                }
            else:
                response = client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                )
                content = response.choices[0].message.content
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                }

            logger.info(f"AI 响应成功: content_len={len(content)}")
            return AIResponse(content=content, usage=usage)

        except Exception as e:
            error_msg = f"AI 分析失败: {e}"
            logger.error(error_msg)
            return AIResponse(content="", success=False, error=error_msg)

    def triage(self, symptoms: str, data: Optional[str] = None) -> AIResponse:
        """
        事件分诊

        Args:
            symptoms: 事件症状
            data: 相关数据

        Returns:
            AIResponse
        """
        prompt = f"""请对以下运维事件进行分诊：

事件症状: {symptoms}

请提供：
1. 严重程度评估 (P0/P1/P2/P3)
2. 可能的原因
3. 建议的排查步骤
4. 需要关注的指标
"""
        return self.analyze(data or "暂无数据", prompt)

    def suggest_fix(self, problem: str, context: Optional[str] = None) -> AIResponse:
        """
        建议修复方案

        Args:
            problem: 问题描述
            context: 上下文信息

        Returns:
            AIResponse
        """
        prompt = f"""请提供以下问题的修复方案：

问题: {problem}

请提供：
1. 根本原因分析
2. 临时缓解措施
3. 永久修复方案
4. 验证步骤
5. 预防措施
"""
        return self.analyze(context or "暂无上下文", prompt)

    def explain_log(self, log_content: str, question: Optional[str] = None) -> AIResponse:
        """
        解释日志内容

        Args:
            log_content: 日志内容
            question: 问题

        Returns:
            AIResponse
        """
        prompt = f"""请分析以下日志内容：

```
{log_content[:2000]}
```

请提供：
1. 日志摘要
2. 关键错误信息
3. 可能的原因
4. 建议的操作
"""
        if question:
            prompt += f"\n\n具体问题: {question}"

        return self.analyze("", prompt)
