# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [4.3.0] - 2026-07-04

### 🔭 可观测性全覆盖 (基于行业真实技术栈)

#### 新增工具文件 (8 个, 50 个工具)
- ✅ **Grafana API** (4): Dashboard 管理/数据源查询/标注/告警规则
- ✅ **Loki LogQL** (4): 日志查询/标签/时间序列 (K8s 日志标准)
- ✅ **Alertmanager** (3): 活跃告警/静默管理/状态查询
- ✅ **APM 工具** (4): SkyWalking 服务拓扑/指标 + Jaeger 分布式追踪 + OTel Collector
- ✅ **Terraform IaC** (6): init/plan/apply/state/output/validate
- ✅ **GitOps** (5): ArgoCD 应用/项目/仓库 + FluxCD 资源/重同步
- ✅ **CI/CD** (3): Jenkins 作业 + GitLab CI 流水线 + GitHub Actions
- ✅ **安全扫描** (6): Trivy 漏洞/Falco 运行时/OPA 策略/kube-bench/Kubescape
- ✅ **FinOps** (4): Kubecost 资源分配/资产 + AWS 成本 + Azure 成本
- ✅ **企业数据库** (6): Oracle + ClickHouse + TiDB + 达梦DM8 + OceanBase + KingbaseES
- ✅ **扩展中间件** (5): Pulsar + NATS + Traefik + HAProxy + Consul
- ✅ **新 ToolCategory** (9): GITOPS/IAC/APM/CICD/PROFILING/FINOPS/VAULT/MESSAGE_QUEUE/REVERSE_PROXY

#### 工具总计
- v4.2.0: 65 个工具 → v4.3.0: **115 个工具** (+50)

---

## [4.1.0] - 2026-07-04

### 🎉 第一个正式版本

#### 核心架构
- ✅ 12 个专业运维智能体（Linux/K8s/DB/Log/Monitor/Security/SRE/Cost/Incident/DevOps/CMDB/Planner）
- ✅ ReAct 生命周期：观察 → 推理 → 计划 → 执行 → 验证 → 学习
- ✅ 事件总线（Event Bus）解耦式智能体协作

#### 工具与集成
- ✅ MCP 工具市场，20+ 预置工具
- ✅ 插件化架构，支持自定义 MCP 工具
- ✅ SSH 远程命令执行

#### 记忆与知识
- ✅ 5 类记忆系统（工作/短期/长期/语义/情景）
- ✅ 知识库 RAG 语义检索
- ✅ Runbook 自动匹配

#### 工作流
- ✅ YAML 声明式工作流引擎
- ✅ 支持串行/并行/条件分支
- ✅ 10 个预置工作流模板

#### 安全与审批
- ✅ 人工审批（HITL）工作流节点
- ✅ 命令黑名单安全过滤
- ✅ 敏感路径保护
- ✅ 审计日志

#### 部署
- ✅ Docker 一键部署
- ✅ Kubernetes Helm Chart
- ✅ pip 安装
- ✅ 一键部署脚本（deploy.sh）

#### API 与 CLI
- ✅ REST API（OpenAPI 规范）
- ✅ 全功能 CLI

---

## [4.0.0] - 2026-06-01

### 重构版本
- 从 v3.x 全面重构
- 引入 MCP 工具系统
- 新增记忆系统
- 新增知识库 RAG

---

## [3.x] - 2026-03-01

### 平台化
- 新增工作流引擎
- 新增审批系统
- 新增 REST API

---

## [2.x] - 2025-12-01

### 智能化
- 引入 5 类记忆系统
- 新增知识库
- 支持多 LLM 提供商

---

## [1.x] - 2025-06-01

### 基础版本
- 核心 Agent 实现
- CLI 界面
- MCP 工具系统
- 基础记忆
