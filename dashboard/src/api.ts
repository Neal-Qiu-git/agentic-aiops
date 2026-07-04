/**
 * API 数据获取层 — 企业实际使用场景
 * 
 * 核心设计：
 * 1. 自动检测后端 API 是否可用（线上 vs Demo）
 * 2. 所有页面支持真实数据接入
 * 3. 数据源配置中心（用户可配置 Prometheus/Grafana/K8s 等）
 */

// ══════════════════════════════════════════
// 类型定义
// ══════════════════════════════════════════

export type DataMode = 'live' | 'demo';

export interface ApiState<T> {
  data: T;
  loading: boolean;
  mode: DataMode;
  lastUpdate: number;
  error: string | null;
}

// ── 数据源配置 ──
export interface DataSourceConfig {
  id: string;
  name: string;
  type: 'prometheus' | 'grafana' | 'kubernetes' | 'elasticsearch' | 'loki' | 'redis' | 'mysql' | 'custom';
  endpoint: string;
  auth_type: 'none' | 'token' | 'basic' | 'tls';
  enabled: boolean;
  last_check: string;
  status: 'connected' | 'disconnected' | 'error';
}

export const defaultDataSources: DataSourceConfig[] = [
  { id: 'prometheus', name: 'Prometheus', type: 'prometheus', endpoint: 'http://prometheus:9090', auth_type: 'none', enabled: true, last_check: '刚刚', status: 'connected' },
  { id: 'grafana', name: 'Grafana', type: 'grafana', endpoint: 'http://grafana:3000', auth_type: 'token', enabled: true, last_check: '刚刚', status: 'connected' },
  { id: 'k8s', name: 'Kubernetes', type: 'kubernetes', endpoint: 'https://kubernetes.default.svc', auth_type: 'tls', enabled: true, last_check: '刚刚', status: 'connected' },
  { id: 'loki', name: 'Loki', type: 'loki', endpoint: 'http://loki:3100', auth_type: 'none', enabled: false, last_check: '-', status: 'disconnected' },
  { id: 'mysql', name: 'MySQL', type: 'mysql', endpoint: 'mysql://db-master:3306', auth_type: 'basic', enabled: false, last_check: '-', status: 'disconnected' },
  { id: 'redis', name: 'Redis', type: 'redis', endpoint: 'redis://redis-cluster:6379', auth_type: 'none', enabled: false, last_check: '-', status: 'disconnected' },
];

// ══════════════════════════════════════════
// API 检测
// ══════════════════════════════════════════

const API_BASE = (() => {
  if (window.location.port === '8000' || window.location.hostname === 'localhost') {
    return '';
  }
  return '';
})();

let _apiReachable: boolean | null = null;
let _checkPromise: Promise<boolean> | null = null;

async function checkApiReachable(): Promise<boolean> {
  if (_apiReachable !== null) return _apiReachable;
  if (_checkPromise) return _checkPromise;
  
  _checkPromise = (async () => {
    try {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 2000);
      const resp = await fetch(`${API_BASE}/api/v1/health`, { signal: ctrl.signal });
      clearTimeout(timer);
      _apiReachable = resp.ok;
    } catch {
      _apiReachable = false;
    }
    return _apiReachable!;
  })();
  
  return _checkPromise;
}

export async function getMode(): Promise<DataMode> {
  const ok = await checkApiReachable();
  return ok ? 'live' : 'demo';
}

export async function fetchApi<T>(path: string, fallback: T): Promise<{ data: T; mode: DataMode }> {
  const ok = await checkApiReachable();
  if (!ok) return { data: fallback, mode: 'demo' };

  try {
    const resp = await fetch(`${API_BASE}${path}`);
    if (!resp.ok) return { data: fallback, mode: 'demo' };
    const json = await resp.json();
    if (json && typeof json === 'object' && 'data' in json && json.status) {
      return { data: json.data as T, mode: 'live' };
    }
    return { data: json as T, mode: 'live' };
  } catch {
    return { data: fallback, mode: 'demo' };
  }
}

// ══════════════════════════════════════════
// 平台概览数据
// ══════════════════════════════════════════

