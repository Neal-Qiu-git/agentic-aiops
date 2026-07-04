
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

// Workflow data
export const workflows = [
  {
    id: 'wf-1', name: 'K8s 异常自动修复', status: 'completed',
    steps: [
      { name: 'Prometheus 告警', agent: 'monitor', status: 'completed', duration: '0.5s' },
      { name: 'Loki 日志分析', agent: 'log', status: 'completed', duration: '1.8s' },
      { name: 'K8s 根因诊断', agent: 'k8s', status: 'completed', duration: '2.3s' },
      { name: '自动重启/扩容', agent: 'k8s', status: 'completed', duration: '3.2s' },
      { name: 'SLO 验证', agent: 'sre', status: 'completed', duration: '1.0s' },
    ],
    triggeredAt: '08:32:01', completedAt: '08:32:09',
  },
  {
    id: 'wf-2', name: 'GitOps 灰度发布', status: 'running',
    steps: [
      { name: 'ArgoCD 检测变更', agent: 'gitops', status: 'completed', duration: '0.3s' },
      { name: 'Trivy 镜像扫描', agent: 'security', status: 'completed', duration: '4.5s' },
      { name: '灰度部署 10%', agent: 'gitops', status: 'running', duration: '-' },
      { name: 'APM 监控验证', agent: 'apm', status: 'pending', duration: '-' },
      { name: '全量发布', agent: 'gitops', status: 'pending', duration: '-' },
    ],
    triggeredAt: '08:30:15', completedAt: null,
  },
  {
    id: 'wf-3', name: '数据库慢查询优化', status: 'pending',
    steps: [
      { name: 'Prometheus 指标', agent: 'monitor', status: 'pending', duration: '-' },
      { name: 'ClickHouse 分析', agent: 'db', status: 'pending', duration: '-' },
      { name: '索引建议', agent: 'db', status: 'pending', duration: '-' },
      { name: '审批确认', agent: 'planner', status: 'pending', duration: '-' },
    ],
    triggeredAt: '08:28:00', completedAt: null,
  },
];

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
