
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
  { id: 'linux', name: 'Linux Agent', icon: '🐧', description: '系统诊断与性能分析', status: 'active', color: '#10b981', tasks: 1247, successRate: 96.5, avgResponseTime: '2.3s', category: 'infra' },
  { id: 'k8s', name: 'K8s Agent', icon: '☸️', description: 'Kubernetes 运维管理', status: 'active', color: '#3b82f6', tasks: 892, successRate: 94.2, avgResponseTime: '3.1s', category: 'infra' },
  { id: 'docker', name: 'Docker Agent', icon: '🐳', description: 'Docker 容器运维', status: 'active', color: '#0ea5e9', tasks: 1024, successRate: 96.8, avgResponseTime: '1.9s', category: 'infra' },
  { id: 'db', name: 'DB Agent', icon: '🗄️', description: '数据库诊断优化', status: 'active', color: '#8b5cf6', tasks: 634, successRate: 97.8, avgResponseTime: '1.8s', category: 'data' },
  { id: 'log', name: 'Log Agent', icon: '📋', description: '日志分析与告警', status: 'idle', color: '#f59e0b', tasks: 2156, successRate: 92.1, avgResponseTime: '1.2s', category: 'monitor' },
  { id: 'monitor', name: 'Monitor Agent', icon: '📊', description: '监控数据分析', status: 'active', color: '#06b6d4', tasks: 1580, successRate: 95.3, avgResponseTime: '0.8s', category: 'monitor' },
  { id: 'security', name: 'Security Agent', icon: '🔒', description: '安全扫描与防护', status: 'active', color: '#ef4444', tasks: 456, successRate: 99.1, avgResponseTime: '4.2s', category: 'security' },
  { id: 'sre', name: 'SRE Agent', icon: '🏥', description: 'SLI/SLO 管理', status: 'idle', color: '#ec4899', tasks: 328, successRate: 93.7, avgResponseTime: '2.0s', category: 'ops' },
  { id: 'cost', name: 'Cost Agent', icon: '💰', description: '成本分析优化', status: 'idle', color: '#14b8a6', tasks: 189, successRate: 91.4, avgResponseTime: '5.1s', category: 'ops' },
  { id: 'incident', name: 'Incident Agent', icon: '🚨', description: '事件管理响应', status: 'active', color: '#f97316', tasks: 567, successRate: 88.9, avgResponseTime: '3.5s', category: 'ops' },
  { id: 'devops', name: 'DevOps Agent', icon: '🚀', description: 'CI/CD 运维', status: 'idle', color: '#a855f7', tasks: 423, successRate: 95.6, avgResponseTime: '2.7s', category: 'dev' },
  { id: 'cmdb', name: 'CMDB Agent', icon: '📦', description: '配置管理', status: 'idle', color: '#64748b', tasks: 78, successRate: 98.2, avgResponseTime: '0.5s', category: 'data' },
  { id: 'cloud', name: 'Cloud Agent', icon: '☁️', description: '多云平台运维', status: 'active', color: '#f97316', tasks: 756, successRate: 94.5, avgResponseTime: '3.8s', category: 'cloud' },
  { id: 'windows', name: 'Windows Agent', icon: '🪟', description: 'Windows Server 运维', status: 'idle', color: '#06b6d4', tasks: 423, successRate: 95.2, avgResponseTime: '2.5s', category: 'infra' },
  { id: 'network', name: 'Network Agent', icon: '🌐', description: '网络设备运维', status: 'active', color: '#14b8a6', tasks: 612, successRate: 96.8, avgResponseTime: '1.8s', category: 'infra' },
  { id: 'middleware', name: 'Middleware Agent', icon: '📦', description: '中间件运维', status: 'active', color: '#a855f7', tasks: 834, successRate: 95.9, avgResponseTime: '2.1s', category: 'infra' },
  { id: 'servicemesh', name: 'ServiceMesh Agent', icon: '🔗', description: '服务网格管理', status: 'idle', color: '#6366f1', tasks: 156, successRate: 93.2, avgResponseTime: '2.8s', category: 'infra' },
  { id: 'virtual', name: 'Virtual Agent', icon: '🖥️', description: '虚拟化平台运维', status: 'idle', color: '#84cc16', tasks: 298, successRate: 97.5, avgResponseTime: '2.0s', category: 'infra' },
  { id: 'planner', name: 'Planner Agent', icon: '📋', description: '任务规划调度', status: 'active', color: '#eab308', tasks: 3456, successRate: 97.1, avgResponseTime: '1.5s', category: 'core' },
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
  { source: 'incident', target: 'devops', label: '修复' },
  { source: 'security', target: 'cmdb', label: '资产' },
  { source: 'cost', target: 'cmdb', label: '成本' },
];

