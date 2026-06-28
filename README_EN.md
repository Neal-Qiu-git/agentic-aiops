# Agentic AIOps

<div align="center">

🤖 **AI Native Autonomous Operations Platform**

*An Autonomous Operations Platform powered by LLM, Multi-Agent and MCP for Linux, Kubernetes, Cloud and Database Operations*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.1-orange.svg?style=flat-square)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)]()
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes&logoColor=white)]()
[![MCP](https://img.shields.io/badge/MCP-Supported-FF6B35?style=flat-square)]()
[![ReAct](https://img.shields.io/badge/ReAct-Agent-9B59B6?style=flat-square)]()
[![Multi-Agent](https://img.shields.io/badge/Multi--Agent-E74C3C?style=flat-square)]()

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

## ✨ Why Agentic AIOps?

| Feature | Traditional AIOps | Agentic AIOps |
|---------|:-----------------:|:-------------:|
| Root Cause Analysis | ✅ | ✅ |
| Auto Fix | ❌ | ✅ |
| Multi-Agent | ❌ | ✅ |
| Memory | ❌ | ✅ |
| Knowledge Base | ❌ | ✅ |
| Human Approval | ❌ | ✅ |
| Workflow | ❌ | ✅ |
| Event Bus | ❌ | ✅ |
| Plugin System | ❌ | ✅ |

---

## 🧠 Core Design Principles

1. **Planner-driven** — All tasks are decomposed by PlannerAgent before execution
2. **Tool-first** — All capabilities abstracted via MCP Tools
3. **Memory-native** — Every execution learns and forms long-term experience
4. **Human-in-the-loop** — High-risk operations require approval
5. **Event-driven** — All Agents collaborate via Event Bus

---

## 🤖 Supported Agents

| Agent | Description | Status |
|-------|-------------|:------:|
| 🐧 Linux Agent | System operations | ✅ |
| ☸️ K8s Agent | Kubernetes operations | ✅ |
| 🗄️ DB Agent | Database operations | ✅ |
| 📋 Log Agent | Log analysis | ✅ |
| 📊 Monitor Agent | Monitoring analysis | ✅ |
| 🔒 Security Agent | Security operations | ✅ |
| 🚀 DevOps Agent | CI/CD operations | ✅ |
| 🏥 SRE Agent | SRE operations | ✅ |
| 🚨 Incident Agent | Incident management | ✅ |
| 💰 Cost Agent | Cost optimization | ✅ |

---

## 📊 Support Matrix

### Platforms

| Platform | Support |
|----------|:-------:|
| Linux | ✅ |
| Docker | ✅ |
| Kubernetes | ✅ |
| AWS | ✅ |
| Aliyun | ✅ |
| Tencent | ✅ |

### Databases

| Database | Support |
|----------|:-------:|
| MySQL | ✅ |
| Redis | ✅ |
| PostgreSQL | ✅ |
| MongoDB | ✅ |
| Elasticsearch | ✅ |
| Kafka | ✅ |

---

## ⚡ Quick Start

```bash
# Install
pip install agentic-aiops

# Configure
cp config.example.yaml config.yaml
export AIOPS_AI_API_KEY="your-api-key"

# Run
aiops diagnose --host 10.0.0.1 --symptom "high CPU"
```

---

## 🏢 Enterprise Features

- 🔐 RBAC
- 📋 Audit Log
- ✅ Approval Workflow
- 🔔 Webhook Integration
- 🔌 Plugin System
- 📡 REST API
- 🔄 High Availability

---

## 🗺️ Roadmap

- **v1.x**: Core Agents, CLI
- **v2.x**: Memory, Knowledge, Workflow, Approval
- **v3.x**: Dashboard, Plugin Marketplace, Voice Agent

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

[MIT License](LICENSE)
