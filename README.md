# Agentic AIOps

<div align="center">

🤖 **Agent 驱动的智能运维平台**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0-orange.svg)]()

</div>

---

## 核心理念

> **传统 AIOps：发现问题 → 提示运维人员处理**
>
> **Agentic AIOps：发现问题 → 自主分析 → 自主执行 → 自主验证 → 自主学习**

每个 Agent 具备独立思考和行动能力，通过 **ReAct 循环**（Reasoning + Acting）自主完成运维任务。

---

## 10 大能力中心

| # | 能力 | Agent | 说明 |
|---|------|-------|------|
| 1 | 🤖 **AI Copilot** | `AICopilot` | 运维问答、命令生成 |
| 2 | 🔍 **根因分析** | `LinuxAgent` | CPU/内存/磁盘/网络故障自动诊断 |
| 3 | 🔧 **自动修复** | `LinuxAgent` | 基于 Runbook 自主执行修复 |
| 4 | ☸️ **K8s Agent** | `K8sAgent` | Pod/Deployment/Node 故障诊断和管理 |
| 5 | 🗄️ **DB Agent** | `DBAgent` | MySQL/Redis 性能诊断 |
| 6 | 📋 **Log Agent** | `LogAgent` | 日志分析、错误链路追踪 |
| 7 | 📊 **Monitor Agent** | `MonitorAgent` | Prometheus/Grafana 监控分析 |
| 8 | 🔒 **Security Agent** | `SecurityAgent` | 安全巡检、入侵检测 |
| 9 | 🚀 **DevOps Agent** | `DevOpsAgent` | CI/CD、发布管理 |
| 10 | 🧠 **Multi-Agent** | `PlannerAgent` | 任务分解、多 Agent 协同 |

---

## 系统架构

```
CLI / API
    │
PlannerAgent (总控)
    │
┌───┼───────────────────────────┐
│   │                           │
LinuxAgent  K8sAgent  DBAgent  LogAgent  MonitorAgent  SecurityAgent  DevOpsAgent
│   │                           │
Tool Registry (MCP)
│
kubectl | docker | ssh | mysql | redis | prometheus | git | helm
```

---

## 快速开始

### 安装

```bash
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
pip install -e .
```

### 配置

```bash
cp config.example.yaml config.yaml
```

编辑 `config.yaml`，配置服务器和 AI API。

### 使用

```bash
# AI Copilot
aiops copilot "CPU为什么高"

# Agent 自主诊断
aiops agent diagnose --host 10.0.0.1 --symptom "服务响应慢"

# K8s Agent
aiops agent k8s --symptom "Pod CrashLoopBackOff"

# DB Agent
aiops agent db --type mysql --symptom "查询慢"

# Security Agent
aiops agent security --host 10.0.0.1

# Log Agent
aiops agent log --host 10.0.0.1 --file /var/log/nginx/error.log --pattern "502"

# Auto-Fix
aiops agent auto-fix --host 10.0.0.1 --issue high-cpu
```

---

## Agent ReAct 循环

```
Thought → Action → Observation → ... → Final Answer
```

示例：Pod CrashLoopBackOff 诊断

```
Agent Thought: 查看 Pod 状态
Agent Action: k8s_get_pods
Observation: myapp-pod CrashLoopBackOff

Agent Thought: 查看事件
Agent Action: k8s_get_events
Observation: OOMKilled

Agent Thought: 内存不足，查看配置
Agent Action: k8s_describe_pod
Observation: memory limit=128Mi

Agent Final Answer: 内存限制不足，建议增大至 512Mi
```

---

## Tool Calling (MCP)

| 工具 | 功能 |
|------|------|
| `ssh_exec` | SSH 远程执行 |
| `kubectl` / `k8s_*` | Kubernetes 管理（8个工具） |
| `docker_*` | Docker 管理 |
| `mysql_query` | MySQL 查询 |
| `redis_query` | Redis 命令 |
| `prometheus_query` | PromQL 查询 |
| `log_search` | 日志搜索 |

---

## 项目结构

```
aiops/
├── cli.py              # CLI 入口
├── core/               # 核心引擎（SSH/AI/Config）
├── agents/             # Agent 层（ReAct 循环）
│   ├── base.py         # BaseAgent
│   ├── planner.py      # 8个专业 Agent
│   └── copilot.py      # AI Copilot
├── tools/              # Tool 层（MCP 工具）
│   ├── registry.py     # 工具注册中心
│   ├── ssh/k8s/docker/mysql/redis/prometheus/log/http
├── modules/            # 功能模块
├── collectors/         # 数据采集
├── analyzers/          # 分析引擎
├── reporters/          # 报告生成
└── knowledge/          # 知识库
```

---

## License

MIT License
