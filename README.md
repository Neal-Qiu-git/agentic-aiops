# Agentic AIOps

<div align="center">

🤖 **AI Native 自主运维平台**

*基于 LLM、Multi-Agent 与 MCP 构建的自主运维平台，可实现 Linux、Kubernetes、数据库、云平台的自主诊断、自主修复与持续学习*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.1-orange.svg?style=flat-square)]()
[![Stars](https://img.shields.io/github/stars/neal4752/agentic-aiops?style=flat-square&logo=github)]()
[![PyPI](https://img.shields.io/pypi/v/agentic-aiops?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/agentic-aiops/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](Dockerfile)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes&logoColor=white)]()
[![MCP](https://img.shields.io/badge/MCP-Supported-FF6B35?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0wIDE4Yy00LjQxIDAtOC0zLjU5LTgtOHMzLjU5LTggOC04IDggMy41OSA4IDgtMy41OSA4LTggOHoiLz48L3N2Zz4=)]()
[![ReAct](https://img.shields.io/badge/ReAct-Agent-9B59B6?style=flat-square)]()
[![Multi-Agent](https://img.shields.io/badge/Multi--Agent-Collaboration-E74C3C?style=flat-square)]()

[English](README_EN.md) | 中文

</div>

---

## 🎯 一句话定位

> **Agentic AIOps** 是一个基于 **LLM + ReAct + MCP + Multi-Agent** 构建的新一代 AI 运维平台，让 AI 不仅能分析，还能真正完成运维工作。

---

## ✨ 为什么选择 Agentic AIOps？

| 能力 | 传统 AIOps | Agentic AIOps |
|------|:----------:|:-------------:|
| 根因分析 | ✅ | ✅ |
| 自动修复 | ❌ | ✅ |
| Multi-Agent 协同 | ❌ | ✅ |
| 持续学习 (Memory) | ❌ | ✅ |
| 知识库 (Knowledge) | ❌ | ✅ |
| 人工审批 (Approval) | ❌ | ✅ |
| 工作流编排 (Workflow) | ❌ | ✅ |
| 事件驱动 (Event Bus) | ❌ | ✅ |
| 插件化扩展 (Plugin) | ❌ | ✅ |
| 云原生支持 | ⚠️ 部分 | ✅ 全覆盖 |

---

## 🏗️ 架构设计

```
                         ┌─────────────────────────────────────┐
                         │              用户层                   │
                         │   CLI / API / Dashboard / Chat       │
                         └──────────────────┬──────────────────┘
                                            │
                         ┌──────────────────▼──────────────────┐
                         │         Event Bus (事件总线)         │
                         │    发布/订阅，解耦组件通信            │
                         └──────────────────┬──────────────────┘
                                            │
                         ┌──────────────────▼──────────────────┐
                         │       Planner Agent (总控)           │
                         │  任务分解 → Agent调度 → 结果聚合      │
                         └──────────────────┬──────────────────┘
                                            │
          ┌─────────────┬─────────────┬─────┴─────┬─────────────┬─────────────┐
          │             │             │           │             │             │
          ▼             ▼             ▼           ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
   │  Linux   │  │   K8s    │  │    DB    │ │   Log    │ │ Monitor  │ │ Security │
   │  Agent   │  │  Agent   │  │  Agent   │ │  Agent   │ │  Agent   │ │  Agent   │
   └──────────┘  └──────────┘  └──────────┘ └──────────┘ └──────────┘ └──────────┘
          │             │             │           │             │             │
          └─────────────┴─────────────┴─────┬─────┴─────────────┴─────────────┘
                                            │
                         ┌──────────────────▼──────────────────┐
                         │        MCP Marketplace (工具市场)    │
                         │  20+ 插件化工具，支持自定义扩展       │
                         └──────────────────┬──────────────────┘
                                            │
                         ┌──────────────────▼──────────────────┐
                         │            Memory + Knowledge        │
                         │    持续学习，知识沉淀，经验复用        │
                         └─────────────────────────────────────┘
```

---

## 🧠 Core Design Principles

1. **Planner-driven** — 所有任务先由 PlannerAgent 拆解，再分发给专业 Agent
2. **Tool-first** — 所有能力通过 MCP Tool 抽象，Agent 不直接操作基础设施
3. **Memory-native** — 每次执行都会学习，形成长期经验
4. **Human-in-the-loop** — 高风险操作必须经过审批
5. **Event-driven** — 所有 Agent 通过 Event Bus 解耦协作

---

## 📸 Demo

```bash
$ aiops diagnose --host 10.0.0.1 --symptom "CPU 高"

╭─────────────────────────────────────────────────────────────────╮
│  🔍 Observe   │ CPU 使用率 95%，持续 5 分钟                      │
│  🧠 Reason    │ 检测到 CPU 异常高，需要诊断                       │
│  📋 Plan      │ 分解任务：检查进程 → 分析 GC → Thread Dump        │
│  ⚡ Action    │ 执行诊断命令...                                  │
│     ├─ $ top -bn1 | head -20                                    │
│     ├─ $ ps aux --sort=-%cpu | head -10                         │
│     └─ $ jstack <pid> > /tmp/thread_dump.txt                   │
│  ✅ Verify    │ 发现 Java 进程 GC 线程占用 80%                    │
│  📝 Learn     │ 记录故障经验到知识库                               │
╰─────────────────────────────────────────────────────────────────╯

📋 诊断报告
├── 根因: Java 进程 Full GC 频繁
├── 证据: GC 线程占用 80% CPU
├── 建议: 增大 JVM 堆内存 -Xmx4g → 8g
└── 置信度: 92%
```

---

## 🤖 Agent 生态

| Agent | 职责 | 状态 |
|-------|------|:----:|
| 🐧 **Linux Agent** | 系统运维：CPU/内存/磁盘/网络 | ✅ |
| ☸️ **K8s Agent** | 容器运维：Pod/Deployment/Node | ✅ |
| 🗄️ **DB Agent** | 数据库：MySQL/Redis/PG/MongoDB | ✅ |
| 📋 **Log Agent** | 日志分析：错误追踪、链路分析 | ✅ |
| 📊 **Monitor Agent** | 监控分析：Prometheus/Grafana | ✅ |
| 🔒 **Security Agent** | 安全运维：漏洞扫描、合规检查 | ✅ |
| 🚀 **DevOps Agent** | DevOps：CI/CD、发布管理 | ✅ |
| 🏥 **SRE Agent** | SRE：SLI/SLO/Error Budget | ✅ |
| 🚨 **Incident Agent** | 故障管理：Timeline、RCA | ✅ |
| 💰 **Cost Agent** | 成本优化：云资源分析 | ✅ |
| 📦 **CMDB Agent** | 配置管理：资产发现、依赖关系 | 🚧 |
| 🎤 **Voice Agent** | 语音运维：语音交互 | 📋 |

---

## 🔄 Agent Lifecycle

```
    ┌─────────────────────────────────────────────────────────────────┐
    │                     Agent Lifecycle                              │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                  │
    │   ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
    │   │ Observe  │───▶│  Reason  │───▶│   Plan   │                  │
    │   │   观察    │    │   推理    │    │   规划    │                  │
    │   └──────────┘    └──────────┘    └──────────┘                  │
    │        │                               │                         │
    │        │                               ▼                         │
    │   ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
    │   │  Learn   │◀───│  Verify  │◀───│   Act    │                  │
    │   │   学习    │    │   验证    │    │   执行    │                  │
    │   └──────────┘    └──────────┘    └──────────┘                  │
    │                                                                  │
    └─────────────────────────────────────────────────────────────────┘
```

---

## 📊 支持矩阵

### 平台支持

| 平台 | 支持 | 说明 |
|------|:----:|------|
| Linux | ✅ | 物理机/虚拟机 |
| Docker | ✅ | 容器化部署 |
| Kubernetes | ✅ | 云原生编排 |
| AWS | ✅ | 云平台 |
| 阿里云 | ✅ | 云平台 |
| 腾讯云 | ✅ | 云平台 |

### 数据库支持

| 数据库 | 支持 | 说明 |
|--------|:----:|------|
| MySQL | ✅ | 慢查询、索引优化 |
| Redis | ✅ | 连接诊断、内存分析 |
| PostgreSQL | ✅ | 性能优化 |
| MongoDB | ✅ | 集合分析 |
| Elasticsearch | ✅ | 索引优化 |
| Kafka | ✅ | 消费延迟分析 |

### 监控工具

| 工具 | 支持 | 说明 |
|------|:----:|------|
| Prometheus | ✅ | 指标查询 |
| Grafana | ✅ | 面板分析 |
| Loki | 🚧 | 日志聚合 |
| VictoriaMetrics | 📋 | 时序数据库 |

---

## ⚡ Quick Start

### 安装

```bash
# pip 安装
pip install agentic-aiops

# 或从源码安装
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
pip install -e .
```

### Docker 部署

```bash
# Docker 单机
docker run -it agentic-aiops aiops diagnose --help

# Docker Compose
docker compose up -d
```

### Kubernetes 部署

```bash
# Helm 安装
helm install aiops ./charts/agentic-aiops

# kubectl 安装
kubectl apply -f k8s/
```

### 配置

```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml

# 设置环境变量
export AIOPS_AI_API_KEY="your-api-key"
```

### 使用

```bash
# 诊断
aiops diagnose --host 10.0.0.1 --symptom "CPU 高"

# K8s 诊断
aiops agent k8s --symptom "Pod CrashLoopBackOff"

# 数据库诊断
aiops agent db --type mysql --symptom "查询慢"

# 工作流执行
aiops workflow run cpu-diagnosis --host 10.0.0.1
```

---

## 🔄 Workflow 示例

```yaml
# cpu-diagnosis.yaml
name: cpu-diagnosis
description: CPU 高诊断流程

steps:
  - name: observe
    action: ssh_exec
    command: "top -bn1 | head -20"

  - name: check_process
    action: ssh_exec
    command: "ps aux --sort=-%cpu | head -10"
    depends_on: observe

  - name: check_gc
    action: ssh_exec
    command: "jstat -gc <pid>"
    depends_on: check_process

  - name: thread_dump
    action: ssh_exec
    command: "jstack <pid> > /tmp/thread_dump.txt"
    depends_on: check_gc

  - name: analyze
    action: ai_analyze
    input: "{{observe.output}} {{check_process.output}} {{check_gc.output}}"
    depends_on: thread_dump

  - name: fix
    action: ssh_exec
    command: "systemctl restart java-app"
    condition: "analyze.severity == 'high'"
    approval: true
    depends_on: analyze

  - name: verify
    action: ssh_exec
    command: "top -bn1 | grep 'Cpu(s)'"
    depends_on: fix

  - name: learn
    action: memory_store
    content: "{{analyze.result}}"
    depends_on: verify
```

---

## 🧠 Memory 流程

```
Redis Down
    │
    ▼
AI 诊断修复
    │
    ▼
记录执行步骤
    │
    ▼
写入 Memory
    │
    ▼
更新 Knowledge
    │
    ▼
下次遇到类似问题
    │
    ▼
直接调用经验
```

---

## 📚 Knowledge 来源

| 来源 | 说明 |
|------|------|
| 📖 Runbook | 运维剧本 |
| 📘 Official Docs | 官方文档 |
| 🐛 GitHub Issues | 社区问题 |
| 💬 StackOverflow | 技术问答 |
| 📝 Internal Wiki | 内部文档 |
| 🗄️ CMDB | 配置管理 |
| 📜 Historical Cases | 历史案例 |

---

## 🔌 插件生态

| 分类 | 插件 |
|------|------|
| **容器** | Docker, Kubernetes, Helm, Containerd |
| **数据库** | MySQL, Redis, PostgreSQL, MongoDB, Elasticsearch |
| **消息队列** | Kafka, RabbitMQ, RocketMQ |
| **监控** | Prometheus, Grafana, AlertManager |
| **云平台** | AWS, 阿里云, 腾讯云 |
| **IaC** | Terraform, Ansible, Pulumi |
| **CI/CD** | Jenkins, GitLab CI, GitHub Actions |

---

## 🏢 Enterprise Features

| 特性 | 说明 |
|------|------|
| 🔐 **RBAC** | 基于角色的访问控制 |
| 📋 **Audit Log** | 完整的审计日志 |
| ✅ **Approval** | 高风险操作审批 |
| 🔔 **Webhook** | 飞书/钉钉/Slack/Email |
| 🔌 **Plugin** | 插件化扩展 |
| 📡 **REST API** | OpenAPI 规范 |
| 🌐 **Multi-Cluster** | 多集群支持 |
| 🔄 **High Availability** | 高可用部署 |

---

## 🗺️ Roadmap

### v1.x ✅

- [x] Linux Agent
- [x] K8s Agent
- [x] DB Agent
- [x] CLI 工具

### v2.x 🚧

- [x] Memory System
- [x] Knowledge Base
- [x] Workflow Engine
- [x] Approval System
- [ ] RAG 检索增强
- [ ] Event Bus

### v3.x 📋

- [ ] Dashboard UI
- [ ] Plugin Marketplace
- [ ] Voice Agent
- [ ] Cloud Agent
- [ ] Multi-Cluster

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

[![Contributors](https://contrib.rocks/image?repo=neal4752/agentic-aiops)]()

---

## 📄 License

[MIT License](LICENSE)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neal4752/agentic-aiops&type=Date)]()

---

<div align="center">

**如果觉得有用，请给个 ⭐ Star 支持一下！**

</div>
