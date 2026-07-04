
export interface Agent {
  id: string;
  name: string;
  icon: string;
  description: string;
  status: 'active' | 'idle' | 'error';
  color: string;
  tasks: number;
  successRate: number;
  avgResponseTime: string;
  category: string;
}

export const agents: Agent[] = [
  { id: 'planner', name: 'Planner Agent', icon: '📋', description: '任务规划调度 · 总控中心', status: 'active', color: '#eab308', tasks: 4521, successRate: 97.1, avgResponseTime: '1.5s', category: 'core' },
  { id: 'linux', name: 'Linux Agent', icon: '🐧', description: 'Linux 系统诊断与性能分析', status: 'active', color: '#10b981', tasks: 1247, successRate: 96.5, avgResponseTime: '2.3s', category: 'infra' },
  { id: 'k8s', name: 'K8s Agent', icon: '☸️', description: 'Kubernetes 运维管理', status: 'active', color: '#3b82f6', tasks: 892, successRate: 94.2, avgResponseTime: '3.1s', category: 'infra' },
  { id: 'docker', name: 'Docker Agent', icon: '🐳', description: 'Docker/containerd 容器运维', status: 'active', color: '#0ea5e9', tasks: 1024, successRate: 96.8, avgResponseTime: '1.9s', category: 'infra' },
  { id: 'cloud', name: 'Cloud Agent', icon: '☁️', description: '多云管理 (AWS/Azure/GCP/阿里/华为/腾讯)', status: 'active', color: '#f97316', tasks: 756, successRate: 94.5, avgResponseTime: '3.8s', category: 'cloud' },
  { id: 'windows', name: 'Windows Agent', icon: '🪟', description: 'Windows Server 运维 (WinRM/PowerShell)', status: 'idle', color: '#06b6d4', tasks: 423, successRate: 95.2, avgResponseTime: '2.5s', category: 'infra' },
  { id: 'virtual', name: 'Virtual Agent', icon: '🖥️', description: '虚拟化运维 (VMware/KVM/Proxmox/OpenStack)', status: 'idle', color: '#84cc16', tasks: 298, successRate: 97.5, avgResponseTime: '2.0s', category: 'infra' },
  { id: 'db', name: 'DB Agent', icon: '🗄️', description: '数据库诊断优化 (MySQL/PG/Oracle/Redis/ES/DM8/TiDB/ClickHouse)', status: 'active', color: '#8b5cf6', tasks: 634, successRate: 97.8, avgResponseTime: '1.8s', category: 'data' },
  { id: 'log', name: 'Log Agent', icon: '📋', description: '日志分析 (Loki/ELK/Grep/SkyWalking)', status: 'idle', color: '#f59e0b', tasks: 2156, successRate: 92.1, avgResponseTime: '1.2s', category: 'monitor' },
  { id: 'monitor', name: 'Monitor Agent', icon: '📊', description: '监控分析 (Prometheus/Grafana/OTel)', status: 'active', color: '#06b6d4', tasks: 1580, successRate: 95.3, avgResponseTime: '0.8s', category: 'monitor' },
  { id: 'apm', name: 'APM Agent', icon: '🔍', description: '应用性能追踪 (SkyWalking/Jaeger/OTel)', status: 'idle', color: '#6366f1', tasks: 387, successRate: 94.6, avgResponseTime: '1.5s', category: 'monitor' },
  { id: 'security', name: 'Security Agent', icon: '🔒', description: '安全扫描 (Trivy/Falco/OPA/Kubescape)', status: 'active', color: '#ef4444', tasks: 456, successRate: 99.1, avgResponseTime: '4.2s', category: 'security' },
  { id: 'sre', name: 'SRE Agent', icon: '🏥', description: 'SLI/SLO/错误预算管理', status: 'idle', color: '#ec4899', tasks: 328, successRate: 93.7, avgResponseTime: '2.0s', category: 'ops' },
  { id: 'cost', name: 'FinOps Agent', icon: '💰', description: '成本优化 (Kubecost/AWS/Azure)', status: 'idle', color: '#14b8a6', tasks: 189, successRate: 91.4, avgResponseTime: '5.1s', category: 'ops' },
  { id: 'incident', name: 'Incident Agent', icon: '🚨', description: '事件管理与自动响应', status: 'active', color: '#f97316', tasks: 567, successRate: 88.9, avgResponseTime: '3.5s', category: 'ops' },
  { id: 'devops', name: 'DevOps Agent', icon: '🚀', description: 'CI/CD (Jenkins/GitLab CI/GitHub Actions)', status: 'idle', color: '#a855f7', tasks: 423, successRate: 95.6, avgResponseTime: '2.7s', category: 'dev' },
  { id: 'gitops', name: 'GitOps Agent', icon: '🔀', description: 'GitOps 部署 (ArgoCD/FluxCD)', status: 'idle', color: '#8b5cf6', tasks: 312, successRate: 96.3, avgResponseTime: '2.2s', category: 'dev' },
  { id: 'iac', name: 'IaC Agent', icon: '🏗️', description: '基础设施即代码 (Terraform/Ansible)', status: 'idle', color: '#64748b', tasks: 245, successRate: 97.8, avgResponseTime: '3.0s', category: 'dev' },
  { id: 'network', name: 'Network Agent', icon: '🌐', description: '网络运维 (防火墙/LB/DNS/VPN)', status: 'active', color: '#14b8a6', tasks: 612, successRate: 96.8, avgResponseTime: '1.8s', category: 'infra' },
  { id: 'middleware', name: 'Middleware Agent', icon: '📦', description: '中间件 (Nginx/Tomcat/Kafka/RabbitMQ/Pulsar/NATS/Traefik)', status: 'active', color: '#a855f7', tasks: 834, successRate: 95.9, avgResponseTime: '2.1s', category: 'infra' },
  { id: 'servicemesh', name: 'ServiceMesh Agent', icon: '🔗', description: '服务网格 (Istio/Linkerd/Cilium)', status: 'idle', color: '#6366f1', tasks: 156, successRate: 93.2, avgResponseTime: '2.8s', category: 'infra' },
  { id: 'cmdb', name: 'CMDB Agent', icon: '📦', description: '配置管理数据库', status: 'idle', color: '#64748b', tasks: 78, successRate: 98.2, avgResponseTime: '0.5s', category: 'data' },
  { id: 'copilot', name: 'AI Copilot', icon: '🤖', description: 'AI 对话助手 · 自然语言运维', status: 'active', color: '#3b82f6', tasks: 2890, successRate: 96.8, avgResponseTime: '1.0s', category: 'core' },
];

