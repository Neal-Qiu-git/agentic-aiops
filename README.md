# Agentic AIOps

<div align="center">

🤖 **AI Native 运维平台，让 AI 不仅能分析，还能真正完成运维工作**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.0-orange.svg)]()

</div>

---

## 什么是 Agentic AIOps？

**Agentic AIOps** 是一个基于 **LLM + ReAct + MCP + Multi-Agent** 构建的新一代 AI 运维平台。

区别于传统 AIOps：

```
传统 AIOps：
监控 → 告警 → 人工处理

Agentic AIOps：
监控 → AI分析 → AI制定方案 → AI执行 → AI验证 → AI总结经验 → 知识沉淀
```

真正实现：

> **AI 能独立完成一次完整的运维闭环。**

---

## Agent 生命周期

```
Observe → Reason → Plan → Act → Verify → Learn
```

示例：Prometheus 发现 CPU 异常

```
1. Observe: Prometheus 发现 CPU 使用率 > 90%
         ↓
2. Reason: PlannerAgent 分析需要哪些 Agent
         ↓
3. Plan: 分解任务给 LinuxAgent, LogAgent, MonitorAgent
         ↓
4. Act: 各 Agent 并行执行诊断
         ↓
5. Verify: 验证修复结果，确认 CPU 恢复正常
         ↓
6. Learn: 记录故障经验，写入知识库
```

---

## ⚠️ 安全说明

**重要：在生产环境使用前，请务必：**

1. **配置敏感信息**：使用环境变量存储密码和 API Key
2. **配置安全策略**：编辑 `config.yaml` 中的安全选项
3. **限制命令执行**：配置命令白名单/黑名单
4. **启用审批流程**：危险操作需要人工确认

```bash
# 设置环境变量
export AIOPS_SERVER_PRODUCTION_PASSWORD="your-password"
export AIOPS_AI_API_KEY="your-api-key"

# 或使用密钥文件
export AIOPS_SERVER_PRODUCTION_KEY_FILE="~/.ssh/id_rsa"
```

---

## 12 大能力中心

| # | 能力 | Agent | 说明 |
|---|------|-------|------|
| 1 | 🤖 **AI Copilot** | `AICopilot` | 运维问答、命令生成 |
| 2 | 🔍 **根因分析** | `LinuxAgent` | CPU/内存/磁盘/网络故障自动诊断 |
| 3 | 🔧 **自动修复** | `LinuxAgent` | 基于 Runbook 自主执行修复 |
| 4 | ☸️ **K8s Agent** | `K8sAgent` | Pod/Deployment/Node 故障诊断和管理 |
| 5 | 🗄️ **DB Agent** | `DBAgent` | MySQL/Redis/PostgreSQL/MongoDB 诊断 |
| 6 | 📋 **Log Agent** | `LogAgent` | 日志分析、错误链路追踪 |
| 7 | 📊 **Monitor Agent** | `MonitorAgent` | Prometheus/Grafana 监控分析 |
| 8 | 🔒 **Security Agent** | `SecurityAgent` | 安全巡检、入侵检测 |
| 9 | 🚀 **DevOps Agent** | `DevOpsAgent` | CI/CD、发布管理 |
| 10 | 🧠 **Multi-Agent** | `PlannerAgent` | 任务分解、多 Agent 协同 |
| 11 | 💾 **Memory Center** | `MemoryAgent` | 历史任务、故障经验、持续学习 |
| 12 | 📚 **Knowledge Center** | `KnowledgeAgent` | Runbook、RAG 检索、知识沉淀 |

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户层                                   │
│  CLI / API / Dashboard / Chat Interface                         │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Planner Agent (总控)                          │
│  任务分解 → Agent 调度 → 结果聚合 → 验证 → 学习                   │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Agent 层 (ReAct)                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Linux    │ │ K8s      │ │ DB       │ │ Log      │           │
│  │ Agent    │ │ Agent    │ │ Agent    │ │ Agent    │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Monitor  │ │ Security │ │ DevOps   │ │ Multi    │           │
│  │ Agent    │ │ Agent    │ │ Agent    │ │ Agent    │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP Marketplace (工具市场)                    │
│  SSH | K8s | Docker | MySQL | Redis | PostgreSQL | MongoDB     │
│  Prometheus | Grafana | Elasticsearch | Kafka                  │
│  AWS | Aliyun | Tencent | Terraform | Ansible | Helm           │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      基础设施层                                  │
│  本地服务器 | 容器 | Kubernetes | 云平台 (AWS/阿里云/腾讯云)       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 运维场景全覆盖