export interface PlatformOverview {
  // 系统状态
  system: {
    status: string;
    uptime: string;
    version: string;
    agents_active: number;
    agents_total: number;
    tools_total: number;
    tasks_today: number;
    tasks_total: number;
    success_rate: number;
  };
  // 资源概览
  resources: {
    servers: number;
    vms: number;
    containers: number;
    k8s_clusters: number;
    databases: number;
    network_devices: number;
  };
  // 今日事件
  events_today: {
    total: number;
    critical: number;
    warning: number;
    info: number;
    resolved: number;
  };
  // 成本概览
  cost: {
    monthly_total: number;
    trend: number; // 百分比变化
    budget_used: number; // 预算使用百分比
  };
}

export const demoPlatformOverview: PlatformOverview = {
  system: {
    status: 'healthy',
    uptime: '32d 14h 23m',
    version: 'v4.5.0',
    agents_active: 14,
    agents_total: 21,
    tools_total: 148,
    tasks_today: 127,
    tasks_total: 8934,
    success_rate: 96.8,
  },
  resources: {
    servers: 45,
    vms: 128,
    containers: 520,
    k8s_clusters: 6,
    databases: 32,
    network_devices: 67,
  },
  events_today: {
    total: 47,
    critical: 3,
    warning: 12,
    info: 32,
    resolved: 38,
  },
  cost: {
    monthly_total: 494000,
    trend: 3.2,
    budget_used: 82,
  },
};

// ══════════════════════════════════════════
// 告警数据
// ══════════════════════════════════════════

export interface Alert {
  name: string;
  severity: 'critical' | 'warning' | 'info';
  state: 'firing' | 'pending' | 'resolved';
  description: string;
  instance: string;
  started_at: string;
  labels?: Record<string, string>;
  runbook_url?: string;
  silenced?: boolean;
}

export interface AlertData {
  alerts: Alert[];
  summary: {
    total: number;
    firing: number;
    pending: number;
    resolved: number;
    by_severity: { critical: number; warning: number; info: number };
  };
}

export const demoAlerts: AlertData = {
  alerts: [
    { name: 'HighCPUUsage', severity: 'warning', state: 'firing', description: 'CPU使用率超过85%持续5分钟', instance: 'prod-web-01:9090', started_at: '2分钟前', labels: { job: 'node-exporter', env: 'production' }, runbook_url: '/runbooks/high-cpu' },
    { name: 'DiskSpaceLow', severity: 'critical', state: 'firing', description: '磁盘使用率超过90%', instance: 'db-master-01:9090', started_at: '15分钟前', labels: { job: 'node-exporter', mount: '/data' }, runbook_url: '/runbooks/disk-low' },
    { name: 'PodCrashLooping', severity: 'warning', state: 'firing', description: 'Pod crashloop超过5次', instance: 'k8s-worker-03', started_at: '28分钟前', labels: { namespace: 'staging', pod: 'user-service-xxx' }, runbook_url: '/runbooks/pod-crash' },
    { name: 'SSLExpiryWarning', severity: 'info', state: 'firing', description: 'SSL证书将在7天内过期', instance: 'lb-frontend', started_at: '3小时前', labels: { domain: 'api.example.com' }, runbook_url: '/runbooks/ssl-renew' },
    { name: 'MemoryHigh', severity: 'info', state: 'resolved', description: '内存使用率已恢复到正常水平', instance: 'app-server-02:9090', started_at: '1小时前' },
    { name: 'APIErrorRateHigh', severity: 'critical', state: 'firing', description: 'API 5xx错误率超过1%', instance: 'api-gateway:8080', started_at: '8分钟前', labels: { service: 'payment-service' }, runbook_url: '/runbooks/api-errors' },
  ],
  summary: {
    total: 6,
    firing: 4,
    pending: 0,
    resolved: 2,
    by_severity: { critical: 2, warning: 2, info: 2 },
  },
};

// ══════════════════════════════════════════
// 监控数据
// ══════════════════════════════════════════

export interface MonitoringSummary {
  cpu_usage?: number;
  memory_usage?: number;
  disk_usage?: number;
  network_in?: string;
  network_out?: string;
  uptime?: string;
  load_avg?: number[];
  status?: string;
  firing_alerts?: number;
  targets_up?: number;
  targets_down?: number;
}

export const demoMonitoringSummary: MonitoringSummary = {
  cpu_usage: 42, memory_usage: 67, disk_usage: 68,
  network_in: '125 MB/s', network_out: '89 MB/s',
  uptime: '32d 14h', load_avg: [1.2, 0.9, 0.8], status: 'healthy',
  firing_alerts: 4, targets_up: 5, targets_down: 1,
};