// Recent events
export const events = [
  { time: '08:32', type: 'success', title: 'CPU 诊断完成', desc: 'Linux Agent 完成 prod-01 高CPU诊断，定位到 Java GC 问题', agent: 'linux' },
  { time: '08:30', type: 'warning', title: 'Pod 重启告警', desc: 'K8s Agent 检测到 namespace/production 中 3 个 Pod 异常重启', agent: 'k8s' },
  { time: '08:28', type: 'info', title: '慢查询分析', desc: 'DB Agent 分析 MySQL 慢查询日志，发现 5 条超过 3s 的查询', agent: 'db' },
  { time: '08:25', type: 'error', title: '安全扫描告警', desc: 'Security Agent 发现 2 个高危 CVE 漏洞', agent: 'security' },
  { time: '08:22', type: 'success', title: '工作流执行完成', desc: '自动修复工作流成功执行：扩容 + 重启 + 验证', agent: 'planner' },
  { time: '08:20', type: 'info', title: '成本报告生成', desc: 'Cost Agent 生成本月成本报告，节省 12.3%', agent: 'cost' },
  { time: '08:18', type: 'warning', title: '磁盘空间预警', desc: 'Monitor Agent 检测到 prod-03 磁盘使用率 87%', agent: 'monitor' },
  { time: '08:15', type: 'success', title: 'CI/CD 部署完成', desc: 'DevOps Agent 完成 v2.1.0 灰度发布，流量切换 10%', agent: 'devops' },
];

// Workflow data
export const workflows = [
  {
    id: 'wf-1',
    name: 'CPU 高负载自动修复',
    status: 'completed',
    steps: [
      { name: '监控告警', agent: 'monitor', status: 'completed', duration: '0.5s' },
      { name: '根因分析', agent: 'linux', status: 'completed', duration: '2.3s' },
      { name: '进程排查', agent: 'linux', status: 'completed', duration: '1.8s' },
      { name: '自动修复', agent: 'devops', status: 'completed', duration: '5.2s' },
      { name: '验证恢复', agent: 'monitor', status: 'completed', duration: '1.0s' },
    ],
    triggeredAt: '08:32:01',
    completedAt: '08:32:11',
  },
  {
    id: 'wf-2',
    name: 'Pod 异常重启处理',
    status: 'running',
    steps: [
      { name: '告警检测', agent: 'monitor', status: 'completed', duration: '0.3s' },
      { name: 'K8s 诊断', agent: 'k8s', status: 'completed', duration: '2.1s' },
      { name: '日志分析', agent: 'log', status: 'running', duration: '-' },
      { name: '自动重启', agent: 'k8s', status: 'pending', duration: '-' },
      { name: '健康检查', agent: 'sre', status: 'pending', duration: '-' },
    ],
    triggeredAt: '08:30:15',
    completedAt: null,
  },
  {
    id: 'wf-3',
    name: '慢查询优化',
    status: 'pending',
    steps: [
      { name: '查询分析', agent: 'db', status: 'pending', duration: '-' },
      { name: '索引建议', agent: 'db', status: 'pending', duration: '-' },
      { name: '审批确认', agent: 'planner', status: 'pending', duration: '-' },
      { name: '执行优化', agent: 'db', status: 'pending', duration: '-' },
    ],
    triggeredAt: '08:28:00',
    completedAt: null,
  },
];

// System health
export const systemHealth = {
  cpu: 42,
  memory: 67,
  disk: 58,
  network: 23,
  uptime: '32d 14h 23m',
  totalAgents: 12,
  activeAgents: 6,
  totalTasks: 8993,
  successRate: 95.8,
  avgResponseTime: '2.4s',
};
