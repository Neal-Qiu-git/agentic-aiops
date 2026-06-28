# Agentic AIOps

<div align="center">

🤖 **AI Native Autonomous Operations Platform**

*Let AI not only analyze, but truly complete operations work*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.1-orange.svg)]()

English | [中文](README.md)

</div>

---

## What is Agentic AIOps?

**Agentic AIOps** is a next-generation AI operations platform built on **LLM + ReAct + MCP + Multi-Agent**.

```
Traditional AIOps: Alert → Human Processing

Agentic AIOps:
AI Analysis → AI Planning → AI Execution → AI Verification → AI Learning
```

> **AI can independently complete a full operations loop.**

---

## Key Features

| Feature | Description |
|---------|-------------|
| 🔄 **Agent Lifecycle** | Observe → Reason → Plan → Act → Verify → Learn |
| 🧠 **Memory System** | Short/Long/Semantic/Episodic memory, continuous learning |
| 📚 **Knowledge + RAG** | Runbook, docs, historical cases intelligent retrieval |
| ⚡ **Event Driven** | Event-driven Multi-Agent collaboration |
| 🔧 **MCP Marketplace** | Plugin tool marketplace, 20+ tools |
| 🚦 **Workflow Engine** | YAML orchestration, visual operations flow |
| 👤 **Human Approval** | High-risk operation approval, Webhook/Slack/Teams |

---

## Quick Start

```bash
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
pip install -e .

aiops diagnose --host 10.0.0.1 --symptom "high CPU"
```

---

## Documentation

- [Installation](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Agents](docs/agents.md)
- [API Reference](docs/api.md)

---

## License

[MIT License](LICENSE)