// ══════════════════════════════════════════
// 部署数据
// ══════════════════════════════════════════

export interface PodInfo {
  name: string; namespace: string; status: string;
  node: string; restarts: number; age: string; ready?: string;
  containers?: { name: string; ready: boolean; restarts: number }[];
}

export interface DeploymentInfo {
  name: string; namespace: string; replicas: string; ready?: string;
  status: string; updated: number; available: number;
  strategy?: string; containers?: string;
}

export interface NodeInfo {
  name: string; status: string; roles: string;
  age: string; version: string; cpu: string; memory: string;
}

export interface K8sEvents {
  type: string; reason: string; object: string;
  message: string; age: string; namespace: string;
}

export interface DeploymentSummary {
  total_pods: number; running_pods: number;
  pending_pods: number; failed_pods: number;
  total_deployments: number; healthy_deployments: number;
  total_nodes: number; ready_nodes: number;
  total_namespaces: number;
}

export const demoDeploymentSummary: DeploymentSummary = {
  total_pods: 47, running_pods: 42, pending_pods: 3, failed_pods: 2,
  total_deployments: 12, healthy_deployments: 10,
  total_nodes: 4, ready_nodes: 4, total_namespaces: 7,
};

export const demoPods: PodInfo[] = [
  { name: 'nginx-frontend-7b8d4f5c9-x2k4m', namespace: 'production', status: 'Running', node: 'worker-01', restarts: 0, age: '5d', ready: '1/1' },
  { name: 'api-gateway-5c6d7e8f9-abc12', namespace: 'production', status: 'Running', node: 'worker-02', restarts: 1, age: '3d', ready: '1/1' },
  { name: 'redis-cluster-0', namespace: 'data', status: 'Running', node: 'worker-01', restarts: 0, age: '12d', ready: '1/1' },
  { name: 'redis-cluster-1', namespace: 'data', status: 'Running', node: 'worker-02', restarts: 0, age: '12d', ready: '1/1' },
  { name: 'postgres-primary-0', namespace: 'data', status: 'Running', node: 'worker-03', restarts: 0, age: '20d', ready: '1/1' },
  { name: 'order-service-6f7g8h9i0-klm3n', namespace: 'production', status: 'Running', node: 'worker-01', restarts: 2, age: '1d', ready: '1/1' },
  { name: 'payment-service-a1b2c3d4-efg5h', namespace: 'production', status: 'Pending', node: '', restarts: 0, age: '5m', ready: '0/1' },
  { name: 'log-collector-j1k2l3m4-nop5q', namespace: 'monitoring', status: 'Running', node: 'worker-03', restarts: 0, age: '8d', ready: '1/1' },
  { name: 'alertmanager-r1s2t3u4-vwx5y', namespace: 'monitoring', status: 'Running', node: 'worker-04', restarts: 0, age: '15d', ready: '1/1' },
  { name: 'user-service-z1a2b3c4-d5e6f', namespace: 'staging', status: 'CrashLoopBackOff', node: 'worker-02', restarts: 8, age: '2h', ready: '0/2' },
  { name: 'search-engine-g7h8i9j0-k1l2m', namespace: 'production', status: 'Running', node: 'worker-04', restarts: 0, age: '7d', ready: '1/1' },
  { name: 'notification-svc-n3o4p5q6-r7s8', namespace: 'production', status: 'Running', node: 'worker-01', restarts: 0, age: '4d', ready: '1/1' },
];

