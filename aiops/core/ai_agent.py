"""AI 代理核心"""
SYSTEM_PROMPT = "你是一位资深 SRE/DevOps 工程师，擅长运维故障排查。用中文回答。"

class AIAgent:
    def __init__(self, config):
        self.config = config; self._client = None

    @property
    def available(self): return self.config.enabled and bool(self.config.api_key)

    def analyze(self, data, question=None):
        if not self._client:
            if not self.available: raise RuntimeError("AI 未配置")
            from openai import OpenAI
            self._client = OpenAI(api_key=self.config.api_key, base_url=self.config.base_url)
        msg = f"服务器数据:\n{data}"
        if question: msg += f"\n问题: {question}"
        resp = self._client.chat.completions.create(model=self.config.model,
            messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":msg}])
        return resp.choices[0].message.content

    def triage(self, symptoms, data=None): return self.analyze(data or "暂无数据", f"事件症状: {symptoms}")
