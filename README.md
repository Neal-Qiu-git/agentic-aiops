# Agentic AIOps

<div align="center">

🤖 **AI-native Operations Platform**

*Not another AI Agent. An autonomous operations system that diagnoses, fixes, verifies, and learns.*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-4.0-orange.svg?style=flat-square)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)]()
[![K8s](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes&logoColor=white)]()
[![MCP](https://img.shields.io/badge/MCP-20%2B_Tools-FF6B35?style=flat-square)]()
[![Stars](https://img.shields.io/github/stars/neal4752/agentic-aiops?style=flat-square)]()

[English](README_EN.md) | 中文 | [Docs](docs/) | [Examples](examples/)

</div>

---

## What is Agentic AIOps?

**Agentic AIOps** is an AI-native operations platform that combines Multi-Agent collaboration, Memory, Knowledge, Workflow, Event Bus, and Human Approval into a unified operational system.

> **It's not another AI Agent — it's an autonomous operations platform.**

| Framework | Purpose | MCP | Memory | Workflow | Approval |
|-----------|---------|:---:|:------:|:--------:|:--------:|
| LangGraph | General Agent | ❌ | ✅ | ✅ | ❌ |
| CrewAI | General Agent | ❌ | ❌ | ❌ | ❌ |
| AutoGPT | General Agent | ❌ | ❌ | ❌ | ❌ |
| OpenHands | Dev Agent | ❌ | ❌ | ❌ | ❌ |
| **Agentic AIOps** | **Ops Agent** | ✅ | ✅ | ✅ | ✅ |

---

## ✨ Features

- 🤖 **12 Specialized Agents** — Linux, K8s, DB, Log, Monitor, Security, SRE, Cost, Incident, DevOps, CMDB, Planner
- 🔄 **ReAct Lifecycle** — Observe → Reason → Plan → Act → Verify → Learn
- 🔌 **MCP Marketplace** — 20+ tools, plugin architecture
- 🧠 **5-Type Memory** — Working, Short-term, Long-term, Semantic, Episodic
- 📚 **Knowledge RAG** — Runbooks, docs, historical cases
- ⚡ **Event Bus** — Decoupled agent collaboration
- 🚦 **Workflow Engine** — YAML-based automation
- 👤 **Human Approval** — Risk-based workflow approval
- 📡 **REST API** — OpenAPI specification
- 🖥️ **CLI** — Full-featured command line

---

## 📸 Demo

```
$ aiops diagnose --host 10.0.0.1 --symptom "服务响应慢"

[08:32:01] 🔍 OBSERVE    CPU 95%, Memory 87%, Load 8.2
[08:32:02] 🧠 REASON     High CPU, analyzing processes
[08:32:03] 📋 PLAN       check_top → check_process → check_gc
[08:32:04] ⚡ ACTION     $ top -bn1 | head -20
[08:32:05] ⚡ ACTION     $ ps aux --sort=-%cpu | head -10
[08:32:06] ⚡ ACTION     $ jstat -gc 12345
[08:32:07] ✅ VERIFY     Java GC consuming 80% CPU
[08:32:08] 📝 LEARN      Incident recorded to knowledge base

╔═══════════════════════════════════════════════════════════╗
║  Root Cause:  Java Full GC triggered by memory pressure  ║
║  Confidence:  94%                                         ║
║  Fix:         Increase JVM heap -Xmx4g → 8g             ║
╚═══════════════════════════════════════════════════════════╝
```

> 📹 **[Watch Full Demo Video](docs/demo.md)**

---

## 🏗️ Architecture

```
                         ┌─────────────────────┐
                         │      User Layer     │
                         │  CLI │ API │ Chat   │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │     Event Bus       │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │   Planner Agent     │
                         └──────────┬──────────┘
                                    │
       ┌──────────┬────────┬────────┼────────┬──────────┐
       │          │        │        │        │          │
       ▼          ▼        ▼        ▼        ▼          ▼
   ┌──────┐   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
   │Linux │   │ K8s  │ │  DB  │ │ Log  │ │Monit │ │Secur │
   │Agent │   │Agent │ │Agent │ │Agent │ │Agent │ │Agent │
   └──────┘   └──────┘ └──────┘ └──────┘ └──────┘ └──────┘
       │          │        │        │        │          │
       └──────────┴────────┴────┬───┴────────┴──────────┘
                                │
                     ┌──────────▼──────────┐
                     │   MCP Marketplace   │
                     └──────────┬──────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Memory │ Knowledge  │
                     └─────────────────────┘
```

📖 **[详细架构文档](docs/architecture.md)**

---

## 📊 Support Matrix

| Platform | Database | Monitoring | Cloud |
|----------|----------|------------|-------|
| Linux ✅ | MySQL ✅ | Prometheus ✅ | AWS ✅ |
| Docker ✅ | Redis ✅ | Grafana ✅ | Aliyun ✅ |
| K8s ✅ | PostgreSQL ✅ | Loki 🚧 | Tencent ✅ |
| | MongoDB ✅ | | |
| | Elasticsearch ✅ | | |

---

## ⚡ Quick Start

```bash
# Install
pip install agentic-aiops

# Configure
export AIOPS_AI_API_KEY=your-key

# Run
aiops diagnose --host 10.0.0.1 --symptom "CPU 高"
```

### Docker

```bash
docker run -it --rm -e AIOPS_AI_API_KEY=your-key agentic-aiops
```

### Kubernetes

```bash
helm install aiops ./charts/agentic-aiops --set ai.apiKey=your-key
```

📖 **[完整安装文档](docs/installation.md)**

---

## 🤖 Supported Agents

| Agent | Description | Status |
|-------|-------------|:------:|
| 🐧 Linux | System diagnostics | ✅ |
| ☸️ K8s | Kubernetes operations | ✅ |
| 🗄️ DB | Database diagnostics | ✅ |
| 📋 Log | Log analysis | ✅ |
| 📊 Monitor | Monitoring analysis | ✅ |
| 🔒 Security | Security scanning | ✅ |
| 🏥 SRE | SLI/SLO/Error Budget | ✅ |
| 💰 Cost | Cost optimization | ✅ |
| 🚨 Incident | Incident management | ✅ |
| 🚀 DevOps | CI/CD operations | ✅ |

---

## 🤖 Supported LLM

| Provider | Models |
|----------|--------|
| DeepSeek | deepseek-chat |
| OpenAI | gpt-4o, gpt-4-turbo |
| Anthropic | claude-3-opus, claude-3-sonnet |
| Qwen | qwen-max, qwen-plus |
| Ollama | llama3, mistral |
| OpenRouter | Multiple models |

---

## 🗺️ Roadmap

### v1.x — Foundation ✅

- [x] Core Agents (Linux, K8s, DB)
- [x] CLI Interface
- [x] MCP Tool System
- [x] Basic Memory

### v2.x — Intelligence ✅

- [x] Memory System (5 types)
- [x] Knowledge Base
- [x] Workflow Engine
- [x] Approval System

### v3.x — Platform 🚧

- [ ] Web Dashboard
- [ ] Workflow Designer
- [ ] Plugin Marketplace
- [ ] REST API Enhancement

### v4.x — Enterprise 📋

- [ ] Multi-Cluster Support
- [ ] RBAC
- [ ] Audit Log
- [ ] High Availability

### v5.x — Cloud Native 📋

- [ ] Voice Agent
- [ ] Auto-Remediation
- [ ] Self-Healing Systems

---

## 🏢 Enterprise Features

- 🔐 **RBAC** — Role-based access control
- 📋 **Audit Log** — Complete operation history
- ✅ **Approval** — Risk-based workflow approval
- 🔔 **Webhook** — Feishu, DingTalk, Slack, Email
- 🔌 **Plugin** — Extensible architecture
- 📡 **REST API** — OpenAPI specification
- 🌐 **Multi-Cluster** — Cross-cluster management
- 🔄 **High Availability** — HA deployment

---

## 📚 Documentation

- [Architecture](docs/architecture.md)
- [Installation](docs/installation.md)
- [Agents](docs/agents.md)
- [Workflow](docs/workflow.md)
- [Memory](docs/memory.md)
- [Knowledge](docs/knowledge.md)
- [Approval](docs/approval.md)
- [MCP Tools](docs/mcp.md)
- [Security](docs/security.md)
- [API](docs/api.md)
- [FAQ](docs/faq.md)
- [ADR](docs/adr/)

---

## 📁 Examples

| Example | Description |
|---------|-------------|
| [cpu-high](examples/cpu-high/) | CPU usage diagnosis |
| [memory-leak](examples/memory-leak/) | Memory leak detection |
| [pod-crash](examples/pod-crash/) | K8s Pod troubleshooting |
| [redis-timeout](examples/redis-timeout/) | Redis connection issues |
| [mysql-slow](examples/mysql-slow/) | MySQL slow query analysis |
| [disk-full](examples/disk-full/) | Disk space diagnosis |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

[![Contributors](https://contrib.rocks/image?repo=neal4752/agentic-aiops)]()

---

## 📄 License

[MIT License](LICENSE)

---

<div align="center">

**If this project is helpful, please give it a ⭐ Star!**

</div>