export const demoDeployments: DeploymentInfo[] = [
  { name: 'nginx-frontend', namespace: 'production', replicas: '3/3', ready: '3/3', status: 'healthy', updated: 3, available: 3, strategy: 'RollingUpdate', containers: 'nginx:1.25' },
  { name: 'api-gateway', namespace: 'production', replicas: '2/2', ready: '2/2', status: 'healthy', updated: 2, available: 2, strategy: 'RollingUpdate', containers: 'node:20-alpine' },
  { name: 'order-service', namespace: 'production', replicas: '4/4', ready: '4/4', status: 'healthy', updated: 4, available: 4, strategy: 'RollingUpdate', containers: 'java:21-slim' },
  { name: 'payment-service', namespace: 'production', replicas: '1/2', ready: '1/2', status: 'degraded', updated: 1, available: 1, strategy: 'RollingUpdate', containers: 'java:21-slim' },
  { name: 'search-engine', namespace: 'production', replicas: '3/3', ready: '3/3', status: 'healthy', updated: 3, available: 3, strategy: 'RollingUpdate', containers: 'elasticsearch:8.11' },
  { name: 'redis-cluster', namespace: 'data', replicas: '3/3', ready: '3/3', status: 'healthy', updated: 3, available: 3, strategy: 'RollingUpdate', containers: 'redis:7.2' },
  { name: 'postgres-primary', namespace: 'data', replicas: '1/1', ready: '1/1', status: 'healthy', updated: 1, available: 1, strategy: 'Recreate', containers: 'postgres:16' },
  { name: 'log-collector', namespace: 'monitoring', replicas: '2/2', ready: '2/2', status: 'healthy', updated: 2, available: 2, strategy: 'RollingUpdate', containers: 'fluentd:1.16' },
  { name: 'alertmanager', namespace: 'monitoring', replicas: '1/1', ready: '1/1', status: 'healthy', updated: 1, available: 1, strategy: 'RollingUpdate', containers: 'alertmanager:0.26' },
  { name: 'user-service', namespace: 'staging', replicas: '0/2', ready: '0/2', status: 'critical', updated: 0, available: 0, strategy: 'RollingUpdate', containers: 'python:3.12' },
  { name: 'notification-svc', namespace: 'production', replicas: '2/2', ready: '2/2', status: 'healthy', updated: 2, available: 2, strategy: 'RollingUpdate', containers: 'go:1.21-alpine' },
  { name: 'config-server', namespace: 'production', replicas: '1/1', ready: '1/1', status: 'healthy', updated: 1, available: 1, strategy: 'RollingUpdate', containers: 'java:21-slim' },
];

export const demoNodes: NodeInfo[] = [
  { name: 'master-01', status: 'Ready', roles: 'control-plane', age: '45d', version: 'v1.28.4', cpu: '8/8', memory: '31Gi/32Gi' },
  { name: 'worker-01', status: 'Ready', roles: 'worker', age: '45d', version: 'v1.28.4', cpu: '6/8', memory: '24Gi/32Gi' },
  { name: 'worker-02', status: 'Ready', roles: 'worker', age: '45d', version: 'v1.28.4', cpu: '7/8', memory: '28Gi/32Gi' },
  { name: 'worker-03', status: 'Ready', roles: 'worker', age: '30d', version: 'v1.28.4', cpu: '4/8', memory: '20Gi/32Gi' },
  { name: 'worker-04', status: 'Ready', roles: 'worker', age: '15d', version: 'v1.28.4', cpu: '5/8', memory: '22Gi/32Gi' },
];

export const demoK8sEvents: K8sEvents[] = [
  { type: 'Warning', reason: 'FailedScheduling', object: 'payment-service-7d8e9f0g1-h2i3j', message: 'Insufficient cpu on worker-03', age: '5m', namespace: 'production' },
  { type: 'Warning', reason: 'BackOff', object: 'user-service-z1a2b3c4-d5e6f', message: 'Back-off restarting failed container', age: '2h', namespace: 'staging' },
  { type: 'Normal', reason: 'ScalingReplicaSet', object: 'order-service-6f7g8h9i0', message: 'Scaled up replica set to 4', age: '1d', namespace: 'production' },
  { type: 'Normal', reason: 'Pulling', object: 'nginx-frontend-7b8d4f5c9', message: 'Pulling image "nginx:1.25"', age: '5d', namespace: 'production' },
  { type: 'Normal', reason: 'Scheduled', object: 'log-collector-j1k2l3m4-nop5q', message: 'Successfully assigned to worker-03', age: '8d', namespace: 'monitoring' },
];

// ══════════════════════════════════════════
// SLO 数据
// ══════════════════════════════════════════

export interface SLOData {
  name: string; target: number; current: number;
  status: string; error_budget_remaining: number;
  description: string; slo_type: string;
}