### 部署方式

| 场景 | 支持 | 说明 |
|------|------|------|
| **本地部署** | ✅ | 传统物理机/虚拟机 |
| **容器部署** | ✅ | Docker/Docker Compose |
| **Kubernetes** | ✅ | Pod/Deployment/Service/Node |
| **云平台** | ✅ | AWS/阿里云/腾讯云 |

### 数据库支持

| 数据库 | 支持 | 说明 |
|--------|------|------|
| **MySQL** | ✅ | 查询分析、慢查询、性能优化 |
| **Redis** | ✅ | 连接诊断、内存分析、持久化 |
| **PostgreSQL** | ✅ | 查询分析、索引优化 |
| **MongoDB** | ✅ | 集合分析、性能诊断 |
| **Elasticsearch** | ✅ | 索引分析、查询优化 |
| **Kafka** | ✅ | 消息队列监控、消费者组分析 |

### 运维领域

| 领域 | 支持 | 说明 |
|------|------|------|
| **系统运维** | ✅ | CPU/内存/磁盘/网络/进程 |
| **应用运维** | ✅ | 服务状态、日志分析、链路追踪 |
| **容器运维** | ✅ | Docker/K8s 故障诊断 |
| **数据库运维** | ✅ | 多数据库性能诊断 |
| **安全运维** | ✅ | 漏洞扫描、合规检查、入侵检测 |
| **云原生运维** | ✅ | 云平台资源管理、成本优化 |

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

# DB Agent (支持多种数据库)
aiops agent db --type mysql --symptom "查询慢"
aiops agent db --type redis --symptom "连接超时"
aiops agent db --type postgresql --symptom "慢查询"

# Security Agent
aiops agent security --host 10.0.0.1

# Log Agent
aiops agent log --host 10.0.0.1 --file /var/log/nginx/error.log --pattern "502"

# Multi-Agent 协同
aiops agent multi --goal "Pod CrashLoopBackOff 并查看日志和监控"

# 自动修复
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

## Tool Calling (MCP Marketplace)

### 系统工具

| 工具 | 功能 | 安全级别 |
|------|------|----------|
| `ssh_exec` | SSH 远程执行 | 需要确认 |
| `kubectl` / `k8s_*` | Kubernetes 管理（8个工具） | 部分需要确认 |
| `docker_*` | Docker 管理（7个工具） | 部分需要确认 |

### 数据库工具

| 工具 | 功能 | 安全级别 |
|------|------|----------|
| `mysql_query` | MySQL 查询 | 只读 |
| `redis_query` | Redis 命令 | 只读 |
| `postgresql_query` | PostgreSQL 查询 | 只读 |
| `mongodb_query` | MongoDB 查询 | 只读 |
| `elasticsearch_query` | Elasticsearch 查询 | 只读 |
| `kafka_query` | Kafka 管理 | 只读 |

### 云平台工具

| 工具 | 功能 | 安全级别 |
|------|------|----------|
| `aws_cli` | AWS CLI | 需要确认 |
| `aliyun_cli` | 阿里云 CLI | 需要确认 |
| `tencent_cli` | 腾讯云 CLI | 需要确认 |
| `terraform` | 基础设施管理 | 需要确认 |
| `ansible` | 自动化工具 | 需要确认 |
| `helm` | K8s 包管理 | 需要确认 |

---

## 核心能力

### Memory Center (记忆系统)

```
短期记忆: 当前会话上下文
长期记忆: 持久化存储
情景记忆: 故障事件记录
```

AI 每执行一次任务：

```
修复 Redis 连接问题
     ↓
记录步骤和结果
     ↓
记录成功率
     ↓
下次遇到类似问题直接调用
```

### Knowledge Center (知识库)

```
Runbook: 运维剧本
故障案例: 历史故障经验
官方文档: 技术文档
最佳实践: 运维规范
```

### RAG (检索增强生成)

```
问题: Redis 为什么连接失败？
     ↓
搜索知识库: 过去 100 次案例
     ↓
结合官方文档
     ↓
生成答案
```

### Workflow Engine (工作流引擎)

```
CPU 高
     ↓
检查 CPU
     ↓
是 Java？
     ↓
Dump
     ↓
分析线程
     ↓
重启
     ↓
验证
     ↓
结束
```

### Human Approval (人工审批)

