/**
 * API Client - 自动检测 demo/real 模式
 *
 * 当通过 'aiops serve' 运行时，前后端同域，直接调用 API
 * 当在 GitHub Pages 运行时，无后端，使用内置 demo 数据
 */

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? `${window.location.protocol}//${window.location.host}`
  : ''; // GitHub Pages 无后端，走 fallback

let _isRealMode: boolean | null = null;

/** 检测是否有真实后端 */
export async function detectMode(): Promise<boolean> {
  if (_isRealMode !== null) return _isRealMode;
  try {
    const resp = await fetch(`${API_BASE}/api/v1/health`, { signal: AbortSignal.timeout(2000) });
    const data = await resp.json();
    _isRealMode = data.status === 'healthy';
  } catch {
    _isRealMode = false;
  }
  return _isRealMode;
}

export function isRealMode() {
  return _isRealMode ?? false;
}

/** 通用 API 请求 */
async function apiGet<T>(path: string, fallback: T): Promise<T> {
  if (!API_BASE) return fallback;
  try {
    const resp = await fetch(`${API_BASE}${path}`, { signal: AbortSignal.timeout(5000) });
    if (!resp.ok) return fallback;
    const data = await resp.json();
    return data.data ?? data;
  } catch {
    return fallback;
  }
}

// ===== 监控 API =====
export interface MonitoringSummary {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_in_mbps: number;
  network_out_mbps: number;
  uptime_seconds: number;
  total_alerts: number;
  firing_alerts: number;
  targets_up: number;
  targets_down: number;
}

export interface Alert {
  severity: string;
  name: string;
  instance: string;
  summary: string;
  desc: string;
  since: string;
  source: string;
}

export interface Target {
  url: string;
  job: string;
  health: string;
  lastScrape: string;
}

export interface MetricPoint {
  time: string;
  value: number;
}

const demoSummary: MonitoringSummary = {
  cpu_usage: 42, memory_usage: 67, disk_usage: 68,
  network_in_mbps: 15.2, network_out_mbps: 8.7,
  uptime_seconds: 2592000, total_alerts: 3, firing_alerts: 3,
  targets_up: 5, targets_down: 1,
};

const demoAlerts: Alert[] = [
  { severity: 'critical', name: 'DiskSpaceLow', instance: 'prod-03:9100', summary: '磁盘空间不足 10%', desc: '/data 分区使用率 93.2%', since: '47m', source: 'Prometheus' },
  { severity: 'warning', name: 'HighCPUUsage', instance: 'prod-02:9100', summary: 'CPU 使用率超过 80%', desc: '持续 15 分钟超过阈值', since: '19m', source: 'Prometheus' },
  { severity: 'warning', name: 'PodRestarting', instance: 'production/api-gateway', summary: 'Pod 频繁重启', desc: '1h 内重启 8 次', since: '2h', source: 'K8s Events' },
];

const demoTargets: Target[] = [
  { url: 'prod-01:9100', job: 'node-exporter', health: 'up', lastScrape: '12s ago' },
  { url: 'prod-02:9100', job: 'node-exporter', health: 'up', lastScrape: '8s ago' },
  { url: 'prod-03:9100', job: 'node-exporter', health: 'up', lastScrape: '15s ago' },
  { url: 'prod-01:8080', job: 'app-metrics', health: 'up', lastScrape: '5s ago' },
  { url: 'k8s-master:6443', job: 'kube-apiserver', health: 'up', lastScrape: '3s ago' },
  { url: 'prod-04:9090', job: 'custom-exporter', health: 'down', lastScrape: '5m ago' },
];

export async function fetchMonitoringSummary(): Promise<MonitoringSummary> {
  return apiGet('/api/v1/monitoring/summary', demoSummary);
}

export async function fetchAlerts(): Promise<Alert[]> {
  return apiGet('/api/v1/monitoring/alerts', demoAlerts);
}

export async function fetchTargets(): Promise<Target[]> {
  return apiGet('/api/v1/monitoring/targets', demoTargets);
}

export async function fetchMetrics(query: string): Promise<any> {
  return apiGet(`/api/v1/monitoring/metrics?query=${encodeURIComponent(query)}`, null);
}

// ===== 部署 API =====
export interface K8sNode {
  name: string;
  status: string;
  roles: string;
  age: string;
  version: string;
  cpu: number;
  memory: number;
}

export interface K8sPod {
  name: string;
  namespace: string;
  status: string;
  ready: string;
  restarts: number;
  age: string;
  node: string;
}

export interface K8sDeployment {
  name: string;
  namespace: string;
  ns?: string;
  ready: string;
  strategy: string;
  age: string;
  status: string;
  containers: string;
}

export interface K8sEvent {
  type: string;
  reason: string;
  object: string;
  message: string;
  age: string;
  namespace: string;
}

export interface DeploymentSummary {
  total_pods: number;
  running_pods: number;
  pending_pods: number;
  failed_pods: number;
  total_deployments: number;
  healthy_deployments: number;
  total_nodes: number;
  ready_nodes: number;
  total_namespaces: number;
}