export const demoSLOs: SLOData[] = [
  { name: 'API 可用性', target: 99.9, current: 99.95, status: 'healthy', error_budget_remaining: 95, description: 'HTTP 2xx / 总请求数', slo_type: 'availability' },
  { name: 'API 延迟 P99', target: 200, current: 156, status: 'healthy', error_budget_remaining: 78, description: 'P99 响应时间 < 200ms', slo_type: 'latency' },
  { name: '错误率', target: 0.1, current: 0.05, status: 'healthy', error_budget_remaining: 90, description: '5xx / 总请求数 < 0.1%', slo_type: 'error_rate' },
  { name: '数据新鲜度', target: 60, current: 45, status: 'healthy', error_budget_remaining: 85, description: '指标采集延迟 < 60s', slo_type: 'freshness' },
  { name: '批处理完成率', target: 99, current: 97.5, status: 'degraded', error_budget_remaining: 30, description: '定时任务成功完成率', slo_type: 'availability' },
];

// ══════════════════════════════════════════
// 成本数据
// ══════════════════════════════════════════

export interface CostData {
  provider: string; service: string; monthly: number;
  trend: string; optimization: string; region: string;
}

export const demoCostData: CostData[] = [
  { provider: '阿里云', service: 'ECS 计算', monthly: 125000, trend: '+5%', optimization: '可优化: 3台低利用率实例', region: 'cn-hangzhou' },
  { provider: '阿里云', service: 'RDS 数据库', monthly: 89000, trend: '+2%', optimization: '存储可清理 200GB 历史数据', region: 'cn-hangzhou' },
  { provider: '阿里云', service: 'SLB 负载均衡', monthly: 32000, trend: '0%', optimization: '无优化建议', region: 'cn-hangzhou' },
  { provider: 'AWS', service: 'EC2 计算', monthly: 98000, trend: '-3%', optimization: '预留实例可节省 35%', region: 'us-east-1' },
  { provider: 'AWS', service: 'S3 存储', monthly: 15000, trend: '+12%', optimization: '生命周期策略迁移冷数据', region: 'us-east-1' },
  { provider: 'AWS', service: 'CloudFront', monthly: 22000, trend: '+8%', optimization: '缓存命中率可提升', region: 'global' },
  { provider: '华为云', service: 'ECS', monthly: 68000, trend: '+1%', optimization: '弹性伸缩可减少闲时资源', region: 'cn-north-4' },
  { provider: '腾讯云', service: 'CVM', monthly: 45000, trend: '-2%', optimization: '无优化建议', region: 'ap-guangzhou' },
];

// ══════════════════════════════════════════
// 安全数据
// ══════════════════════════════════════════

export interface SecurityData {
  category: string; total: number; critical: number;
  high: number; medium: number; low: number;
  items: { name: string; severity: string; status: string; description: string }[];
}

export const demoSecurityData: SecurityData[] = [
  { category: '漏洞扫描', total: 23, critical: 2, high: 5, medium: 11, low: 5, items: [
    { name: 'CVE-2024-3094', severity: 'critical', status: 'open', description: 'XZ Utils 后门漏洞' },
    { name: 'CVE-2024-21762', severity: 'critical', status: 'open', description: 'FortiOS 远程代码执行' },
    { name: 'OpenSSH 弱密码', severity: 'high', status: 'mitigated', description: '部分主机仍允许密码登录' },
  ]},
  { category: '合规检查', total: 45, critical: 0, high: 3, medium: 12, low: 30, items: [
    { name: '密码策略', severity: 'high', status: 'open', description: '3台服务器密码不符合等保要求' },
    { name: '审计日志', severity: 'high', status: 'open', description: '审计日志保留不足180天' },
    { name: '文件权限', severity: 'medium', status: 'open', description: '敏感文件权限过宽' },
  ]},
  { category: '配置审计', total: 67, critical: 0, high: 2, medium: 8, low: 57, items: [
    { name: 'SSH 配置', severity: 'high', status: 'open', description: '2台服务器允许 root SSH 登录' },
    { name: '防火墙规则', severity: 'medium', status: 'open', description: '5条冗余规则' },
  ]},
];

// ══════════════════════════════════════════
// 多云数据
// ══════════════════════════════════════════

export interface MulticloudData {
  provider: string; status: string; instances: number;
  regions: string[]; monthly_cost: number; services: string[];
}

