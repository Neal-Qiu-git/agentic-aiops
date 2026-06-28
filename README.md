# Agentic AIOps - 智能运维平台

<div align="center">

🤖 **AI 驱动的一站式运维工具平台**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

## 简介

Agentic AIOps 是一个**全方位智能运维平台**，结合 AI 大模型能力与实用运维工具，覆盖服务器健康巡检、事件分诊、日志诊断、安全扫描、性能监控、自动修复等全流程运维场景。

灵感来源于 [Hermes Agent](https://github.com/hermes-agent) 的 AIOps Skills 体系，将 AI 驱动的运维方法论落地为可部署的独立工具。

## 核心特性

| 模块 | 功能 | 命令 |
|------|------|------|
| 🏥 健康巡检 | 全面检查 CPU/内存/磁盘/网络/服务状态 | `aiops check` |
| 🚨 事件分诊 | 5分钟内判定事件严重级别和影响范围 | `aiops triage` |
| 📋 日志诊断 | 智能扫描日志，匹配错误模式 | `aiops logs` |
| 🔍 环境发现 | 自动发现服务器环境和资产清单 | `aiops discover` |
| 🔒 安全扫描 | SSH配置/端口暴露/弱密码/合规检查 | `aiops security` |
| 📊 性能监控 | 实时性能数据展示 | `aiops monitor` |
| 💰 成本优化 | 资源使用分析和优化建议 | `aiops cost` |
| ✅ 合规检查 | 安全基线合规审计 | `aiops compliance` |
| 🔧 自动修复 | 基于 Runbook 的智能自动修复 | `aiops remediate` |
| 🤖 AI 分析 | LLM 驱动的深度分析和建议 | `aiops analyze` |

## 快速开始

### 安装

```bash
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
pip install -e .
```

### 使用

```bash
# 健康巡检
aiops check --host your-server --user root

# 事件分诊
aiops triage --host your-server --symptom "服务响应慢"

# 安全扫描
aiops security --host your-server

# 环境发现
aiops discover --host your-server

# 生成报告
aiops check --host your-server --format markdown --output report.md
```

## 架构

```
agentic-aiops/
├── aiops/
│   ├── cli.py              # CLI 入口
│   ├── core/               # 核心引擎
│   │   ├── engine.py       # 调度引擎
│   │   ├── ssh_manager.py  # SSH 连接管理
│   │   ├── ai_agent.py     # AI 代理
│   │   └── config.py       # 配置管理
│   ├── modules/            # 功能模块
│   ├── collectors/         # 数据采集器
│   ├── analyzers/          # 分析引擎
│   ├── reporters/          # 报告生成
│   └── plugins/            # 插件系统
├── runbooks/               # 运维手册
└── tests/                  # 测试
```

## AI 集成

支持接入 LLM API 进行智能分析：

```yaml
# config.yaml
ai:
  enabled: true
  provider: deepseek
  api_key: your-api-key
  model: deepseek-chat
  base_url: https://api.deepseek.com/v1
```

## 与 Hermes Skills 的关系

| 本项目模块 | Hermes Skill |
|-----------|-------------|
| `health_check` | `aiops/health-check` |
| `incident_triage` | `aiops/incident-triage` |
| `log_diagnosis` | `aiops/log-diagnosis` |
| `env_discovery` | `aiops/env-discovery` |
| `auto_remediation` | `aiops/ops-automation-agent` |
| `security_scan` | `security/security-review` |

## License

MIT License
