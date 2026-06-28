# Agentic AIOps

<div align="center">

🤖 **AI-native Operations Platform**

*Purpose-built for SRE, DevOps, and Cloud Native automation. Not another generic AI Agent framework.*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.2-orange.svg?style=flat-square)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)]()
[![K8s](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes&logoColor=white)]()
[![MCP](https://img.shields.io/badge/MCP-20%2B_Tools-FF6B35?style=flat-square)]()

[English](README_EN.md) | 中文

</div>

---

## Why Agentic AIOps?

Generic AI Agent frameworks (LangGraph, AutoGPT, CrewAI) are not built for operations.

**Agentic AIOps is purpose-built for:**

- 🐧 **Linux** — CPU, memory, disk, network, process troubleshooting
- ☸️ **Kubernetes** — Pod, Deployment, Service, Node diagnostics
- 🗄️ **Database** — MySQL, Redis, PostgreSQL, MongoDB performance
- 📊 **Monitoring** — Prometheus, Grafana alert analysis
- ☁️ **Cloud** — AWS, Aliyun, Tencent resource management
- 🔒 **Security** — Vulnerability scanning, compliance checks

**Unlike generic frameworks:**

| Capability | Generic Agent | Agentic AIOps |
|------------|:-------------:|:-------------:|
| Linux Diagnostics | ❌ | ✅ 100+ commands |
| K8s Operations | ❌ | ✅ 40+ operations |
| Database Analysis | ❌ | ✅ 20+ diagnostics |
| Runbook Execution | ❌ | ✅ 50+ runbooks |
| Incident Management | ❌ | ✅ Full lifecycle |
| Memory & Learning | Basic | ✅ Operational experience |
| Human Approval | ❌ | ✅ Risk-based |

---

## ✨ Features

- 🤖 **12 Specialized Agents** — Linux, K8s, DB, Log, Monitor, Security, DevOps, SRE, Incident, Cost, CMDB, Planner
- 🔄 **ReAct Reasoning** — Observe → Reason → Plan → Act → Verify → Learn
- 🔌 **MCP Tool Calling** — 20+ tools, plugin architecture
- 🧠 **Operational Memory** — Learn from every incident
- 📚 **Knowledge RAG** — Runbooks, docs, historical cases
- ⚡ **Event Bus** — Decoupled agent collaboration
- 🚦 **Workflow Engine** — YAML-based automation
- 👤 **Human Approval** — Risk-based approval workflow
- 📡 **REST API** — OpenAPI specification
- 🖥️ **CLI Interface** — Full-featured command line

---

## 📸 Demo

```bash
$ aiops diagnose --host 10.0.0.1 --symptom "服务响应慢"

[08:32:01] 🔍 OBSERVE    CPU 95%, Memory 87%, Load 8.2
[08:32:02] 🧠 REASON     High CPU detected, analyzing processes
[08:32:03] 📋 PLAN       Task: check_top → check_process → check_gc
[08:32:04] ⚡ ACTION     $ top -bn1 | head -20
[08:32:05] ⚡ ACTION     $ ps aux --sort=-%cpu | head -10
[08:32:06] ⚡ ACTION     $ jstat -gc 12345
[08:32:07] ✅ VERIFY     Java process GC consuming 80% CPU
[08:32:08] 📝 LEARN      Incident recorded to knowledge base

╔═══════════════════════════════════════════════════════════════════╗
║  DIAGNOSIS REPORT                                                ║
╠═══════════════════════════════════════════════════════════════════╣
║  Root Cause:  Java Full GC triggered by memory pressure          ║
║  Evidence:    GC threads consuming 80% CPU                       ║
║  Confidence:  94%                                                 ║
║  Fix:         Increase JVM heap -Xmx4g → 8g                     ║
║  Command:     sed -i 's/-Xmx4g/-Xmx8g/' /etc/app/jvm.conf      ║
╚═══════════════════════════════════════════════════════════════════╝
```

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
                              │  Pub/Sub Messaging  │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   Planner Agent     │
                              │  Task Decomposition │
                              └──────────┬──────────┘
                                         │
        ┌──────────┬──────────┬──────────┼──────────┬──────────┐
        │          │          │          │          │          │
        ▼          ▼          ▼          ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │ Linux  │ │  K8s   │ │   DB   │ │  Log   │ │Monitor │ │Security│
   │ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │
   └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
        │          │          │          │          │          │
        └──────────┴──────────┴─────┬────┴──────────┴──────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │       MCP Marketplace       │
                     │  20+ Tools │ Plugin System  │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │   Memory │ Knowledge │ RAG   │
                     └─────────────────────────────┘
```

---

## 🔄 Workflow Execution

```
Prometheus Alert: CPU > 90%
         │
         ▼
┌─────────────────────────────────────────────────────┐
│                   Event Bus                         │
│         metric.alert: cpu_high                      │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                Planner Agent                        │
│         Analyze alert, create plan                  │
└───────────────────────┬─────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │ Linux   │   │  Log    │   │Monitor  │
    │ Agent   │   │ Agent   │   │ Agent   │
    └─────────┘   └─────────┘   └─────────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │Result Aggregation│
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │   Auto Fix      │
              │ (if approved)   │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │   Verification  │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │   Memory        │
              │   + Knowledge   │
              └─────────────────┘
```

---

## 🧠 Agent Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                        IDLE                                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Event received
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OBSERVING                                   │
│            Collect metrics, logs, events                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REASONING                                   │
│            LLM analyzes root cause                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PLANNING                                    │
│            Decompose into actionable steps                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXECUTING                                   │
│            MCP Tool calls, command execution                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
┌──────────────────────┐     ┌──────────────────────┐
│  Need Approval?      │     │  No Approval         │
│  Wait for human      │     │  Continue            │
└──────────┬───────────┘     └──────────┬───────────┘
           │                            │
           └─────────────┬──────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      VERIFYING                                   │
│            Re-check metrics, confirm fix                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       LEARNING                                   │
│            Record to Memory, update Knowledge                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        IDLE                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔌 Tool Marketplace

| Category | Tools |
|----------|-------|
| **Linux** | SSH, top, ps, free, df, systemctl, journalctl, netstat, ss |
| **Kubernetes** | kubectl, helm, crictl, k9s |
| **Docker** | docker, docker-compose, containerd |
| **Database** | MySQL CLI, Redis CLI, psql, mongosh, es-cli |
| **Monitoring** | prometheus-cli, grafana-cli, alertmanager |
| **Logging** | elasticsearch, loki, fluentd |
| **Cloud** | AWS CLI, aliyun CLI, tccli |
| **CI/CD** | Jenkins, GitLab CI, ArgoCD |
| **IaC** | Terraform, Ansible, Pulumi |

---

## 🧠 Memory & Knowledge

### Memory Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Working** | Current session context | Current task |
| **Short-term** | Recent interactions (TTL) | Conversation history |
| **Long-term** | Persistent storage | Incident history |
| **Semantic** | Vector-based retrieval | Similar incidents |
| **Episodic** | Specific events | Past fixes |

### Knowledge Sources

| Source | Description |
|--------|-------------|
| 📖 Runbooks | Standard operating procedures |
| 📘 Official Docs | Vendor documentation |
| 🐛 GitHub Issues | Community solutions |
| 💬 StackOverflow | Technical Q&A |
| 📝 Internal Wiki | Organization knowledge |
| 🗄️ CMDB | Configuration management |

### Memory Flow

```
Incident Occurs
       │
       ▼
AI Diagnoses & Fixes
       │
       ▼
Record Steps & Results
       │
       ▼
Calculate Success Rate
       │
       ▼
Update Semantic Index
       │
       ▼
Next Similar Incident
       │
       ▼
Recall & Apply Experience
```

---

## 👤 Human Approval

```
Agent prepares: systemctl restart mysql
       │
       ▼
Risk Assessment: HIGH
       │
       ▼
Notification sent to:
├── Feishu (飞书)
├── DingTalk (钉钉)
├── Slack
└── Email
       │
       ▼
Wait for approval...
       │
       ▼
Approved → Execute → Verify
Rejected → Log reason → Abort
```

---

## ⚡ Quick Start

### pip install

```bash
pip install agentic-aiops
```

### Docker

```bash
docker run -it --rm \
  -e AIOPS_AI_API_KEY=your-key \
  agentic-aiops aiops diagnose --help
```

### Docker Compose

```bash
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
docker compose up -d
```

### Kubernetes

```bash
helm install aiops ./charts/agentic-aiops \
  --set ai.apiKey=your-key
```

### From Source

```bash
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
pip install -e .
```

---

## 🤖 Supported LLM

| Provider | Model | Status |
|----------|-------|:------:|
| DeepSeek | deepseek-chat | ✅ |
| OpenAI | gpt-4o, gpt-4-turbo | ✅ |
| Anthropic | claude-3-opus, claude-3-sonnet | ✅ |
| Qwen | qwen-max, qwen-plus | ✅ |
| Ollama | llama3, mistral | ✅ |
| OpenRouter | Multiple models | ✅ |
| Azure OpenAI | GPT-4 | ✅ |
| Gemini | gemini-pro | 🚧 |

---

## 🔧 Plugin Development

### Custom Agent

```python
from aiops.agents import BaseAgent

class MyAgent(BaseAgent):
    name = "my_agent"
    description = "Custom agent"

    def observe(self, event):
        # Collect data
        pass

    def reason(self, data):
        # Analyze with LLM
        pass

    def plan(self, analysis):
        # Create execution plan
        pass

    def act(self, plan):
        # Execute tools
        pass

    def verify(self, results):
        # Verify results
        pass
```

### Custom Tool

```python
from aiops.tools import BaseTool, ToolResult

class MyTool(BaseTool):
    name = "my_tool"
    description = "Custom tool"
    category = "custom"

    def execute(self, **kwargs) -> ToolResult:
        # Implementation
        return ToolResult(success=True, output="done")
```

---

## 📊 Capability Matrix

| Capability | Count |
|------------|:-----:|
| Linux Commands | 100+ |
| K8s Operations | 40+ |
| Database Diagnostics | 20+ |
| Monitoring Analysis | 30+ |
| Runbooks | 50+ |
| Agent Types | 12 |
| MCP Tools | 20+ |
| Knowledge Sources | 7 |

---

## 🗺️ Roadmap

### v1.x — Foundation ✅

- [x] Core Agents (Linux, K8s, DB)
- [x] CLI Interface
- [x] MCP Tool System
- [x] Basic Memory

### v2.x — Intelligence 🚧

- [x] Memory System (5 types)
- [x] Knowledge Base
- [x] Workflow Engine
- [x] Approval System
- [ ] RAG Enhancement
- [ ] Event Bus

### v3.x — Platform 📋

- [ ] Web Dashboard
- [ ] Workflow Designer
- [ ] Plugin Marketplace
- [ ] Voice Agent
- [ ] Multi-Cluster Support

---

## 🏢 Enterprise Features

- 🔐 **RBAC** — Role-based access control
- 📋 **Audit Log** — Complete operation history
- ✅ **Approval** — Risk-based workflow approval
- 🔔 **Webhook** — Feishu, DingTalk, Slack, Email
- 🔌 **Plugin** — Extensible architecture
- 📡 **REST API** — OpenAPI specification
- 🌐 **Multi-Cluster** — Cross-cluster management
- 🔄 **High Availability** — HA deployment support

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

[![Contributors](https://contrib.rocks/image?repo=neal4752/agentic-aiops)]()

---

## 📄 License

[MIT License](LICENSE)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neal4752/agentic-aiops&type=Date)]()

---

<div align="center">

**If this project is helpful, please give it a ⭐ Star!**

</div>