export const demoMulticloud: MulticloudData[] = [
  { provider: '阿里云', status: 'healthy', instances: 35, regions: ['cn-hangzhou', 'cn-shanghai'], monthly_cost: 246000, services: ['ECS', 'RDS', 'Redis', 'SLB', 'OSS', 'CDN'] },
  { provider: 'AWS', status: 'healthy', instances: 18, regions: ['us-east-1', 'ap-southeast-1'], monthly_cost: 135000, services: ['EC2', 'RDS', 'S3', 'CloudFront', 'Lambda'] },
  { provider: '华为云', status: 'healthy', instances: 12, regions: ['cn-north-4'], monthly_cost: 68000, services: ['ECS', 'RDS', 'OBS', 'CCE'] },
  { provider: '腾讯云', status: 'degraded', instances: 8, regions: ['ap-guangzhou'], monthly_cost: 45000, services: ['CVM', 'COS', 'CLB'] },
];

// ══════════════════════════════════════════
// 事件日志
// ══════════════════════════════════════════

export interface EventLog {
  time: string; level: string; source: string;
  title: string; description: string;
}

export const demoEvents: EventLog[] = [
  { time: '14:32:15', level: 'error', source: 'k8s', title: 'Pod CrashLoopBackOff', description: 'user-service 容器反复崩溃，已重启8次' },
  { time: '14:28:03', level: 'warning', source: 'monitoring', title: 'CPU 告警触发', description: 'prod-web-01 CPU使用率达到 87%' },
  { time: '14:15:42', level: 'info', source: 'deploy', title: '滚动更新完成', description: 'nginx-frontend 3/3 副本更新成功' },
  { time: '14:02:18', level: 'warning', source: 'db', title: '慢查询告警', description: 'postgres-primary 检测到3条慢查询(>2s)' },
  { time: '13:45:00', level: 'info', source: 'sre', title: 'SLO 检查通过', description: 'API可用性 99.95%，目标 99.9%' },
  { time: '13:30:22', level: 'info', source: 'deploy', title: '新版本部署', description: 'api-gateway v2.3.1 部署到 staging' },
  { time: '13:15:11', level: 'error', source: 'security', title: '异常登录检测', description: '检测到非常规IP 203.0.113.42 尝试SSH登录' },
  { time: '13:00:00', level: 'info', source: 'cost', title: '成本报告生成', description: '本月云资源总费用 ¥494,000，较上月 +3.2%' },
  { time: '12:45:33', level: 'warning', source: 'network', title: '延迟升高', description: '阿里云→AWS链路延迟升至 195ms' },
  { time: '12:30:00', level: 'info', source: 'backup', title: '备份完成', description: 'postgres-primary 每日全量备份成功' },
];

// ══════════════════════════════════════════
// Agent/Tool 数据
// ══════════════════════════════════════════

export interface AgentData {
  name: string; icon: string; status: string;
  tasks: number; tools: string[]; description: string;
  category: string;
}

export const demoAgentData: AgentData[] = [
  { name: 'linux', icon: '🐧', status: 'active', tasks: 1247, tools: ['ssh', 'systemctl', 'journalctl'], description: 'Linux 系统运维', category: '基础' },
  { name: 'docker', icon: '🐳', status: 'active', tasks: 892, tools: ['docker', 'docker-compose', 'containerd'], description: '容器运行时管理', category: '容器' },
  { name: 'k8s', icon: '☸️', status: 'active', tasks: 2103, tools: ['kubectl', 'helm', 'kustomize'], description: 'Kubernetes 编排', category: '容器' },
  { name: 'db', icon: '🗄️', status: 'active', tasks: 634, tools: ['mysql', 'redis-cli', 'psql'], description: '数据库运维', category: '数据' },
  { name: 'monitor', icon: '📊', status: 'active', tasks: 3456, tools: ['prometheus', 'grafana', 'alertmanager'], description: '监控与告警', category: '监控' },
  { name: 'security', icon: '🔒', status: 'active', tasks: 289, tools: ['trivy', 'vault', 'cert-manager'], description: '安全扫描与合规', category: '安全' },
  { name: 'log', icon: '📝', status: 'active', tasks: 1567, tools: ['loki', 'elasticsearch', 'fluentd'], description: '日志分析', category: '监控' },
  { name: 'incident', icon: '🚨', status: 'idle', tasks: 45, tools: ['pagerduty', 'slack', 'jira'], description: '故障应急响应', category: '运维' },
  { name: 'sre', icon: '🏥', status: 'active', tasks: 178, tools: ['slo-toolkit', 'error-budget'], description: 'SLO/SLI 管理', category: '运维' },
  { name: 'cost', icon: '💰', status: 'active', tasks: 92, tools: ['kubecost', 'infracost', 'finops'], description: '成本优化', category: 'FinOps' },
  { name: 'devops', icon: '🚀', status: 'active', tasks: 567, tools: ['jenkins', 'gitlab', 'argocd'], description: 'CI/CD 流水线', category: 'DevOps' },
  { name: 'cloud', icon: '☁️', status: 'active', tasks: 445, tools: ['aws-cli', 'aliyun-cli', 'hcloud'], description: '多云管理', category: '云' },
  { name: 'network', icon: '🌐', status: 'active', tasks: 234, tools: ['ping', 'traceroute', 'ss'], description: '网络诊断', category: '网络' },
  { name: 'middleware', icon: '📦', status: 'active', tasks: 378, tools: ['nginx', 'rabbitmq', 'kafka'], description: '中间件管理', category: '中间件' },
  { name: 'cmdb', icon: '📋', status: 'idle', tasks: 56, tools: ['ansible', 'terraform'], description: '配置管理', category: 'CMDB' },
  { name: 'planner', icon: '🧠', status: 'active', tasks: 890, tools: ['task-planner', 'workflow-engine'], description: '任务编排调度', category: '核心' },
  { name: 'copilot', icon: '🤖', status: 'active', tasks: 2340, tools: ['llm-api', 'rag-engine'], description: 'AI 对话助手', category: '核心' },
];