// Tool categories (v4.3.0 - 115 tools)
export const toolCategories = [
  { name: '可观测性', icon: '🔭', count: 24, tools: ['Prometheus (5)', 'Grafana (4)', 'Loki (4)', 'Alertmanager (3)', 'APM (4)', 'OTel (1)'], color: '#3b82f6' },
  { name: '数据库', icon: '🗄️', count: 21, tools: ['MySQL', 'Redis', 'PostgreSQL', 'MongoDB', 'ES', 'Oracle', 'ClickHouse', 'TiDB', 'DM8', 'OceanBase', 'KingbaseES', 'Kafka'], color: '#8b5cf6' },
  { name: '云平台', icon: '☁️', count: 4, tools: ['AWS', 'Azure', '阿里云', '腾讯云', '华为云'], color: '#f97316' },
  { name: '容器/K8s', icon: '🐳', count: 27, tools: ['K8s (12)', 'Docker (7)', 'Kubectl (1)'], color: '#0ea5e9' },
  { name: '中间件', icon: '📦', count: 11, tools: ['Nginx', 'Tomcat', 'RabbitMQ', 'Kafka', 'TongWeb', 'Pulsar', 'NATS', 'Traefik', 'HAProxy', 'Consul'], color: '#a855f7' },
  { name: '安全', icon: '🔒', count: 7, tools: ['Trivy', 'Falco', 'OPA', 'kube-bench', 'Kubescape'], color: '#ef4444' },
  { name: 'CI/CD', icon: '🚀', count: 3, tools: ['Jenkins', 'GitLab CI', 'GitHub Actions'], color: '#10b981' },
  { name: 'GitOps', icon: '🔀', count: 5, tools: ['ArgoCD (3)', 'FluxCD (2)'], color: '#8b5cf6' },
  { name: 'IaC', icon: '🏗️', count: 6, tools: ['Terraform (6)'], color: '#64748b' },
  { name: 'FinOps', icon: '💰', count: 4, tools: ['Kubecost (2)', 'AWS Cost', 'Azure Cost'], color: '#14b8a6' },
  { name: '网络', icon: '🌐', count: 6, tools: ['Firewall', 'LoadBalancer', 'DNS', 'NetworkDiag', 'VPN'], color: '#06b6d4' },
  { name: '虚拟化', icon: '🖥️', count: 3, tools: ['VMware', 'KVM', 'Proxmox'], color: '#84cc16' },
  { name: '远程管理', icon: '🪟', count: 3, tools: ['WinRM Exec', 'EventLog', 'Service'], color: '#06b6d4' },
  { name: '密钥管理', icon: '🔐', count: 6, tools: ['Vault (6)'], color: '#ef4444' },
  { name: '配置管理', icon: '⚙️', count: 3, tools: ['Ansible AdHoc', 'Playbook', 'Inventory'], color: '#f59e0b' },
  { name: '代码质量', icon: '🔍', count: 2, tools: ['SonarQube Scan', 'Status'], color: '#10b981' },
  { name: '日志', icon: '📋', count: 1, tools: ['LogSearch'], color: '#f59e0b' },
  { name: 'SSH', icon: '🔑', count: 3, tools: ['SSH Exec', 'Test', 'SystemInfo'], color: '#10b981' },
];

