# Agentic AIOps

<div align="center">

🤖 **AI-native Operations Platform**

*Not another AI Agent. An autonomous operations system that diagnoses, fixes, verifies, and learns.*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-4.2-orange.svg?style=flat-square)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)]()
[![K8s](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes&logoColor=white)]()
[![MCP](https://img.shields.io/badge/MCP-20%2B_Tools-FF6B35?style=flat-square)]()
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen?style=flat-square&logo=react&logoColor=white)](https://Neal-Qiu-git.github.io/agentic-aiops/)

[English](README_EN.md) | 中文 | [Docs](docs/) | [Examples](examples/) | [Changelog](CHANGELOG.md)

</div>

---

## 📖 什么是 Agentic AIOps？

**Agentic AIOps** 是一个 AI 原生的运维平台，融合了多智能体协作、记忆系统、知识库、工作流引擎、事件总线和人工审批，构建统一的智能运维体系。

> **它不是又一个 AI Agent —— 它是一个自治运维平台。**

### 与同类框架对比

| 框架 | 定位 | MCP | 记忆 | 工作流 | 审批 | 前端 |
|------|------|:---:|:----:|:------:|:----:|:----:|
| LangGraph | 通用Agent | ❌ | ✅ | ✅ | ❌ | ❌ |
| CrewAI | 通用Agent | ❌ | ❌ | ❌ | ❌ | ❌ |
| AutoGPT | 通用Agent | ❌ | ❌ | ❌ | ❌ | ❌ |
| OpenHands | 开发Agent | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Agentic AIOps** | **运维Agent** | ✅ | ✅ | ✅ | ✅ | 🚧 |

---

## ✨ 核心特性

- 🤖 **12 专业智能体** — Linux、K8s、数据库、日志、监控、安全、SRE、成本、事件、DevOps、CMDB、规划师
- 🔄 **ReAct 生命周期** — 观察 → 推理 → 计划 → 执行 → 验证 → 学习
- 🔌 **MCP 工具市场** — 20+ 工具，插件化架构
- 🧠 **5 类记忆系统** — 工作记忆、短期、长期、语义、情景
- 📚 **知识库 RAG** — Runbook、文档、历史案例语义检索
- ⚡ **事件总线** — 解耦式智能体协作
- 🚦 **工作流引擎** — YAML 声明式自动化编排
- 👤 **人工审批** — 基于风险等级的审批流
- 📡 **REST API** — OpenAPI 规范
- 🖥️ **CLI** — 全功能命令行
- 🐳 **Docker/K8s** — 一键部署
- 🔒 **安全引擎** — 命令黑名单、审计日志、敏感路径保护

---

## 📸 在线演示

> **[🚀 点击查看 Dashboard](https://Neal-Qiu-git.github.io/agentic-aiops/)** — 深空科技风可视化运维平台

### 🕸️ Agent 网络拓扑

12 个专业智能体通过事件总线协作，实时展示 Agent 之间的数据流和依赖关系。

### 📊 仪表盘总览

系统健康监控（CPU / 内存 / 磁盘 / 网络）、智能体状态、最近事件流。

### 🤖 智能体管理

每个 Agent 的任务数、成功率、响应时间、最后活跃时间。

### ⚡ 工作流引擎

YAML 声明式自动化编排，步骤可视化展示。

### 📡 事件日志

实时事件流（成功 / 警告 / 错误 / 信息），支持筛选和搜索。

---

### CLI 演示

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

---

## 🏗️ 架构

```
                         ┌─────────────────────┐
                         │      用户层         │
                         │  CLI │ API │ Chat   │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │     事件总线        │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │   规划师 Agent      │
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
                     │   MCP 工具市场      │
                     └──────────┬──────────┘
                                │
                     ┌──────────▼──────────┐
                     │  记忆  │  知识库     │
                     └─────────────────────┘
```

📖 **[详细架构文档](docs/architecture.md)**

---

## ⚡ 快速开始

### 方式一：一键脚本（推荐）

```bash
# Linux / macOS
curl -sL https://gitee.com/neal4752/agentic-aiops/raw/main/deploy.sh -o deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### 方式二：Docker Compose

```bash
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
cp .env.example .env
# 编辑 .env 填入 API Key
docker compose up -d
```

### 方式三：pip 安装

```bash
pip install agentic-aiops

# 配置
export AIOPS_AI_API_KEY=your-api-key

# 运行诊断
aiops diagnose --host 10.0.0.1 --symptom "CPU 高"
```

### 方式四：Kubernetes

```bash
helm install aiops ./charts/agentic-aiops --set ai.apiKey=your-key
```

📖 **[完整安装文档](docs/installation.md)**

---

## 📊 支持矩阵

| 平台 | 数据库 | 监控 | 云 |
|------|--------|------|-----|
| Linux ✅ | MySQL ✅ | Prometheus ✅ | AWS ✅ |
| Docker ✅ | Redis ✅ | Grafana ✅ | 阿里云 ✅ |
| K8s ✅ | PostgreSQL ✅ | Loki 🚧 | 腾讯云 ✅ |
| | MongoDB ✅ | | |
| | Elasticsearch ✅ | | |

---

## 🤖 支持的智能体

| 智能体 | 描述 | 状态 |
|--------|------|:----:|
| 🐧 Linux | 系统诊断 | ✅ |
| ☸️ K8s | Kubernetes 运维 | ✅ |
| 🗄️ DB | 数据库诊断 | ✅ |
| 📋 Log | 日志分析 | ✅ |
| 📊 Monitor | 监控分析 | ✅ |
| 🔒 Security | 安全扫描 | ✅ |
| 🏥 SRE | SLI/SLO/错误预算 | ✅ |
| 💰 Cost | 成本优化 | ✅ |
| 🚨 Incident | 事件管理 | ✅ |
| 🚀 DevOps | CI/CD 运维 | ✅ |
| 📦 CMDB | 配置管理 | ✅ |
| 📋 Planner | 任务规划 | ✅ |

---

## 🤖 支持的大模型

| 提供商 | 模型 |
|--------|------|
| DeepSeek | deepseek-chat |
| OpenAI | gpt-4o, gpt-4-turbo |
| Anthropic | claude-3-opus, claude-3-sonnet |
| 通义千问 | qwen-max, qwen-plus |
| Ollama | llama3, mistral |
| OpenRouter | 多种模型 |

---

## 🗺️ 路线图

### v1.x — 基础 ✅
- [x] 核心 Agent（Linux、K8s、DB）
- [x] CLI 界面
- [x] MCP 工具系统
- [x] 基础记忆

### v2.x — 智能 ✅
- [x] 5 类记忆系统
- [x] 知识库 RAG
- [x] 工作流引擎
- [x] 审批系统

### v3.x — 平台 🚧
- [x] REST API
- [x] Docker/K8s 部署
- [x] Web Dashboard (React + TypeScript)
- [ ] 可视化工作流设计器

### v4.x — 企业 📋
- [ ] 多集群支持
- [ ] RBAC 权限
- [ ] 审计日志
- [ ] 高可用部署

---

## 📁 项目结构

```
agentic-aiops/
├── aiops/                  # 核心代码
│   ├── agents/             # 12个专业智能体
│   ├── analyzers/          # 分析器
│   ├── api/                # REST API
│   ├── approval/           # 审批系统
│   ├── collectors/         # 数据采集
│   ├── core/               # 核心引擎
│   ├── eventbus/           # 事件总线
│   ├── knowledge/          # 知识库
│   ├── mcp/                # MCP 工具
│   ├── memory/             # 记忆系统
│   ├── modules/            # 功能模块
│   ├── planner/            # 规划引擎
│   ├── plugins/            # 插件系统
│   ├── rag/                # RAG 检索
│   ├── reporters/          # 报告生成
│   ├── tools/              # 工具集
│   └── workflow/           # 工作流引擎
├── data/                   # 数据文件
│   ├── knowledge/          # 知识库数据
│   └── memory/             # 记忆存储
├── docs/                   # 文档
├── examples/               # 场景示例
├── plugins/                # 外部插件
├── runbooks/               # 运维手册
├── scripts/                # 脚本工具
├── tests/                  # 测试
├── deploy.sh               # 一键部署
├── docker-compose.yml      # Docker 编排
├── .env.example            # 环境变量模板
├── config.example.yaml     # 配置模板
└── CHANGELOG.md            # 版本历史
```

---

## 📚 文档

- [架构设计](docs/architecture.md)
- [安装部署](docs/installation.md)
- [智能体](docs/agents.md)
- [工作流](docs/workflow.md)
- [记忆系统](docs/memory.md)
- [知识库](docs/knowledge.md)
- [审批系统](docs/approval.md)
- [MCP 工具](docs/mcp.md)
- [安全机制](docs/security.md)
- [API 文档](docs/api.md)
- [常见问题](docs/faq.md)
- [ADR 决策记录](docs/adr/)

---

## 📁 场景示例

| 示例 | 描述 |
|------|------|
| [cpu-high](examples/cpu-high/) | CPU 使用率诊断 |
| [memory-leak](examples/memory-leak/) | 内存泄漏检测 |
| [pod-crash](examples/pod-crash/) | K8s Pod 故障排查 |
| [redis-timeout](examples/redis-timeout/) | Redis 连接超时 |
| [mysql-slow](examples/mysql-slow/) | MySQL 慢查询分析 |
| [disk-full](examples/disk-full/) | 磁盘空间诊断 |

---

## 🤝 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)

[![Contributors](https://contrib.rocks/image?repo=neal4752/agentic-aiops)]()

---

## 📄 许可证

[MIT License](LICENSE)

---

<div align="center">

**如果项目对你有帮助，请点个 ⭐ Star 支持！**

</div>