// ══════════════════════════════════════════
// 工作流数据
// ══════════════════════════════════════════

export interface WorkflowData {
  name: string; status: string; triggers: string;
  steps: number; last_run: string; success_rate: number;
  description: string;
}

export const demoWorkflows: WorkflowData[] = [
  { name: 'P0 故障自动响应', status: 'active', triggers: '告警触发', steps: 8, last_run: '2小时前', success_rate: 98, description: '检测→定位→隔离→通知→修复→验证→复盘' },
  { name: '每日巡检', status: 'active', triggers: '定时 09:00', steps: 12, last_run: '今天 09:00', success_rate: 100, description: '健康检查→安全扫描→性能基线→报告生成' },
  { name: '自动扩缩容', status: 'active', triggers: 'CPU>80%', steps: 5, last_run: '30分钟前', success_rate: 95, description: '触发→评估→扩容→验证→通知' },
  { name: '数据库备份验证', status: 'active', triggers: '定时 02:00', steps: 6, last_run: '今天 02:00', success_rate: 100, description: '备份→校验→恢复测试→清理→报告' },
  { name: 'SSL证书续签', status: 'active', triggers: '到期前30天', steps: 4, last_run: '3天前', success_rate: 100, description: '检测→申请→部署→验证' },
];

// ══════════════════════════════════════════
// 环境发现数据
// ══════════════════════════════════════════

export interface DiscoveryData {
  os: { os_type: string; os_name: string; os_version: string; kernel: string; arch: string; hostname: string };
  hardware: { cpu_cores: number; memory_gb: number; disk_gb: number; load_1m: number; is_virtual: boolean; virtual_type: string; arch: string };
  cloud: { is_cloud: boolean; provider: string; region: string; instance_type: string; instance_id: string };
  containers: { docker: boolean; docker_version: string; docker_running: boolean; containerd: boolean; podman: boolean; k3s: boolean };
  kubernetes: { available: boolean; version: string; nodes: number; namespaces: number; pods: number; provider: string };
  middleware: { name: string; version: string; running: boolean }[];
  databases: { name: string; version: string; port: number; running: boolean }[];
  network: { private_ip: string; public_ip: string; dns: string[]; interfaces: { name: string; ip: string }[] };
  services: { systemd_count: number; docker_containers: number; listening_ports: number[] };
  deployment: { docker_compose: boolean; k8s_deployment: boolean; ansible: boolean; terraform: boolean; helm: boolean; gitops: boolean };
  recommended_agents: { name: string; icon: string; reason: string; priority: string; category: string }[];
  inferred_topology: { type: string; label: string; confidence: number };
}

// ══════════════════════════════════════════
// 旧版兼容导出（data/agents.ts 仍在使用）
// ══════════════════════════════════════════

export const systemHealth = {
  status: 'healthy',
  uptime: '32d 14h 23m',
  activeAgents: 14,
  totalAgents: 21,
  totalTools: 148,
  totalTasks: 8934,
  successRate: 96.8,
  cpu: 42,
  memory: 67,
  disk: 68,
  network: 35,
};

export const events = demoEvents;