```
AI 准备执行: systemctl restart mysql
     ↓
等待确认
     ↓
用户审批
     ↓
执行
```

危险命令全部需要审批：

- 删除操作
- 重启服务
- 扩容/缩容
- 版本升级
- 回滚操作

---

## 项目结构

```
aiops/
├── __init__.py              # 包初始化
├── cli.py                  # CLI 入口
├── core/                   # 核心引擎
│   ├── config.py           # 配置管理
│   ├── engine.py           # AIOps 引擎
│   ├── ssh_manager.py      # SSH 连接管理
│   ├── ai_agent.py         # AI 代理
│   └── security.py         # 安全验证
├── agents/                 # Agent 层（ReAct 循环）
│   ├── base.py             # BaseAgent
│   ├── planner.py          # 8个专业 Agent
│   └── copilot.py          # AI Copilot
├── tools/                  # Tool 层（MCP 工具）
│   ├── base.py             # 工具基类
│   ├── registry.py         # 工具注册中心
│   ├── ssh_tools.py        # SSH 工具
│   ├── k8s_tools.py        # Kubernetes 工具
│   ├── docker_tools.py     # Docker 工具
│   ├── database_tools.py   # 数据库工具
│   ├── cloud_tools.py      # 云平台工具
│   └── ...
├── memory/                 # 记忆系统
│   ├── base.py             # 记忆基类
│   ├── short_term.py       # 短期记忆
│   ├── long_term.py        # 长期记忆
│   └── episodic.py         # 情景记忆
├── knowledge/              # 知识库系统
│   ├── base.py             # 知识库基类
│   └── runbooks.py         # Runbook 管理
├── rag/                    # RAG 检索增强生成
│   ├── base.py             # RAG 基类
│   └── engine.py           # RAG 引擎
├── workflow/               # 工作流引擎
│   ├── base.py             # 工作流基类
│   └── engine.py           # 工作流引擎
├── approval/               # 审批系统
│   ├── base.py             # 审批基类
│   └── manager.py          # 审批管理器
├── eventbus/               # 事件总线
│   ├── base.py             # 事件基类
│   └── bus.py              # 事件总线
├── planner/                # 任务规划器
│   ├── base.py             # 规划器基类
│   ├── react_planner.py    # ReAct 规划器
│   └── multi_agent.py      # 多 Agent 规划器
├── mcp/                    # MCP 工具市场
│   ├── base.py             # MCP 基类
│   └── marketplace.py      # 工具市场
├── modules/                # 功能模块
├── collectors/             # 数据采集
├── analyzers/              # 分析引擎
├── reporters/              # 报告生成
├── api/                    # API 接口
├── ui/                     # Web UI
└── runbooks/               # 运维剧本
```

---

## 配置示例

```yaml
# config.yaml
servers:
  - name: production
    host: 10.0.0.1
    port: 22
    user: root
    # 密码建议使用环境变量

  - name: staging
    host: 10.0.0.2
    port: 22
    user: deploy

ai:
  enabled: true
  provider: deepseek
  # api_key 建议使用环境变量
  model: deepseek-chat

security:
  blocked_commands:
    - rm -rf
    - shutdown
    - mkfs
  max_output_size: 10000
  audit_logging: true

approval:
  auto_approve_threshold: low
  require_approval_for:
    - restart
    - delete
    - scale
    - upgrade
```

---

## 路线图

| Version | Feature | 状态 |
|---------|---------|------|
| v1.0 | AI Copilot | ✅ |
| v1.1 | Linux Agent | ✅ |
| v1.2 | Kubernetes Agent | ✅ |
| v1.3 | Planner Agent | ✅ |
| v2.0 | 多数据库支持 | ✅ |
| v2.1 | 安全增强 | ✅ |
| v3.0 | Memory + Knowledge | 🚧 |
| v3.1 | RAG 检索增强 | 🚧 |
| v3.2 | Workflow Engine | 🚧 |
| v3.3 | Approval Center | 🚧 |
| v4.0 | Multi-Agent 协同 | 📋 |
| v4.1 | Event Bus 事件驱动 | 📋 |
| v4.2 | MCP Marketplace | 📋 |
| v5.0 | Web Dashboard | 📋 |
| v5.1 | API 接口 | 📋 |

---

## 开发指南

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black aiops/
```

### 类型检查

```bash
mypy aiops/
```

---

## License

MIT License

---

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 作者: Neal
- 仓库: https://gitee.com/neal4752/agentic-aiops
