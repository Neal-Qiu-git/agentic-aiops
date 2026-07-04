# Agentic AIOps

<div align="center">

🤖 **AI-native Operations Platform**

*Purpose-built for SRE, DevOps, and Cloud Native automation*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.2-orange.svg?style=flat-square)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)]()
[![K8s](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes&logoColor=white)]()
[![MCP](https://img.shields.io/badge/MCP-20%2B_Tools-FF6B35?style=flat-square)]()

English | [中文](README.md)

</div>

---

## Why Agentic AIOps?

Generic AI Agent frameworks are not built for operations.

**Agentic AIOps is purpose-built for:**

- 🐧 Linux — System diagnostics and troubleshooting
- ☸️ Kubernetes — Container orchestration management
- 🗄️ Database — MySQL, Redis, PostgreSQL, MongoDB
- 📊 Monitoring — Prometheus, Grafana analysis
- ☁️ Cloud — AWS, Aliyun, Tencent
- 🔒 Security — Vulnerability scanning, compliance

---

## ✨ Features

- 🤖 **12 Specialized Agents**
- 🔄 **ReAct Reasoning**
- 🔌 **MCP Tool Calling** — 20+ tools
- 🧠 **Operational Memory**
- 📚 **Knowledge RAG**
- ⚡ **Event Bus**
- 🚦 **Workflow Engine**
- 👤 **Human Approval**

---

## 📸 Demo

```bash
$ aiops diagnose --host 10.0.0.1 --symptom "high CPU"

[08:32:01] 🔍 OBSERVE    CPU 95%, Memory 87%
[08:32:02] 🧠 REASON     Analyzing processes
[08:32:03] 📋 PLAN       check_top → check_process → check_gc
[08:32:04] ⚡ ACTION     $ top -bn1 | head -20
[08:32:05] ✅ VERIFY     Java GC consuming 80% CPU
[08:32:06] 📝 LEARN      Recorded to knowledge base

Root Cause: Java Full GC
Fix: Increase JVM heap -Xmx4g → 8g
```

---

## 🏗️ Architecture

```
                    User (CLI/API)
                         │
                    Event Bus
                         │
                   Planner Agent
                         │
    ┌────────┬───────┬───┴───┬───────┬────────┐
    │        │       │       │       │        │
  Linux    K8s      DB     Log   Monitor  Security
  Agent    Agent   Agent  Agent   Agent    Agent
    │        │       │       │       │        │
    └────────┴───────┴───┬───┴───────┴────────┘
                         │
                  MCP Marketplace
                         │
               Memory │ Knowledge │ RAG
```

---

## ⚡ Quick Start

```bash
# Install
pip install agentic-aiops

# Configure
export AIOPS_AI_API_KEY=your-key

# Run
aiops diagnose --host 10.0.0.1 --symptom "high CPU"
```

### Docker

```bash
docker run -it agentic-aiops aiops diagnose --help
```

### Kubernetes

```bash
helm install aiops ./charts/agentic-aiops
```

---

## 🤖 Supported Agents

| Agent | Description | Status |
|-------|-------------|:------:|
| Linux Agent | System operations | ✅ |
| K8s Agent | Kubernetes operations | ✅ |
| DB Agent | Database operations | ✅ |
| Log Agent | Log analysis | ✅ |
| Monitor Agent | Monitoring | ✅ |
| Security Agent | Security | ✅ |
| SRE Agent | SRE operations | ✅ |
| Cost Agent | Cost optimization | ✅ |

---

## 🤖 Supported LLM

- DeepSeek
- OpenAI (GPT-4)
- Anthropic (Claude)
- Qwen
- Ollama
- OpenRouter

---

## 📊 Support Matrix

| Platform | Database | Monitoring |
|----------|----------|------------|
| Linux ✅ | MySQL ✅ | Prometheus ✅ |
| Docker ✅ | Redis ✅ | Grafana ✅ |
| K8s ✅ | PostgreSQL ✅ | Loki 🚧 |
| AWS ✅ | MongoDB ✅ | |
| Aliyun ✅ | Elasticsearch ✅ | |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

[MIT License](LICENSE)