// ══════════════════════════════════════════
// 兼容旧页面的导出（DeploymentPage/MonitoringPage）
// ══════════════════════════════════════════

export { getMode as detectMode };

// ── 监控类型 ──
export interface Target { job: string; instance: string; status: string; last_scrape: string; }

export async function fetchMonitoringSummary(): Promise<{ data: MonitoringSummary; mode: DataMode }> {
  return fetchApi<MonitoringSummary>('/api/v1/monitoring/summary', demoMonitoringSummary);
}
export async function fetchAlerts(): Promise<{ data: AlertData; mode: DataMode }> {
  return fetchApi<AlertData>('/api/v1/monitoring/alerts', demoAlerts);
}
export async function fetchTargets(): Promise<{ data: { targets: Target[] }; mode: DataMode }> {
  return fetchApi('/api/v1/monitoring/targets', { targets: [
    { job: 'node-exporter', instance: 'master-01:9100', status: 'up', last_scrape: '15s ago' },
    { job: 'node-exporter', instance: 'worker-01:9100', status: 'up', last_scrape: '12s ago' },
    { job: 'node-exporter', instance: 'worker-02:9100', status: 'up', last_scrape: '8s ago' },
    { job: 'kube-state-metrics', instance: 'master-01:8080', status: 'up', last_scrape: '20s ago' },
    { job: 'prometheus', instance: 'master-01:9090', status: 'up', last_scrape: '5s ago' },
    { job: 'alertmanager', instance: 'master-01:9093', status: 'up', last_scrape: '18s ago' },
  ] });
}

// ── 部署类型 ──
export interface K8sNode { name: string; status: string; roles: string; age: string; version: string; cpu: string; memory: string; }
export interface K8sPod { name: string; namespace: string; status: string; node: string; restarts: number; age: string; ready?: string; }
export interface K8sDeployment { name: string; namespace: string; ns?: string; replicas: string; ready?: string; status: string; updated: number; available: number; strategy?: string; containers?: string; }
export interface K8sEvent { type: string; reason: string; object: string; message: string; age: string; namespace: string; }

export async function fetchDeploymentSummary(): Promise<{ data: DeploymentSummary; mode: DataMode }> {
  return fetchApi<DeploymentSummary>('/api/v1/deployment/summary', demoDeploymentSummary);
}
export async function fetchNodes(): Promise<{ data: K8sNode[]; mode: DataMode }> {
  return fetchApi<K8sNode[]>('/api/v1/deployment/nodes', demoNodes);
}
export async function fetchPods(): Promise<{ data: K8sPod[]; mode: DataMode }> {
  return fetchApi<K8sPod[]>('/api/v1/deployment/pods', demoPods);
}
export async function fetchDeployments(): Promise<{ data: K8sDeployment[]; mode: DataMode }> {
  return fetchApi<K8sDeployment[]>('/api/v1/deployment/deployments', demoDeployments);
}
export async function fetchEvents(): Promise<{ data: K8sEvent[]; mode: DataMode }> {
  return fetchApi<K8sEvent[]>('/api/v1/deployment/events', demoK8sEvents);
}

// ══════════════════════════════════════════
// SLO / 事件日志 / 工作流 / 智能体 API
// ══════════════════════════════════════════

export async function fetchSLOs(): Promise<{ data: SLOData[]; mode: DataMode }> {
  return fetchApi<SLOData[]>('/api/v1/slo', demoSLOs);
}
export async function fetchEventLogs(): Promise<{ data: EventLog[]; mode: DataMode }> {
  return fetchApi<EventLog[]>('/api/v1/events', demoEvents);
}
export async function fetchWorkflows(): Promise<{ data: WorkflowData[]; mode: DataMode }> {
  return fetchApi<WorkflowData[]>('/api/v1/workflows', demoWorkflows);
}
export async function fetchAgentData(): Promise<{ data: AgentData[]; mode: DataMode }> {
  return fetchApi<AgentData[]>('/api/v1/agents', demoAgentData);
}

// ══════════════════════════════════════════
// Agent 网络拓扑连接
// ══════════════════════════════════════════

export interface AgentConnection {
  source: string; target: string; label: string;
}

export const demoConnections: AgentConnection[] = [
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
];

export async function fetchConnections(): Promise<{ data: AgentConnection[]; mode: DataMode }> {
  return fetchApi<AgentConnection[]>('/api/v1/network/connections', demoConnections);
}
