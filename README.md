# Agentic AIOps

<div align="center">

🤖 **AI Native 自主运维平台**

*让 AI 不仅能分析，还能真正完成运维工作*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.1-orange.svg)]()
[![Stars](https://img.shields.io/github/stars/neal4752/agentic-aiops?style=social)]()

[English](README_EN.md) | 中文

</div>

---

## 🎯 什么是 Agentic AIOps？

**Agentic AIOps** 是一个基于 **LLM + ReAct + MCP + Multi-Agent** 构建的新一代 AI 运维平台。

```
传统 AIOps：监控 → 告警 → 人工处理

Agentic AIOps：
监控 → AI分析 → AI制定方案 → AI执行 → AI验证 → AI总结经验 → 知识沉淀
```

> **AI 能独立完成一次完整的运维闭环。**

---

## 🚀 核心特性

| 特性 | 说明 |
|------|------|
| 🔄 **Agent 生命周期** | Observe → Reason → Plan → Act → Verify → Learn |
| 🧠 **Memory System** | 短期/长期/语义/情景记忆，持续学习 |
| 📚 **Knowledge + RAG** | Runbook、官方文档、历史案例智能检索 |
| ⚡ **Event Driven** | 事件驱动的 Multi-Agent 协作 |
| 🔧 **MCP Marketplace** | 插件化工具市场，支持 20+ 工具 |
| 🚦 **Workflow Engine** | YAML 编排，可视化运维流程 |
| 👤 **Human Approval** | 高风险操作审批，支持 Webhook/飞书/钉钉 |
| 🏢 **Multi-Environment** | 本地/容器/K8s/云平台全覆盖 |

---

## 📸 Demo

```bash
# CPU 诊断
$ aiops diagnose --host 10.0.0.1 --symptom "CPU 高"

╭──────────────────────────────────────────────────────╮
│  🔍 Observe: CPU 使用率 95%                           │
│  🧠 Reason: 检测到 CPU 异常高                          │
│  📋 Plan: 执行 CPU 诊断流程                           │
│  ⚡ Action: 执行诊断命令...                           │
│     $ top -bn1 | head -20                            │
│     $ ps aux --sort=-%cpu | head -10                 │
│  ✅ Verify: 发现 Java 进程占用 80%                     │
│  📝 Learn: 记录故障经验到知识库                         │
╰──────────────────────────────────────────────────────╯

根因分析: Java 进程 gc 频繁导致 CPU 高
建议: 增大 JVM 堆内存 -Xmx4g → 8g
```

---

## 🏗️ 架构图

```
                    ┌─────────────────────────────────────┐
                    │           用户层                      │
                    │    CLI / API / Dashboard / Chat      │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────▼───────────────────┐
                    │         Planner Agent (总控)         │
                    │    任务分解 → Agent调度 → 结果聚合     │
                    └─────────────────┬───────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│  Linux Agent    │        │  K8s Agent      │        │  DB Agent       │
│  系统运维        │        │  容器运维        │        │  数据库运维       │
└─────────────────┘        └─────────────────┘        └─────────────────┘
          │                           │                           │
          └───────────────────────────┼───────────────────────────┘
                                      │
                    ┌─────────────────▼───────────────────┐
                    │          MCP Marketplace            │
                    │    SSH | K8s | Docker | DB | Cloud  │
                    └─────────────────┬───────────────────┘
                                      │
┌─────────────────────────────────────┼─────────────────────────────┐
│                                     │                             │
▼                                     ▼                             ▼
🧠 Memory                    📚 Knowledge                    ⚡ Event Bus
短期/长期/语义/情景记忆         Runbook/文档/RAG               事件驱动协作
```

---

## 🎯 运维场景

| 场景 | 支持 | 说明 |
|------|:----:|------|
| CPU 高 | ✅ | 进程分析、GC 诊断、线程 Dump |
| 内存泄漏 | ✅ | 堆分析、GC 日志、内存监控 |
| 磁盘满 | ✅ | 大文件查找、日志清理、扩容建议 |
| Pod CrashLoopBackOff | ✅ | OOM/探针/配置/镜像诊断 |
| Node NotReady | ✅ | 资源/网络/组件诊断 |
| Redis 连接失败 | ✅ | 连接池/内存/网络/DNS 诊断 |
| MySQL 慢查询 | ✅ | 索引/锁/配置优化建议 |
| Nginx 502 | ✅ | 后端/超时/配置诊断 |
| Kafka 消费延迟 | ✅ | 消费者组/分区/配置诊断 |

---

## ⚡ 快速开始

```bash
# 安装
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
pip install -e .

# 配置
cp config.example.yaml config.yaml
# 编辑 config.yaml

# 使用
aiops diagnose --host 10.0.0.1 --symptom "服务响应慢"
```

📖 **[完整安装文档](docs/installation.md)** | 📚 **[架构详解](docs/architecture.md)** | 🔧 **[Agent 指南](docs/agents.md)**

---

## 🗺️ Roadmap

| 阶段 | 功能 | 状态 |
|------|------|:----:|
| **Current** | Linux/K8s/DB Agent, Memory, Knowledge | ✅ |
| **Next** | Workflow, Approval, RAG, Event Bus | 🚧 |
| **Future** | Plugin Marketplace, Voice Agent, GUI | 📋 |

---

## 📚 文档

- [安装指南](docs/installation.md)
- [架构设计](docs/architecture.md)
- [Agent 指南](docs/agents.md)
- [Workflow 引擎](docs/workflow.md)
- [记忆系统](docs/memory.md)
- [知识库](docs/knowledge.md)
- [审批系统](docs/approval.md)
- [MCP 工具市场](docs/mcp.md)
- [安全配置](docs/security.md)
- [API 文档](docs/api.md)
- [FAQ](docs/faq.md)

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

---

## 📄 License

[MIT License](LICENSE)

---

<div align="center">

**如果觉得有用，请给个 ⭐ Star 支持一下！**

</div>