// Network topology connections
export const connections = [
  { source: 'planner', target: 'linux', label: '调度' },
  { source: 'planner', target: 'k8s', label: '调度' },
  { source: 'planner', target: 'docker', label: '调度' },
  { source: 'planner', target: 'db', label: '调度' },
  { source: 'planner', target: 'log', label: '调度' },
  { source: 'planner', target: 'monitor', label: '调度' },
  { source: 'planner', target: 'security', label: '调度' },
  { source: 'planner', target: 'cloud', label: '调度' },
  { source: 'planner', target: 'windows', label: '调度' },
  { source: 'planner', target: 'network', label: '调度' },
  { source: 'planner', target: 'middleware', label: '调度' },
  { source: 'planner', target: 'servicemesh', label: '调度' },
  { source: 'planner', target: 'virtual', label: '调度' },
  { source: 'planner', target: 'gitops', label: '调度' },
  { source: 'planner', target: 'iac', label: '调度' },
  { source: 'planner', target: 'apm', label: '调度' },
  { source: 'cloud', target: 'monitor', label: '指标' },
  { source: 'middleware', target: 'log', label: '日志' },
  { source: 'network', target: 'security', label: '策略' },
  { source: 'virtual', target: 'monitor', label: '指标' },
  { source: 'linux', target: 'monitor', label: '数据' },
  { source: 'k8s', target: 'monitor', label: '指标' },
  { source: 'docker', target: 'monitor', label: '指标' },
  { source: 'db', target: 'log', label: '日志' },
  { source: 'log', target: 'incident', label: '告警' },
  { source: 'monitor', target: 'sre', label: 'SLO' },
  { source: 'apm', target: 'sre', label: '追踪' },
  { source: 'incident', target: 'devops', label: '修复' },
  { source: 'gitops', target: 'devops', label: '同步' },
  { source: 'iac', target: 'cloud', label: '编排' },
  { source: 'security', target: 'cmdb', label: '资产' },
  { source: 'cost', target: 'cmdb', label: '成本' },
  { source: 'copilot', target: 'planner', label: '对话' },
];

// Recent events (v4.3.0 - more diverse)
export const events = [
  { time: '08:32', type: 'success', title: 'Prometheus 查询完成', desc: 'Monitor Agent 通过 Prometheus API 获取全集群 CPU/内存趋势', agent: 'monitor' },
  { time: '08:30', type: 'warning', title: 'Trivy 漏洞扫描', desc: 'Security Agent 发现 nginx:1.21 镜像存在 2 个 HIGH CVE', agent: 'security' },
  { time: '08:28', type: 'info', title: 'Loki 日志分析', desc: 'Log Agent 使用 LogQL 查询 production 命名空间最近 1h 错误日志', agent: 'log' },
  { time: '08:25', type: 'success', title: 'Terraform Plan 完成', desc: 'IaC Agent 预览基础设施变更: 3 个新增, 1 个修改', agent: 'iac' },
  { time: '08:22', type: 'info', title: 'ArgoCD 同步', desc: 'GitOps Agent 触发 production 应用同步，版本 v2.3.1', agent: 'gitops' },
  { time: '08:20', type: 'error', title: 'K8s Pod 异常', desc: 'K8s Agent 检测到 gateway Pod CrashLoopBackOff，自动重启', agent: 'k8s' },
  { time: '08:18', type: 'success', title: 'SkyWalking 拓扑', desc: 'APM Agent 查询服务拓扑，12 个微服务调用链正常', agent: 'apm' },
  { time: '08:15', type: 'info', title: 'Kubecost 报告', desc: 'FinOps Agent 生成命名空间成本分配，开发环境超标 15%', agent: 'cost' },
  { time: '08:12', type: 'warning', title: 'ClickHouse 慢查询', desc: 'DB Agent 检测到 3 条超过 10s 的 OLAP 查询', agent: 'db' },
  { time: '08:10', type: 'success', title: 'Jenkins 构建', desc: 'DevOps Agent 触发 microservice-api 构建，流水线 #1247', agent: 'devops' },
];

// ── 工作流数据类型 ──
export interface WorkflowStep {
  name: string;
  agent: string;
  tool?: string;
  status: 'completed' | 'running' | 'pending' | 'error' | 'skipped';
  duration: string;
  input?: string;
  output?: string;
}

export interface Workflow {
  id: string;
  name: string;
  description: string;
  category: 'incident' | 'deploy' | 'optimize' | 'security' | 'compliance' | 'provision';
  trigger: 'alert' | 'schedule' | 'manual' | 'webhook' | 'api';
  status: 'completed' | 'running' | 'pending' | 'error';
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  agents: string[];
  avgDuration: string;
  successRate: number;
  totalRuns: number;
  lastRun: string;
  triggeredAt?: string;
  completedAt?: string | null;
  steps: WorkflowStep[];
}

