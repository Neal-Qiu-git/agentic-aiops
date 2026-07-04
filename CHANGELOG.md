# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [5.3.0] - 2026-07-04

### 🏗️ Dashboard 重构为平台介绍 + 代码修复

#### Dashboard 重定位
- 仪表盘从实时数据页改为 **4 Tab 平台介绍页**（平台概览/使用指南/Agent网络/智能体&工具）
- Agent 网络和智能体&工具从侧边栏移除，内容整合到仪表盘分页

#### 代码质量修复
- ✅ 修复 `k8s_tools.py` 重复 key 语法错误（`"cpu": "cpu": "45%"`）
- ✅ 修复 `mysql_tools.py` f-string 引号嵌套错误
- ✅ 修复 `windows_tools.py` 3处 PowerShell 命令引号冲突
- ✅ 新增后端 `/api/v1/cost/summary` 和 `/api/v1/security/summary` 端点
- ✅ 移除 `DashboardPage.tsx` 未使用的 `agents` 导入
- ✅ 删除 4 个废弃页面文件（NetworksPage、AgentsPage、AlertPage旧、MulticloudPage）
- ✅ `package.json` 版本号更新为 5.3.0
- ✅ `agents.ts` 工具计数注释更新为 148+
- ✅ App.tsx 改为 `React.lazy` + `Suspense` 代码分割，首屏加载更快

#### README
- 中英文 README 全面更新至 v5.3.0

---

## [5.2.0] - 2026-07-04

### 📊 仪表盘重构为平台介绍页
- 仪表盘改为 4 Tab：平台概览、使用指南、Agent 网络、智能体&工具
- 平台概览含 Hero + 核心能力 + 指标 + 快速入口
- 使用指南含 CLI 命令 + 环境拓扑 + API 端点
- Agent 网络含 5 层架构 + 通信链路 + 数据流向
- 智能体&工具含 10 类工具 + 智能体目录

---

## [5.1.0] - 2026-07-04

### 🔄 多云概览合并到环境管理
- 多云概览的账户/费用数据合并为 EnvironmentsPage 第三个 Tab「多云账户」
- 页面数 17→16，消除重叠
- 后端补全 6 个缺失 API 端点（slo/events/workflows/network/multicloud/audit）

---

## [5.0.0] - 2026-07-04

### 🏢 企业级 Dashboard 升级
- 新增 3 个企业页面：数据源配置、审计日志、系统设置
- 侧边栏重构为 6 组（概览/运维/安全&成本/配置/开发/系统）
- 告警中心、成本分析、安全态势全面升级为 API 驱动

---

## [4.8.1] - 2026-07-04

### 📡 API 驱动升级（多云 + 网络）
- 多云概览页面改为 API + Demo 双模式
- Agent 网络拓扑改为 API 驱动

---

## [4.8.0] - 2026-07-04

### 📡 API 驱动升级（SLO + 事件）
- SLO 仪表盘从静态数据改为 API + Demo 双模式
- 事件日志从静态数据改为 API + Demo 双模式

---

## [4.7.1] - 2026-07-04

### 🐛 黑屏修复
- 修复 DeploymentPage 和 MonitoringPage 黑屏问题
- 根因：`fetchPods()` 返回对象直接赋值给数组状态 + 字段名不匹配

---

## [4.7.0] - 2026-07-04

### 🔌 核心页面接入真实 API
- 告警中心、成本分析、安全态势升级为 API 驱动
- 支持 live/demo 模式自动切换，15秒刷新
- 新增 `api.ts` 统一数据获取层

---

## [4.6.0] - 2026-07-04

### 📊 仪表盘升级
- 仪表盘重写为平台介绍 + 操作指引 + 实时状态
- 包含核心指标、资源概览、告警快览、快速入口

---

## [4.5.0] - 2026-07-04

### 🔧 P1 全量补全 - 新兴技术 + 小众场景

#### 新增工具 (9 个)
- ✅ **containerd** — K8s 默认容器运行时 (CNCF 毕业)
- ✅ **Podman** — Red Hat 无守护进程容器
- ✅ **WildFly** — Red Hat Java 应用服务器 (JBoss)
- ✅ **Caddy** — 现代自动 HTTPS Web 服务器
- ✅ **Grafana Mimir** — Prometheus 长期存储 (CNCF 孵化)
- ✅ **Pyroscope** (2) — 持续性能分析 (CNCF 孵化)
- ✅ **DynamoDB** — AWS 原生 NoSQL
- ✅ **GCP Cost** — Google Cloud 成本分析

#### 工具总计
- v4.4.0: 139 → v4.5.0: **148 个工具** (+9)
- 覆盖率: 100% (所有主流 + 新兴技术)

---

## [4.4.0] - 2026-07-04

### 🏢 企业级补全 - 基于行业对标审查修复 17 项缺失

#### P0 关键修复
- ✅ **AWS CLI** — 全球 #1 云 (市占 31%), 补全 EC2/S3/RDS/Lambda/EKS/IAM
- ✅ **GCP CLI** — 全球 #3 云 (市占 11%), 补全 GKE/Cloud SQL/GCE/Cloud Run
- ✅ **Vault** (6 工具) — 密钥管理事实标准 (KV/租约/策略/引擎)
- ✅ **Helm** (4 工具) — K8s 包管理事实标准 (list/status/history/rollback)
- ✅ **Ansible** (3 工具) — 最流行配置管理 (adhoc/playbook/inventory)
- ✅ **Harbor** — CNCF 毕业项目, K8s 容器镜像仓库
- ✅ **Redis Cluster** (5 工具) — 从 1 个工具增强到 5 个 (info/slowlog/cluster/key分析/sentinel)

#### P1 重要补充
- ✅ **OpenStack** (3 工具) — 私有云事实标准 (server/network/volume)
- ✅ **Cassandra** — 分布式 NoSQL (Netflix/Apple 大规模使用)
- ✅ **Grafana Tempo** (2 工具) — CNCF 孵化, 分布式追踪
- ✅ **Cert-Manager** — CNCF 孵化, K8s TLS 证书管理
- ✅ **MetalLB** — CNCF 毕业, K8s 裸金属负载均衡
- ✅ **SonarQube** (2 工具) — 代码质量/安全扫描标准

#### 工具总计
- v4.3.0: 108 个工具 → v4.4.0: **139 个工具** (+31)

---

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
