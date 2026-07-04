# Agentic AIOps

<div align="center">

🤖 **AI-Native Intelligent Operations Platform**

*Not another AI Agent. An autonomous operations system that diagnoses, fixes, verifies, and learns.*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-5.3-orange.svg?style=flat-square)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)]()
[![K8s](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes&logoColor=white)]()
[![MCP](https://img.shields.io/badge/MCP-148%2B_Tools-FF6B35?style=flat-square)]()
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen?style=flat-square&logo=react&logoColor=white)](https://Neal-Qiu-git.github.io/agentic-aiops/)

[English](README_EN.md) | 中文 | [Docs](docs/) | [Examples](examples/) | [Changelog](CHANGELOG.md)

</div>

---

## 📖 什么是 Agentic AIOps？

**Agentic AIOps** 是一个 AI 原生的运维平台，融合了多智能体协作、记忆系统、知识库、工作流引擎、事件总线和人工审批，构建统一的智能运维体系。

> **它不是又一个 AI Agent —— 它是一个自治运维平台。**

### 核心数据

| 指标 | 数量 |
|------|------|
| 🤖 专业智能体 | 21+ |
| 🔌 MCP 工具 | 148+ |
| 🏗️ 环境拓扑 | 18 种 |
| 📊 Dashboard 页面 | 14 个 |
| 🌐 REST API 端点 | 27+ |
| 📜 开源协议 | MIT |

### 与同类框架对比

| 框架 | 定位 | MCP | 记忆 | 工作流 | 审批 | 前端 | 环境发现 |
|------|------|:---:|:----:|:------:|:----:|:----:|:--------:|
| LangGraph | 通用Agent | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| CrewAI | 通用Agent | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| AutoGPT | 通用Agent | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| OpenHands | 开发Agent | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Agentic AIOps** | **运维Agent** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## ✨ 核心特性

### 🤖 智能体体系
- **21 个专业智能体** — 覆盖 Linux、K8s、Docker、数据库、中间件、网络、虚拟化、Windows、监控、日志、APM、安全、SRE、成本、事件、DevOps、GitOps、IaC、云平台、服务网格、AI Copilot
- **5 层架构** — 核心调度层 → 基础运维层 → 监控可观测层 → 安全&运维层 → 云&FinOps层
- **ReAct 生命周期** — 观察 → 推理 → 计划 → 执行 → 验证 → 学习

### 🔌 工具与集成
- **148+ MCP 工具** — 覆盖 15 大类运维场景
- **技术栈全覆盖** — Prometheus、Grafana、SkyWalking、Jaeger、Loki、Terraform、Ansible、Helm、ArgoCD、Jenkins、Trivy、Kubecost 等
- **多云支持** — AWS、Azure、GCP、阿里云、华为云、腾讯云

### 🏗️ 环境管理
- **18 种环境拓扑** — 纯本地、纯云、混合云、多云、边缘、跨境、国产化全栈等
- **环境发现 Agent** — 自动探测 OS、硬件、容器、中间件、数据库，智能推荐 Agent 组合
- **多行业 Demo** — 汽车制造、医疗HIS、高校超算、电商、游戏、证券、政务云等

### 📊 可视化 Dashboard
- **平台概览** — 架构图、核心能力、技术栈覆盖
- **使用指南** — 5步快速开始、CLI命令参考、API端点、配置文件示例
- **Agent 网络** — 分层架构、数据流向、工作流示例、通信链路
- **智能体 & 工具** — 能力矩阵、工具分类、智能体目录

### 🔒 企业级能力
- **工作流引擎** — 10 条真实企业工作流（P0故障响应、每日巡检、自动扩缩容等）
- **人工审批** — 基于风险等级的审批流
- **安全引擎** — 命令黑名单、审计日志、敏感路径保护
- **REST API** — OpenAPI 规范，27+ 端点
- **CLI** — 全功能命令行

---

## 📸 在线演示

> **[🚀 点击查看 Dashboard](https://Neal-Qiu-git.github.io/agentic-aiops/)** — 深空科技风可视化运维平台

### 仪表盘 4 个 Tab

| Tab | 内容 |
|-----|------|
| 📊 平台概览 | 架构图、核心能力、技术栈、快速入口 |
| 📖 使用指南 | 快速开始、CLI命令、API端点、配置示例、18种环境拓扑 |
| 🕸️ Agent 网络 | 5层架构、数据流向、工作流示例、27条通信链路 |
| 🤖 智能体 & 工具 | 10个核心Agent能力矩阵、15类工具、21个智能体目录 |

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
┌─────────────────────────────────────────────────────────┐
│                    📊 Dashboard (React)                  │
│  仪表盘 │ 监控 │ 告警 │ 部署 │ SLO │ 安全 │ 成本 │ 环境  │
├─────────────────────────────────────────────────────────┤
│                  🌐 API Server (Python)                  │
│          /api/v1/health │ monitoring │ deployment        │
│          /api/v1/alerts │ slo │ cost │ security          │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│ 🧠 Planner│ 🐧 Linux │ 🐳 Docker│ ☸️ K8s   │ 🗄️ DB      │
│ 🤖 Copilot│ 🪟 Win   │ 🖥️ Virt │ 🌐 Net   │ 📦 Middleware│
├──────────┼──────────┼──────────┼──────────┼─────────────┤
│ 📊 Monitor│ 📋 Log   │ 🔍 APM   │ 🏥 SRE   │ 🔒 Security │
│ 💰 FinOps │ 🚨 Incident│ 🚀 DevOps│ 🔀 GitOps│ 🏗️ IaC   │
├──────────┴──────────┴──────────┴──────────┴─────────────┤
│              🔌 MCP Tools (148+ 工具)                    │
│  Prometheus │ Grafana │ K8s │ Docker │ Terraform │ Vault │
│  Ansible │ Helm │ ArgoCD │ Jenkins │ Trivy │ SkyWalking │
├─────────────────────────────────────────────────────────┤
│              🌍 支持环境 (18种拓扑)                       │
│  本地物理机 │ 虚拟化 │ 容器 │ 公有云 │ 混合云 │ 多云       │
│  Serverless │ 边缘 │ 跨境 │ 国产化 │ 灾备 │ 多活         │
└─────────────────────────────────────────────────────────┘
```

📖 **[详细架构文档](docs/architecture.md)**

---

## ⚡ 快速开始

### 方式一：pip 安装（推荐）

```bash
pip install agentic-aiops

# 验证安装
aiops --version

# 环境探测
aiops discover

# 启动服务 (API + Dashboard)
aiops serve
# 访问 http://localhost:8000
```

### 方式二：Docker Compose

```bash
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
cp .env.example .env
# 编辑 .env 填入 API Key
docker compose up -d
```

### 方式三：一键脚本

```bash
curl -sL https://gitee.com/neal4752/agentic-aiops/raw/main/deploy.sh -o deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### 方式四：Kubernetes

```bash
helm install aiops ./charts/agentic-aiops --set ai.apiKey=your-key
```

📖 **[完整安装文档](docs/installation.md)**

---

## ⌨️ CLI 命令

| 命令 | 说明 | 分类 |
|------|------|------|
| `aiops discover` | 环境探测 | 探测 |
| `aiops serve` | 启动服务 (API + Dashboard) | 服务 |
| `aiops status` | 查看平台状态 | 服务 |
| `aiops agents list` | 列出所有智能体 | 管理 |
| `aiops agents run <agent> "<task>"` | 执行指定任务 | 管理 |
| `aiops alerts list` | 告警列表 | 运维 |
| `aiops alerts ack <id>` | 确认告警 | 运维 |
| `aiops workflow list` | 工作流列表 | 运维 |
| `aiops workflow run "<name>"` | 执行工作流 | 运维 |
| `aiops cost report` | 成本分析报告 | FinOps |
| `aiops security scan` | 安全漏洞扫描 | 安全 |
| `aiops slo status` | SLO 状态查看 | SRE |
| `aiops deploy status` | 部署状态查看 | 部署 |
| `aiops env list` | 环境列表 | 环境 |

---

## 📊 支持矩阵

### 平台 & 运行时

| 平台 | 容器 | 数据库 | 中间件 | 监控 |
|------|------|--------|--------|------|
| Linux ✅ | Docker ✅ | MySQL ✅ | Nginx ✅ | Prometheus ✅ |
| Windows ✅ | containerd ✅ | PostgreSQL ✅ | RabbitMQ ✅ | Grafana ✅ |
| 麒麟 V10 ✅ | Podman ✅ | Redis ✅ | Kafka ✅ | SkyWalking ✅ |
| 统信 UOS ✅ | K3s ✅ | Oracle ✅ | TongWeb ✅ | Jaeger ✅ |
| openEuler ✅ | Docker Swarm ✅ | 达梦 DM8 ✅ | WildFly ✅ | Loki ✅ |
| | | MongoDB ✅ | Caddy ✅ | |
| | | Elasticsearch ✅ | | |
| | | TiDB ✅ | | |
| | | ClickHouse ✅ | | |

### 云平台

| 云 | 服务 |
|----|------|
| AWS ✅ | EC2, RDS, S3, CloudFront, Lambda, EKS |
| 阿里云 ✅ | ECS, RDS, Redis, SLB, OSS, CDN, ACK |
| 华为云 ✅ | ECS, RDS, OBS, CCE, 华为云Stack |
| 腾讯云 ✅ | CVM, COS, CLB, TKE |
| Azure ✅ | VM, SQL, Blob, AKS |
| GCP ✅ | Compute, Cloud SQL, GKE |

### IaC & CI/CD

| 工具 | 状态 |
|------|------|
| Terraform ✅ | Ansible ✅ |
| Helm ✅ | ArgoCD ✅ |
| Jenkins ✅ | GitLab CI ✅ |
| GitHub Actions ✅ | FluxCD ✅ |

---

## 🤖 智能体目录 (21 个)

### 核心调度层
| 智能体 | 描述 | 工具数 |
|--------|------|:------:|
| 📋 Planner | 任务规划调度 · 总控中心 | 2 |
| 🤖 Copilot | AI 对话助手 | 2 |

### 基础运维层
| 智能体 | 描述 | 工具数 |
|--------|------|:------:|
| 🐧 Linux | 系统诊断与性能分析 | 8 |
| 🐳 Docker | Docker/containerd 容器运维 | 7 |
| ☸️ K8s | Kubernetes 运维管理 | 6 |
| 🗄️ DB | 数据库诊断优化 (MySQL/PG/Oracle/Redis/DM8/TiDB) | 7 |
| 📦 Middleware | 中间件管理 (Nginx/RabbitMQ/Kafka/TongWeb) | 6 |
| 🌐 Network | 网络运维 (防火墙/LB/DNS/VPN) | 5 |
| 🖥️ Virtual | 虚拟化运维 (VMware/KVM/Proxmox/OpenStack) | 5 |
| 🪟 Windows | Windows Server 运维 | 4 |

### 监控可观测层
| 智能体 | 描述 | 工具数 |
|--------|------|:------:|
| 📊 Monitor | 监控分析 (Prometheus/Grafana/OTel) | 5 |
| 📋 Log | 日志分析 (Loki/ELK/SkyWalking) | 5 |
| 🔍 APM | 应用性能追踪 (SkyWalking/Jaeger/OTel) | 4 |
| 🏥 SRE | SLI/SLO/错误预算管理 | 3 |

### 安全 & 运维层
| 智能体 | 描述 | 工具数 |
|--------|------|:------:|
| 🔒 Security | 安全扫描 (Trivy/Falco/OPA/Kubescape) | 5 |
| 🚨 Incident | 事件管理与自动响应 | 4 |
| 🚀 DevOps | CI/CD (Jenkins/GitLab CI/GitHub Actions) | 5 |
| 🔀 GitOps | GitOps 部署 (ArgoCD/FluxCD) | 3 |
| 🏗️ IaC | 基础设施即代码 (Terraform/Ansible) | 4 |

### 云 & FinOps 层
| 智能体 | 描述 | 工具数 |
|--------|------|:------:|
| ☁️ Cloud | 多云管理 (AWS/Azure/GCP/阿里/华为/腾讯) | 6 |
| 💰 FinOps | 成本优化 (Kubecost/AWS/Azure) | 3 |
| 🔀 ServiceMesh | 服务网格 (Istio/Linkerd) | 3 |

---

## 🤖 支持的大模型

| 提供商 | 模型 |
|--------|------|
| DeepSeek | deepseek-chat, deepseek-reasoner |
| OpenAI | gpt-4o, gpt-4-turbo |
| Anthropic | claude-3-opus, claude-3-sonnet |
| 通义千问 | qwen-max, qwen-plus |
| 小米 MIMO | mimo-v2.5-pro |
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

### v3.x — 平台 ✅
- [x] REST API
- [x] Docker/K8s 部署
- [x] Web Dashboard (React + TypeScript + Vite)

### v4.x — 企业 ✅
- [x] 148+ MCP 工具 (32+ 工具文件)
- [x] 21+ 专业智能体
- [x] 18 种环境拓扑
- [x] 环境发现 Agent
- [x] Dashboard 14 个页面
- [x] 10 条企业级工作流
- [x] 多云/混合云/国产化支持

### v5.x — 完善 🚧
- [x] 仪表盘重构为平台介绍分页
- [x] Agent 网络 + 智能体整合到仪表盘
- [x] 核心页面接入真实 API (12/14 页面)
- [ ] 可视化工作流设计器
- [ ] 多集群支持
- [ ] RBAC 权限
- [ ] 高可用部署

---

## 📁 项目结构

```
agentic-aiops/
├── aiops/                      # 核心代码
│   ├── agents/                 # 智能体定义
│   ├── analyzers/              # 分析器
│   ├── api/                    # REST API Server
│   ├── approval/               # 审批系统
│   ├── collectors/             # 数据采集
│   ├── core/                   # 核心引擎
│   ├── environments/           # 环境管理 (18种拓扑)
│   ├── eventbus/               # 事件总线
│   ├── knowledge/              # 知识库
│   ├── mcp/                    # MCP 工具
│   ├── memory/                 # 记忆系统
│   ├── modules/                # 功能模块
│   ├── planner/                # 规划引擎
│   ├── plugins/                # 插件系统
│   ├── rag/                    # RAG 检索
│   ├── reporters/              # 报告生成
│   ├── tools/                  # 32+ 工具文件 (148+ 工具)
│   ├── web/                    # Dashboard 构建产物
│   └── workflow/               # 工作流引擎
├── dashboard/                  # Dashboard 前端 (React + TypeScript + Vite)
│   ├── src/
│   │   ├── pages/              # 14 个页面
│   │   ├── api.ts              # API 数据获取层
│   │   └── App.tsx             # 主应用
│   └── package.json
├── data/                       # 数据文件
├── docs/                       # 文档
├── examples/                   # 场景示例
├── plugins/                    # 外部插件
├── runbooks/                   # 运维手册
├── scripts/                    # 脚本工具 (含 deploy-pages.sh)
├── tests/                      # 测试
├── deploy.sh                   # 一键部署
├── docker-compose.yml          # Docker 编排
├── config.example.yaml         # 配置模板 (18种拓扑)
└── CHANGELOG.md                # 版本历史
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