const demoNodes: K8sNode[] = [
  { name: 'k8s-master', status: 'Ready', roles: 'control-plane', age: '127d', version: 'v1.28.4', cpu: 35, memory: 62 },
  { name: 'k8s-worker-01', status: 'Ready', roles: 'worker', age: '127d', version: 'v1.28.4', cpu: 68, memory: 74 },
  { name: 'k8s-worker-02', status: 'Ready', roles: 'worker', age: '95d', version: 'v1.28.4', cpu: 45, memory: 58 },
  { name: 'k8s-worker-03', status: 'Ready', roles: 'worker', age: '30d', version: 'v1.28.4', cpu: 52, memory: 65 },
];

const demoPods: K8sPod[] = [
  { name: 'api-gateway-7d8f9c6b4-x2k9m', namespace: 'production', status: 'Running', ready: '2/2', restarts: 0, age: '45d', node: 'k8s-worker-01' },
  { name: 'api-gateway-6f4c8b9a3-m3n5p', namespace: 'production', status: 'CrashLoopBackOff', ready: '0/2', restarts: 8, age: '2h', node: 'k8s-worker-03' },
  { name: 'user-service-5d7c8f9a6-a1b2c', namespace: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '30d', node: 'k8s-worker-01' },
  { name: 'payment-service-8c9d0e1f-a7b8c', namespace: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '60d', node: 'k8s-worker-01' },
  { name: 'mysql-backup-7k8l9m0n', namespace: 'data', status: 'Pending', ready: '0/0', restarts: 0, age: '5m', node: '' },
  { name: 'redis-cluster-0', namespace: 'data', status: 'Running', ready: '1/1', restarts: 0, age: '120d', node: 'k8s-worker-01' },
  { name: 'prometheus-0', namespace: 'monitoring', status: 'Running', ready: '1/1', restarts: 0, age: '90d', node: 'k8s-worker-03' },
  { name: 'grafana-7o8p9q0r', namespace: 'monitoring', status: 'Running', ready: '1/1', restarts: 0, age: '90d', node: 'k8s-worker-03' },
  { name: 'nginx-ingress-v3w4x', namespace: 'ingress-nginx', status: 'Running', ready: '1/1', restarts: 0, age: '127d', node: 'k8s-worker-01' },
];

const demoDeployments: K8sDeployment[] = [
  { name: 'api-gateway', namespace: 'production', ready: '2/3', strategy: 'RollingUpdate', age: '45d', status: 'progressing', containers: 'nginx:1.25, app:v2.1.0' },
  { name: 'user-service', namespace: 'production', ready: '3/3', strategy: 'RollingUpdate', age: '30d', status: 'healthy', containers: 'app:v1.8.2' },
  { name: 'payment-service', namespace: 'production', ready: '2/2', strategy: 'RollingUpdate', age: '60d', status: 'healthy', containers: 'app:v3.0.1' },
  { name: 'redis-cluster', namespace: 'data', ready: '3/3', strategy: 'RollingUpdate', age: '120d', status: 'healthy', containers: 'redis:7.2' },
  { name: 'prometheus', namespace: 'monitoring', ready: '1/1', strategy: 'Recreate', age: '90d', status: 'healthy', containers: 'prometheus:v2.48.0' },
  { name: 'grafana', namespace: 'monitoring', ready: '1/1', strategy: 'RollingUpdate', age: '90d', status: 'healthy', containers: 'grafana:10.2.0' },
  { name: 'nginx-ingress', namespace: 'ingress-nginx', ready: '2/2', strategy: 'RollingUpdate', age: '127d', status: 'healthy', containers: 'nginx:1.9.4' },
];

const demoEvents: K8sEvent[] = [
  { type: 'Warning', reason: 'BackOff', object: 'pod/api-gateway-6f4c8b9a3', message: 'Back-off restarting failed container', age: '2m', namespace: 'production' },
  { type: 'Warning', reason: 'OOMKilling', object: 'pod/api-gateway-6f4c8b9a3', message: 'Memory cgroup out of memory', age: '1h', namespace: 'production' },
  { type: 'Normal', reason: 'ScalingReplicaSet', object: 'deployment/api-gateway', message: 'Scaled up replica set to 3', age: '2h', namespace: 'production' },
  { type: 'Warning', reason: 'FailedScheduling', object: 'pod/mysql-backup', message: '0/3 nodes available: Insufficient cpu', age: '5m', namespace: 'data' },
];

const demoDeploySummary: DeploymentSummary = {
  total_pods: 20, running_pods: 18, pending_pods: 1, failed_pods: 1,
  total_deployments: 7, healthy_deployments: 6,
  total_nodes: 4, ready_nodes: 4, total_namespaces: 7,
};

export async function fetchDeploymentSummary(): Promise<DeploymentSummary> {
  return apiGet('/api/v1/deployment/summary', demoDeploySummary);
}

export async function fetchNodes(): Promise<K8sNode[]> {
  return apiGet('/api/v1/deployment/nodes', demoNodes);
}

export async function fetchPods(): Promise<K8sPod[]> {
  return apiGet('/api/v1/deployment/pods', demoPods);
}

export async function fetchDeployments(): Promise<K8sDeployment[]> {
  return apiGet('/api/v1/deployment/deployments', demoDeployments);
}

export async function fetchEvents(): Promise<K8sEvent[]> {
  return apiGet('/api/v1/deployment/events', demoEvents);
}