// ── 10 条企业级真实工作流 ──
export const workflowTemplates: Workflow[] = [
  // 1. Pod 故障自愈
  {
    id: 'wf-1', name: 'Pod 故障自愈', category: 'incident', trigger: 'alert', priority: 'P0',
    description: 'Prometheus 检测到 Pod CrashLoopBackOff → 自动诊断根因 → 执行修复 → 验证恢复',
    status: 'completed', agents: ['monitor', 'log', 'k8s', 'linux', 'sre'],
    avgDuration: '8s', successRate: 94.2, totalRuns: 237, lastRun: '08:32',
    steps: [
      { name: 'Prometheus 告警触发', agent: 'monitor', tool: 'prometheus_range', status: 'completed', duration: '0.3s',
        input: 'ALERT{kubernetes_pod_status_phase="CrashLoopBackOff"}',
        output: '3 个 Pod 异常: gateway-7f8d, order-svc-3b2c, pay-svc-9e1a' },
      { name: '容器日志采集', agent: 'log', tool: 'loki_query', status: 'completed', duration: '1.2s',
        input: 'logql: {namespace="production"} |= "error" | logfmt | level="error"',
        output: 'OOMKilled: gateway-7f8d 内存超限 (512Mi → 实际使用 680Mi)' },
      { name: '节点资源诊断', agent: 'linux', tool: 'ssh_exec', status: 'completed', duration: '0.8s',
        input: 'free -h && df -h && top -bn1 | head -20',
        output: 'node-03: 内存使用 87%, 磁盘 62%, 负载 4.2' },
      { name: 'K8s 根因定位', agent: 'k8s', tool: 'k8s_pod_events', status: 'completed', duration: '1.5s',
        input: 'kubectl describe pod gateway-7f8d -n production',
        output: '根因: 内存 limits 过低 (512Mi), 建议调整至 1Gi' },
      { name: '自动修复执行', agent: 'k8s', tool: 'k8s_scale_deployment', status: 'completed', duration: '2.1s',
        input: 'kubectl patch deploy gateway -n production -p \'{"spec":{"template":{"spec":{"containers":[{"name":"gateway","resources":{"limits":{"memory":"1Gi"}}}]}}}}\'',
        output: 'Deployment updated, 3/3 replicas ready' },
      { name: 'SLO 恢复验证', agent: 'sre', tool: 'prometheus_range', status: 'completed', duration: '2.5s',
        input: 'SLI: availability=gateway-success/gateway-total, 窗口=5min',
        output: 'Availability: 99.97% (target: 99.95%) ✅ SLO 恢复' },
    ],
    triggeredAt: '08:32:01', completedAt: '08:32:09',
  },
  // 2. GitOps 灰度发布
  {
    id: 'wf-2', name: 'GitOps 灰度发布', category: 'deploy', trigger: 'webhook', priority: 'P1',
    description: '代码推送到 main → 镜像安全扫描 → 灰度部署 10% → APM 验证 → 逐步放量至 100%',
    status: 'running', agents: ['gitops', 'security', 'devops', 'apm', 'sre'],
    avgDuration: '15min', successRate: 97.1, totalRuns: 186, lastRun: '08:30',
    steps: [
      { name: 'ArgoCD 检测 Git 变更', agent: 'gitops', tool: 'argocd_app_list', status: 'completed', duration: '0.3s',
        input: 'repo: microservice-api, branch: main, commit: a3f2e1d',
        output: 'Sync state: OutOfSync, 目标版本: v2.4.1' },
      { name: 'Trivy 镜像漏洞扫描', agent: 'security', tool: 'trivy_image_scan', status: 'completed', duration: '4.5s',
        input: 'image: registry.internal/microservice-api:v2.4.1',
        output: 'CRITICAL: 0, HIGH: 1 (CVE-2024-xxxx, OpenSSL), MEDIUM: 3 → 通过门禁' },
      { name: 'SonarQube 代码质量检查', agent: 'devops', tool: 'sonarqube_status', status: 'completed', duration: '2.8s',
        input: 'project: microservice-api, quality gate: "Bank Standard"',
        output: 'Quality Gate: PASSED (覆盖率 82%, 重复率 1.2%, Bug 0)' },
      { name: '灰度部署 10% 流量', agent: 'gitops', tool: 'argocd_sync', status: 'completed', duration: '1.2s',
        input: 'canary weight: 10%, namespace: production',
        output: 'VirtualService updated: 10% → canary, 90% → stable' },
      { name: 'APM 黄金指标验证', agent: 'apm', tool: 'skywalking_metrics', status: 'running', duration: '-',
        input: 'service: microservice-api, window: 5min, metrics: latency/p50,p99/error_rate',
        output: '-' },
      { name: '全量发布', agent: 'gitops', tool: 'argocd_sync', status: 'pending', duration: '-',
        input: 'canary weight: 100%', output: '-' },
      { name: 'SLO 基线确认', agent: 'sre', tool: 'prometheus_range', status: 'pending', duration: '-',
        input: 'SLI: api-latency-p99 < 200ms', output: '-' },
    ],
    triggeredAt: '08:30:15', completedAt: null,
  },
  // 3. 数据库慢查询优化
  {
    id: 'wf-3', name: '数据库慢查询自动优化', category: 'optimize', trigger: 'alert', priority: 'P1',
    description: 'Prometheus 检测慢查询告警 → 分析执行计划 → 生成索引建议 → 审批 → 执行优化 → 验证',
    status: 'completed', agents: ['monitor', 'db', 'planner', 'linux'],
    avgDuration: '12s', successRate: 96.5, totalRuns: 89, lastRun: '10:15',
    steps: [
      { name: '慢查询告警触发', agent: 'monitor', tool: 'prometheus_range', status: 'completed', duration: '0.5s',
        input: 'mysql_global_status_slow_queries rate(5m) > 10',
        output: '慢查询数: 47/min, 涉及 3 条 SQL, 最长 12.3s' },
      { name: 'ClickHouse 执行计划分析', agent: 'db', tool: 'clickhouse_query', status: 'completed', duration: '2.1s',
        input: 'EXPLAIN ANALYZE SELECT * FROM orders WHERE merchant_id=12345 ORDER BY created_at DESC LIMIT 50',
        output: '全表扫描 (rows=2,340,000), 无索引覆盖 merchant_id+created_at' },
      { name: '索引优化建议', agent: 'db', tool: 'mysql_explain', status: 'completed', duration: '1.8s',
        input: 'MySQL slow_log + 执行计划综合分析',
        output: '建议: CREATE INDEX idx_orders_merchant_time ON orders(merchant_id, created_at DESC)' },
      { name: 'Planner 评估影响', agent: 'planner', tool: 'prometheus_range', status: 'completed', duration: '1.5s',
        input: '评估: 建索引耗时 45s, 锁表风险低, 回滚方案: DROP INDEX',
        output: '风险评估: LOW, 建议在业务低峰期执行 (当前凌晨 02:00)' },
      { name: 'Ansible 执行建索引', agent: 'linux', tool: 'ansible_playbook', status: 'completed', duration: '38.2s',
        input: 'ansible-playbook create-index.yml -e "sql=CREATE INDEX..."',
        output: '索引创建完成, 耗时 42s, 表行数 2,340,000' },
      { name: '查询性能验证', agent: 'db', tool: 'mysql_explain', status: 'completed', duration: '1.2s',
        input: '同一 SQL 再次执行 EXPLAIN',
        output: '索引命中: idx_orders_merchant_time, 扫描行数: 50, 耗时: 0.03s (优化前: 12.3s)' },
    ],
    triggeredAt: '10:15:00', completedAt: '10:15:12',
  },
  // 4. 多云资源编排
  {
    id: 'wf-4', name: '多云资源编排', category: 'provision', trigger: 'api', priority: 'P2',
    description: '业务提需求 → Terraform 生成 Plan → 成本评估 → 安全扫描 → 审批 → 自动创建 → CMDB 录入',
    status: 'completed', agents: ['planner', 'iac', 'cost', 'security', 'cloud', 'cmdb'],
    avgDuration: '45s', successRate: 98.1, totalRuns: 64, lastRun: '昨天 14:30',
    steps: [
      { name: '需求解析', agent: 'planner', tool: 'prometheus_range', status: 'completed', duration: '0.8s',
        input: '需求: 创建 2 台 4C8G ECS (华为云) + 1 台 RDS MySQL (阿里云)',
        output: '资源清单: 2×ecs.c6.xlarge (华为云), 1×rds.mysql.s3.large (阿里云)' },
      { name: 'Terraform Plan 生成', agent: 'iac', tool: 'terraform_plan', status: 'completed', duration: '8.5s',
        input: 'terraform plan -out=tfplan (3 个 resource, 1 个 provider alias)',
        output: 'Plan: 3 to add, 0 to change, 0 to destroy. 预估月费: ¥2,847' },
      { name: '成本评估', agent: 'cost', tool: 'kubecost_cost', status: 'completed', duration: '3.2s',
        input: '对比: 按需 vs 包年包月, 华为云 vs 阿里云价格',
        output: '推荐: 包年包月 (节省 38%), 华为云 ECS ¥1,200/月, 阿里云 RDS ¥850/月' },
      { name: '安全合规扫描', agent: 'security', tool: 'opa_policy_check', status: 'completed', duration: '2.1s',
        input: 'OPA 策略: 非生产环境必须加标签, 生产环境必须加密存储',
        output: '合规检查: PASS (所有资源已标记 environment=staging, encrypted=true)' },
      { name: '审批网关', agent: 'planner', tool: 'prometheus_range', status: 'completed', duration: '0.3s',
        input: '人工审批 (钉钉/飞书通知 → 审批通过)',
        output: '审批人: 张工, 审批时间: 14:32, 耗时: 2min' },
      { name: 'Terraform Apply', agent: 'iac', tool: 'terraform_apply', status: 'completed', duration: '65.3s',
        input: 'terraform apply tfplan',
        output: 'Apply complete! Resources: 3 added. 华为云: 2 ECS running, 阿里云: 1 RDS creating' },
      { name: 'CMDB 资产录入', agent: 'cmdb', tool: 'ansible_adhoc', status: 'completed', duration: '1.5s',
        input: 'CMDB API: POST /assets {type: ecs, count: 2, ...}',
        output: '资产编号: CMDB-2024-07-0456~0458, 已同步至 ITSM 工单系统' },
    ],
    triggeredAt: '14:30:00', completedAt: '14:30:45',
  },
  // 5. 安全漏洞应急响应
  {
    id: 'wf-5', name: '安全漏洞应急响应', category: 'security', trigger: 'alert', priority: 'P0',
    description: 'Trivy/Falco 检测到高危 CVE → 评估影响范围 → 隔离受影响服务 → 触发补丁构建 → 重新扫描验证',
    status: 'completed', agents: ['security', 'incident', 'devops', 'k8s', 'sre'],
    avgDuration: '18min', successRate: 91.3, totalRuns: 42, lastRun: '昨天 22:10',
    steps: [
      { name: '漏洞检测', agent: 'security', tool: 'trivy_image_scan', status: 'completed', duration: '3.2s',
        input: 'trivy image --severity CRITICAL registry.internal/payment:v1.8.2',
        output: 'CRITICAL: CVE-2024-3094 (xz backdoor), 影响: payment, order 两个服务' },
      { name: '影响范围评估', agent: 'incident', tool: 'prometheus_range', status: 'completed', duration: '1.8s',
        input: '查询所有使用 xz-utils 的容器 + 关联服务拓扑',
        output: '受影响: payment-svc (3 pods), order-svc (5 pods), 线上流量 12,000 QPS' },
      { name: '应急隔离', agent: 'k8s', tool: 'k8s_scale_deployment', status: 'completed', duration: '2.5s',
        input: 'NetworkPolicy: deny-all egress from payment-svc (仅保留健康检查)',
        output: 'NetworkPolicy applied, payment-svc 外部流量已隔离' },
      { name: '补丁镜像构建', agent: 'devops', tool: 'jenkins_build', status: 'completed', duration: '120.0s',
        input: 'Jenkins pipeline: payment-svc-patch, branch: hotfix/xz-cve',
        output: 'Build #892 SUCCESS, image: payment:v1.8.3-patch (xz 5.6.1-r2)' },
      { name: '安全重新扫描', agent: 'security', tool: 'trivy_image_scan', status: 'completed', duration: '2.8s',
        input: 'trivy image payment:v1.8.3-patch',
        output: 'CRITICAL: 0, HIGH: 0 → 通过门禁 ✅' },
      { name: '滚动更新部署', agent: 'k8s', tool: 'kubectl_patch_deployment', status: 'completed', duration: '45.0s',
        input: 'kubectl set image deploy payment=payment:v1.8.3-patch -n production',
        output: 'Rolling update: 3/3 pods updated, zero downtime' },
      { name: 'SLO 恢复确认', agent: 'sre', tool: 'prometheus_range', status: 'completed', duration: '5.0s',
        input: 'payment-svc: availability, latency-p99, error_rate (5min window)',
        output: 'Availability: 100%, P99: 45ms, Error: 0.00% ✅ 服务恢复正常' },
    ],
    triggeredAt: '22:10:00', completedAt: '22:28:00',
  },
  // 6. 中间件集群扩容
  {
    id: 'wf-6', name: 'RabbitMQ 集群扩容', category: 'optimize', trigger: 'alert', priority: 'P1',
    description: '队列积压告警 → 流量分析 → 容量规划 → 滚动扩容 → 集群健康检查 → 流量恢复验证',
    status: 'completed', agents: ['monitor', 'middleware', 'planner', 'iac', 'linux'],
    avgDuration: '25s', successRate: 95.8, totalRuns: 31, lastRun: '09:45',
    steps: [
      { name: '队列积压告警', agent: 'monitor', tool: 'prometheus_range', status: 'completed', duration: '0.5s',
        input: 'rabbitmq_queue_messages > 100000 持续 5min',
        output: 'order.delay 队列: 230,000 消息, 消费速率: 1,200/s, 预计积压: 3min' },
      { name: '流量模式分析', agent: 'middleware', tool: 'prometheus_range', status: 'completed', duration: '1.5s',
        input: 'rabbitmq_queue_messages{queue="order.delay"} [1h]',
        output: '峰值出现在 09:30-10:00, 与秒杀活动相关, 峰值 QPS: 8,500' },
      { name: '扩容方案规划', agent: 'planner', tool: 'prometheus_range', status: 'completed', duration: '2.0s',
        input: '当前: 3 节点 (4C8G), 目标: 5 节点, 消费者组: +10',
        output: '方案: 新增 2 节点 + 新增 10 个 consumer, 预计消积压时间: 2min' },
      { name: 'Terraform 扩容', agent: 'iac', tool: 'terraform_apply', status: 'completed', duration: '15.0s',
        input: 'terraform apply (rabbitmq_cluster: 3→5 nodes)',
        output: '2 新节点加入集群, Erlang cookie 同步完成, 镜像队列同步中...' },
      { name: '集群健康检查', agent: 'linux', tool: 'ssh_exec', status: 'completed', duration: '3.0s',
        input: 'rabbitmqctl cluster_status | grep running_nodes',
        output: 'Running nodes: 5/5, Memory: 42%, Disk: 38%, 镜像同步: OK' },
      { name: '消费能力验证', agent: 'middleware', tool: 'prometheus_range', status: 'completed', duration: '5.0s',
        input: 'rabbitmq_queue_messages{queue="order.delay"} [2min]',
        output: '队列积压: 230,000 → 0, 消费速率: 8,500/s ✅ 恢复正常' },
    ],
    triggeredAt: '09:45:00', completedAt: '09:45:25',
  },
  // 7. 合规审计扫描
  {
    id: 'wf-7', name: 'CIS 合规审计扫描', category: 'compliance', trigger: 'schedule', priority: 'P2',
    description: '每周定时触发 → kube-bench 安全扫描 → Falco 策略检查 → OPA 策略审计 → 生成合规报告',
    status: 'pending', agents: ['security', 'k8s', 'cmdb', 'planner'],
    avgDuration: '8min', successRate: 100, totalRuns: 52, lastRun: '上周日 03:00',
    steps: [
      { name: 'CIS kube-bench 扫描', agent: 'security', tool: 'trivy_image_scan', status: 'pending', duration: '-',
        input: 'kube-bench run --targets=master,node,policies (CIS Kubernetes Benchmark v1.8)',
        output: '-' },
      { name: 'Falco 运行时策略检查', agent: 'security', tool: 'falco_detect', status: 'pending', duration: '-',
        input: 'falco -L (列出所有触发的规则)',
        output: '-' },
      { name: 'OPA/Gatekeeper 策略审计', agent: 'security', tool: 'opa_policy_check', status: 'pending', duration: '-',
        input: 'opa audit (所有 ConstraintTemplate 违规)',
        output: '-' },
      { name: 'CMDB 资产交叉校验', agent: 'cmdb', tool: 'ansible_adhoc', status: 'pending', duration: '-',
        input: '对比: CMDB 记录 vs 实际运行资源',
        output: '-' },
      { name: '合规报告生成', agent: 'planner', tool: 'prometheus_range', status: 'pending', duration: '-',
        input: '汇总: CIS 评分 / Falco 违规数 / OPA 违规数 / 资产偏差',
        output: '-' },
    ],
    triggeredAt: '下周日 03:00', completedAt: null,
  },
  // 8. 日志异常智能检测
  {
    id: 'wf-8', name: '日志异常智能检测', category: 'incident', trigger: 'schedule', priority: 'P2',
    description: 'Loki 日志采集 → 模式提取 → 异常检测 → 指标关联 → 自动创建事件 → Copilot 摘要',
    status: 'completed', agents: ['log', 'monitor', 'apm', 'incident', 'copilot'],
    avgDuration: '15s', successRate: 89.7, totalRuns: 156, lastRun: '07:20',
    steps: [
      { name: 'Loki 日志批量采集', agent: 'log', tool: 'loki_query', status: 'completed', duration: '2.5s',
        input: 'logql: {namespace=~"prod.*"} | json | unwrap duration [5m]',
        output: '采集: 1,240,000 条日志, 12 个命名空间' },
      { name: '异常模式提取', agent: 'log', tool: 'loki_query', status: 'completed', duration: '3.8s',
        input: '统计: 错误频率突增 > 3σ, 新错误模式, 堆栈聚类',
        output: '异常: NullPointerException 频率突增 5x (order-svc), 新错误: RedisConnectionTimeout' },
      { name: 'Prometheus 指标关联', agent: 'monitor', tool: 'prometheus_range', status: 'completed', duration: '1.5s',
        input: '关联 order-svc 的 CPU/内存/错误率/延迟指标',
        output: '关联发现: 错误率与 Redis 连接数相关, Redis 连接池耗尽 (pool_size=50, active=50)' },
      { name: 'APM 调用链追踪', agent: 'apm', tool: 'skywalking_metrics', status: 'completed', duration: '2.2s',
        input: 'SkyWalking: order-svc → redis-cache 调用链, 最近 10min',
        output: 'Redis 调用 P99 延迟: 12ms → 2,300ms, 超时比例: 34%' },
      { name: '自动创建事件', agent: 'incident', tool: 'prometheus_range', status: 'completed', duration: '0.8s',
        input: 'Incident: "order-svc Redis 连接池耗尽", severity: P1, 指派人: SRE 团队',
        output: 'INC-2024-07-0089 已创建, 飞书通知已发送至 #sre-alert' },
      { name: 'Copilot 智能摘要', agent: 'copilot', tool: 'prometheus_range', status: 'completed', duration: '4.2s',
        input: '综合所有 Agent 数据, 生成根因分析摘要',
        output: '根因: Redis 连接池配置过小 (50), 高峰期 order-svc 并发请求超限, 建议扩容至 200' },
    ],
    triggeredAt: '07:20:00', completedAt: '07:20:15',
  },
  // 9. 服务网格流量切换
  {
    id: 'wf-9', name: 'Istio 金丝雀流量切换', category: 'deploy', trigger: 'manual', priority: 'P1',
    description: '手动触发 → 更新 VirtualService → 逐步切换流量 (10%→50%→100%) → 每阶段 APM 验证',
    status: 'pending', agents: ['gitops', 'servicemesh', 'apm', 'sre'],
    avgDuration: '20min', successRate: 98.5, totalRuns: 73, lastRun: '昨天 16:00',
    steps: [
      { name: '更新 VirtualService', agent: 'gitops', tool: 'argocd_sync', status: 'pending', duration: '-',
        input: 'kubectl apply -f vs-canary-10.yaml (weight: stable=90, canary=10)',
        output: '-' },
      { name: '10% 流量切换', agent: 'servicemesh', tool: 'prometheus_range', status: 'pending', duration: '-',
        input: 'Istio telemetry: istio_requests_total{destination_service="order-canary"}',
        output: '-' },
      { name: 'APM 黄金指标 (10%)', agent: 'apm', tool: 'skywalking_metrics', status: 'pending', duration: '-',
        input: 'latency-p50, latency-p99, error_rate, throughput (5min window)',
        output: '-' },
      { name: '50% 流量切换', agent: 'servicemesh', tool: 'prometheus_range', status: 'pending', duration: '-',
        input: 'weight: stable=50, canary=50',
        output: '-' },
      { name: 'APM 黄金指标 (50%)', agent: 'apm', tool: 'skywalking_metrics', status: 'pending', duration: '-',
        input: '同上, 5min window',
        output: '-' },
      { name: '100% 全量切换', agent: 'gitops', tool: 'argocd_sync', status: 'pending', duration: '-',
        input: 'weight: stable=0, canary=100 → 新版本成为 stable',
        output: '-' },
      { name: 'SLO 基线确认', agent: 'sre', tool: 'prometheus_range', status: 'pending', duration: '-',
        input: '全局 SLI vs SLO 阈值对比',
        output: '-' },
    ],
    triggeredAt: '待执行', completedAt: null,
  },
  // 10. 成本优化自动执行
  {
    id: 'wf-10', name: '月度成本优化执行', category: 'optimize', trigger: 'schedule', priority: 'P3',
    description: '每周定时扫描 → 识别闲置资源 → 生成优化建议 → 审批 → 自动执行 → 生成节省报告',
    status: 'completed', agents: ['cost', 'cloud', 'planner', 'iac', 'sre'],
    avgDuration: '30s', successRate: 92.0, totalRuns: 48, lastRun: '上周五 02:00',
    steps: [
      { name: '多云成本扫描', agent: 'cost', tool: 'kubecost_cost', status: 'completed', duration: '5.2s',
        input: 'Kubecost: 所有命名空间 + AWS Cost Explorer + Azure Cost Management',
        output: '总月费: ¥128,450, 环比 +8%, 最大增长: staging (+¥12,000)' },
      { name: '闲置资源识别', agent: 'cost', tool: 'kubecost_cost', status: 'completed', duration: '3.8s',
        input: 'CPU 利用率 < 5% 持续 7 天 + 无流量的 LoadBalancer',
        output: '闲置: 3 个 staging ECS (4C8G), 2 个空 ELB, 1 个未挂载 EBS (500G)' },
      { name: '优化建议生成', agent: 'planner', tool: 'prometheus_range', status: 'completed', duration: '2.1s',
        input: '综合: 闲置资源 + 降配建议 + RI/SP 推荐',
        output: '建议: 停止 3 staging ECS (省 ¥4,800/月), 降配 prod API (4C8G→2C4G, 省 ¥1,200/月)' },
      { name: 'SRE 影响评估', agent: 'sre', tool: 'prometheus_range', status: 'completed', duration: '1.5s',
        input: '检查被建议资源的 SLO 依赖关系',
        output: '3 个 staging ECS: 无生产依赖, 可安全停止 ✅' },
      { name: 'Terraform 执行', agent: 'iac', tool: 'terraform_apply', status: 'completed', duration: '18.0s',
        input: 'terraform apply (scale down staging, modify instance types)',
        output: 'Applied: 3 ECS stopped, 2 instance types modified, 1 EBS detached' },
      { name: '节省报告', agent: 'cost', tool: 'kubecost_cost', status: 'completed', duration: '2.5s',
        input: '执行前 vs 执行后成本对比',
        output: '预计月节省: ¥6,000 (4.7%), 年节省: ¥72,000, ROI: 已回本' },
    ],
    triggeredAt: '上周五 02:00', completedAt: '上周五 02:00:30',
  },
];

// 向后兼容: workflows alias
export const workflows = workflowTemplates.map(w => ({
  id: w.id, name: w.name, status: w.status,
  steps: w.steps.map(s => ({ name: s.name, agent: s.agent, status: s.status, duration: s.duration })),
  triggeredAt: w.triggeredAt, completedAt: w.completedAt,
}));

// System health (v4.3.0 - updated stats)
export const systemHealth = {
  cpu: 42,
  memory: 67,
  disk: 58,
  network: 23,
  uptime: '32d 14h 23m',
  totalAgents: 22,
  activeAgents: 9,
  totalTools: 115,
  totalTasks: 14237,
  successRate: 95.8,
  avgResponseTime: '2.4s',
  toolCategories: 15,
};
