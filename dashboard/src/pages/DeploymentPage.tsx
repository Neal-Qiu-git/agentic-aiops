import { useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

// ===== 模拟数据 =====
const nodes = [
  { name: 'k8s-master', status: 'Ready', roles: 'control-plane', age: '127d', version: 'v1.28.4', cpu: 35, memory: 62, cpuTotal: '8', memTotal: '32Gi' },
  { name: 'k8s-worker-01', status: 'Ready', roles: 'worker', age: '127d', version: 'v1.28.4', cpu: 68, memory: 74, cpuTotal: '16', memTotal: '64Gi' },
  { name: 'k8s-worker-02', status: 'Ready', roles: 'worker', age: '95d', version: 'v1.28.4', cpu: 45, memory: 58, cpuTotal: '16', memTotal: '64Gi' },
  { name: 'k8s-worker-03', status: 'Ready', roles: 'worker', age: '30d', version: 'v1.28.4', cpu: 52, memory: 65, cpuTotal: '16', memTotal: '64Gi' },
];

const deployments = [
  { name: 'api-gateway', ns: 'production', ready: '2/3', strategy: 'RollingUpdate', age: '45d', status: 'progressing', containers: 'nginx:1.25, app:v2.1.0' },
  { name: 'user-service', ns: 'production', ready: '3/3', strategy: 'RollingUpdate', age: '30d', status: 'healthy', containers: 'app:v1.8.2' },
  { name: 'payment-service', ns: 'production', ready: '2/2', strategy: 'RollingUpdate', age: '60d', status: 'healthy', containers: 'app:v3.0.1' },
  { name: 'order-service', ns: 'production', ready: '2/2', strategy: 'RollingUpdate', age: '20d', status: 'healthy', containers: 'app:v2.4.0' },
  { name: 'notification-service', ns: 'production', ready: '1/1', strategy: 'RollingUpdate', age: '15d', status: 'healthy', containers: 'app:v1.2.0' },
  { name: 'redis-cluster', ns: 'data', ready: '3/3', strategy: 'RollingUpdate', age: '120d', status: 'healthy', containers: 'redis:7.2' },
  { name: 'mysql-primary', ns: 'data', ready: '1/1', strategy: 'Recreate', age: '127d', status: 'healthy', containers: 'mysql:8.0' },
  { name: 'prometheus', ns: 'monitoring', ready: '1/1', strategy: 'Recreate', age: '90d', status: 'healthy', containers: 'prometheus:v2.48.0' },
  { name: 'grafana', ns: 'monitoring', ready: '1/1', strategy: 'RollingUpdate', age: '90d', status: 'healthy', containers: 'grafana:10.2.0' },
  { name: 'nginx-ingress', ns: 'ingress-nginx', ready: '2/2', strategy: 'RollingUpdate', age: '127d', status: 'healthy', containers: 'nginx:1.9.4' },
];

const pods = [
  { name: 'api-gateway-7d8f9c6b4-x2k9m', ns: 'production', status: 'Running', ready: '2/2', restarts: 0, age: '45d', node: 'k8s-worker-01' },
  { name: 'api-gateway-7d8f9c6b4-h9j2k', ns: 'production', status: 'Running', ready: '2/2', restarts: 0, age: '45d', node: 'k8s-worker-02' },
  { name: 'api-gateway-6f4c8b9a3-m3n5p', ns: 'production', status: 'CrashLoopBackOff', ready: '0/2', restarts: 8, age: '2h', node: 'k8s-worker-03' },
  { name: 'user-service-5d7c8f9a6-a1b2c', ns: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '30d', node: 'k8s-worker-01' },
  { name: 'user-service-5d7c8f9a6-d3e4f', ns: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '30d', node: 'k8s-worker-02' },
  { name: 'user-service-5d7c8f9a6-g5h6i', ns: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '30d', node: 'k8s-worker-03' },
  { name: 'payment-service-8c9d0e1f-a7b8c', ns: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '60d', node: 'k8s-worker-01' },
  { name: 'payment-service-8c9d0e1f-d9e0f', ns: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '60d', node: 'k8s-worker-02' },
  { name: 'order-service-2a3b4c5d-e1f2g', ns: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '20d', node: 'k8s-worker-01' },
  { name: 'order-service-2a3b4c5d-h3i4j', ns: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '20d', node: 'k8s-worker-03' },
  { name: 'notification-6g7h8i9j', ns: 'production', status: 'Running', ready: '1/1', restarts: 0, age: '15d', node: 'k8s-worker-02' },
  { name: 'redis-cluster-0', ns: 'data', status: 'Running', ready: '1/1', restarts: 0, age: '120d', node: 'k8s-worker-01' },
  { name: 'redis-cluster-1', ns: 'data', status: 'Running', ready: '1/1', restarts: 0, age: '120d', node: 'k8s-worker-02' },
  { name: 'redis-cluster-2', ns: 'data', status: 'Running', ready: '1/1', restarts: 0, age: '120d', node: 'k8s-worker-03' },
  { name: 'mysql-primary-0', ns: 'data', status: 'Running', ready: '1/1', restarts: 0, age: '127d', node: 'k8s-worker-01' },
  { name: 'mysql-backup-7k8l9m0n', ns: 'data', status: 'Pending', ready: '0/0', restarts: 0, age: '5m', node: '' },
  { name: 'prometheus-0', ns: 'monitoring', status: 'Running', ready: '1/1', restarts: 0, age: '90d', node: 'k8s-worker-03' },
  { name: 'grafana-7o8p9q0r', ns: 'monitoring', status: 'Running', ready: '1/1', restarts: 0, age: '90d', node: 'k8s-worker-03' },
  { name: 'nginx-ingress-v3w4x', ns: 'ingress-nginx', status: 'Running', ready: '1/1', restarts: 0, age: '127d', node: 'k8s-worker-01' },
  { name: 'nginx-ingress-y5z6a', ns: 'ingress-nginx', status: 'Running', ready: '1/1', restarts: 0, age: '127d', node: 'k8s-worker-02' },
];

const events = [
  { type: 'Warning', reason: 'BackOff', object: 'pod/api-gateway-6f4c8b9a3', message: 'Back-off restarting failed container', age: '2m', ns: 'production' },
  { type: 'Warning', reason: 'Unhealthy', object: 'pod/api-gateway-6f4c8b9a3', message: 'Readiness probe failed: HTTP 503', age: '5m', ns: 'production' },
  { type: 'Warning', reason: 'OOMKilling', object: 'pod/api-gateway-6f4c8b9a3', message: 'Memory cgroup out of memory: Killed process (java)', age: '1h', ns: 'production' },
  { type: 'Normal', reason: 'ScalingReplicaSet', object: 'deployment/api-gateway', message: 'Scaled up replica set to 3', age: '2h', ns: 'production' },
  { type: 'Warning', reason: 'FailedScheduling', object: 'pod/mysql-backup', message: '0/3 nodes available: Insufficient cpu', age: '5m', ns: 'data' },
  { type: 'Normal', reason: 'Started', object: 'pod/user-service-a1b2c', message: 'Started container app', age: '30d', ns: 'production' },
  { type: 'Normal', reason: 'HealthCheck', object: 'node/k8s-worker-03', message: 'Node status is now: NodeReady', age: '30d', ns: '' },
  { type: 'Normal', reason: 'Pulled', object: 'pod/payment-service-a7b8c', message: 'Container image already present on machine', age: '60d', ns: 'production' },
];

const statusConfig: Record<string, { color: string; bg: string }> = {
  Running: { color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
  Pending: { color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
  CrashLoopBackOff: { color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
  Error: { color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
  Ready: { color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
  healthy: { color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
  progressing: { color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
  degraded: { color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
};

const eventTypeColors: Record<string, string> = { Warning: '#f59e0b', Normal: '#3b82f6', Error: '#ef4444' };

const podStatusCounts = pods.reduce((acc, p) => {
  acc[p.status] = (acc[p.status] || 0) + 1;
  return acc;
}, {} as Record<string, number>);
const pieData = Object.entries(podStatusCounts).map(([name, value]) => ({ name, value }));
const pieColors: Record<string, string> = { Running: '#10b981', Pending: '#f59e0b', CrashLoopBackOff: '#ef4444' };

const nodeCpuMem = nodes.map(n => ({ name: n.name, cpu: n.cpu, memory: n.memory }));

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 8, padding: '8px 12px', fontSize: 12 }}>
      <div style={{ color: '#94a3b8', marginBottom: 4 }}>{label}</div>
      {payload.map((p: any, i: number) => (
        <div key={i} style={{ color: p.color }}>{p.name}: <strong>{p.value}%</strong></div>
      ))}
    </div>
  );
};

export default function DeploymentPage() {
  const [tab, setTab] = useState<'overview' | 'pods' | 'events'>('overview');

  const running = pods.filter(p => p.status === 'Running').length;
  const problemPods = pods.filter(p => p.status !== 'Running').length;

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>🚀 部署管理</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>Kubernetes 集群资源 · Pod 状态 · 事件追踪</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ padding: '6px 12px', borderRadius: 8, background: 'rgba(245,158,11,0.12)', color: '#f59e0b', fontSize: 12, fontWeight: 600 }}>🟡 Demo Mode</span>
          <span style={{ padding: '6px 12px', borderRadius: 8, background: 'rgba(16,185,129,0.12)', color: '#10b981', fontSize: 12 }}>● kubectl 连接就绪</span>
        </div>
      </div>

      {/* ===== 统计卡片 ===== */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 20 }}>
        {[
          { label: 'Pod 总数', value: pods.length, icon: '📦', color: '#3b82f6', bg: 'rgba(59,130,246,0.12)' },
          { label: '运行中', value: running, icon: '✅', color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
          { label: '异常 Pod', value: problemPods, icon: '⚠️', color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
          { label: 'Deployment', value: deployments.length, icon: '🚀', color: '#8b5cf6', bg: 'rgba(139,92,246,0.12)' },
        ].map((s, i) => (
          <div key={i} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{ width: 48, height: 48, borderRadius: 12, background: s.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22 }}>{s.icon}</div>
            <div>
              <div style={{ fontSize: 12, color: '#94a3b8' }}>{s.label}</div>
              <div style={{ fontSize: 28, fontWeight: 700, color: s.color }}>{s.value}</div>
            </div>
          </div>
        ))}
      </div>

      {/* ===== Tab 按钮 ===== */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 20, background: '#111827', borderRadius: 10, padding: 4, width: 'fit-content' }}>
        {[
          { key: 'overview', label: '📊 概览' },
          { key: 'pods', label: '📦 Pod 列表' },
          { key: 'events', label: '📡 事件' },
        ].map(t => (
          <button key={t.key} onClick={() => setTab(t.key as any)}
            style={{ padding: '8px 20px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 13, fontWeight: 600, transition: 'all 0.2s',
              background: tab === t.key ? 'rgba(59,130,246,0.2)' : 'transparent',
              color: tab === t.key ? '#3b82f6' : '#94a3b8' }}>
            {t.label}
          </button>
        ))}
      </div>

      {/* ===== Tab: Overview ===== */}
      {tab === 'overview' && (
        <>
          {/* Nodes + Pod 分布 */}
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16, marginBottom: 20 }}>
            {/* Nodes 表格 */}
            <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
              <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>🖥️ 集群节点</div>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
                <thead>
                  <tr style={{ color: '#64748b', textAlign: 'left', borderBottom: '1px solid #2a3050' }}>
                    <th style={{ padding: '8px 0' }}>节点</th>
                    <th>状态</th>
                    <th>角色</th>
                    <th>版本</th>
                    <th>CPU</th>
                    <th>内存</th>
                  </tr>
                </thead>
                <tbody>
                  {nodes.map((n, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                      <td style={{ padding: '10px 0', fontFamily: 'monospace', color: '#e2e8f0' }}>{n.name}</td>
                      <td>
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4, padding: '2px 8px', borderRadius: 4, fontSize: 11, background: 'rgba(16,185,129,0.12)', color: '#10b981' }}>
                          ● {n.status}
                        </span>
                      </td>
                      <td style={{ color: '#94a3b8' }}>{n.roles}</td>
                      <td style={{ color: '#94a3b8', fontFamily: 'monospace' }}>{n.version}</td>
                      <td style={{ width: 140 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                          <div style={{ flex: 1, height: 6, background: '#2a3050', borderRadius: 3 }}>
                            <div style={{ height: '100%', width: `${n.cpu}%`, background: n.cpu > 70 ? '#ef4444' : '#3b82f6', borderRadius: 3 }} />
                          </div>
                          <span style={{ fontSize: 11, color: n.cpu > 70 ? '#ef4444' : '#94a3b8', minWidth: 30 }}>{n.cpu}%</span>
                        </div>
                      </td>
                      <td style={{ width: 140 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                          <div style={{ flex: 1, height: 6, background: '#2a3050', borderRadius: 3 }}>
                            <div style={{ height: '100%', width: `${n.memory}%`, background: n.memory > 80 ? '#ef4444' : '#8b5cf6', borderRadius: 3 }} />
                          </div>
                          <span style={{ fontSize: 11, color: n.memory > 80 ? '#ef4444' : '#94a3b8', minWidth: 30 }}>{n.memory}%</span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pod 状态饼图 */}
            <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
              <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>📊 Pod 状态分布</div>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={3}>
                    {pieData.map((entry) => (
                      <Cell key={entry.name} fill={pieColors[entry.name] || '#64748b'} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12, justifyContent: 'center', marginTop: 8 }}>
                {pieData.map(d => (
                  <div key={d.name} style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 11 }}>
                    <div style={{ width: 8, height: 8, borderRadius: 2, background: pieColors[d.name] || '#64748b' }} />
                    <span style={{ color: '#94a3b8' }}>{d.name}: <strong style={{ color: '#e2e8f0' }}>{d.value}</strong></span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Deployments 卡片网格 */}
          <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, marginBottom: 20 }}>
            <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>🚀 Deployments</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
              {deployments.map((d, i) => {
                const cfg = statusConfig[d.status] || statusConfig.Running;
                const [ready, desired] = d.ready.split('/').map(Number);
                return (
                  <div key={i} style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: 10, padding: 16, borderLeft: `3px solid ${cfg.color}` }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                      <span style={{ fontSize: 13, fontWeight: 600, color: '#e2e8f0' }}>{d.name}</span>
                      <span style={{ padding: '2px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: cfg.bg, color: cfg.color }}>{d.status}</span>
                    </div>
                    <div style={{ fontSize: 11, color: '#94a3b8', marginBottom: 6 }}>
                      <span style={{ color: '#64748b' }}>NS:</span> {d.ns} &nbsp;·&nbsp; <span style={{ color: '#64748b' }}>Age:</span> {d.age}
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <span style={{ fontSize: 11, color: '#64748b' }}>副本 </span>
                        <span style={{ fontSize: 14, fontWeight: 700, color: ready === desired ? '#10b981' : '#f59e0b' }}>{d.ready}</span>
                      </div>
                      <div style={{ fontSize: 10, color: '#64748b', fontFamily: 'monospace' }}>{d.containers}</div>
                    </div>
                    {/* 副本进度条 */}
                    <div style={{ marginTop: 8, height: 4, background: '#2a3050', borderRadius: 2 }}>
                      <div style={{ height: '100%', width: `${(ready / desired) * 100}%`, background: cfg.color, borderRadius: 2, transition: 'width 0.3s' }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 节点资源柱状图 */}
          <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
            <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>📈 节点资源使用</div>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={nodeCpuMem} barGap={4}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2a3050" />
                <XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 11 }} domain={[0, 100]} unit="%" />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="cpu" fill="#3b82f6" name="CPU" radius={[4, 4, 0, 0]} />
                <Bar dataKey="memory" fill="#8b5cf6" name="内存" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </>
      )}

      {/* ===== Tab: Pods ===== */}
      {tab === 'pods' && (
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <span style={{ fontSize: 14, fontWeight: 600 }}>📦 Pod 列表 ({pods.length})</span>
            <span style={{ fontSize: 11, color: '#64748b' }}>按状态排序</span>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
            <thead>
              <tr style={{ color: '#64748b', textAlign: 'left', borderBottom: '1px solid #2a3050' }}>
                <th style={{ padding: '8px 0' }}>状态</th>
                <th>名称</th>
                <th>命名空间</th>
                <th>就绪</th>
                <th>重启</th>
                <th>节点</th>
                <th>存活</th>
              </tr>
            </thead>
            <tbody>
              {pods.sort((a, b) => {
                const order: Record<string, number> = { CrashLoopBackOff: 0, Error: 1, Pending: 2, Running: 3 };
                return (order[a.status] ?? 4) - (order[b.status] ?? 4);
              }).map((p, i) => {
                const cfg = statusConfig[p.status] || statusConfig.Running;
                return (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)', background: p.status !== 'Running' ? 'rgba(239,68,68,0.04)' : 'transparent' }}>
                    <td style={{ padding: '10px 0' }}>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4, padding: '2px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: cfg.bg, color: cfg.color }}>
                        {p.status === 'Running' ? '●' : p.status === 'Pending' ? '◌' : '✖'} {p.status}
                      </span>
                    </td>
                    <td style={{ fontFamily: 'monospace', color: '#e2e8f0', fontSize: 11 }}>{p.name}</td>
                    <td style={{ color: '#94a3b8' }}>{p.ns}</td>
                    <td style={{ color: p.ready === '1/1' || p.ready === '2/2' ? '#10b981' : '#ef4444', fontWeight: 600 }}>{p.ready}</td>
                    <td style={{ color: p.restarts > 0 ? '#ef4444' : '#94a3b8', fontWeight: p.restarts > 0 ? 700 : 400 }}>{p.restarts}</td>
                    <td style={{ color: '#94a3b8', fontFamily: 'monospace', fontSize: 11 }}>{p.node || '-'}</td>
                    <td style={{ color: '#64748b' }}>{p.age}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* ===== Tab: Events ===== */}
      {tab === 'events' && (
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>📡 最近事件 ({events.length})</div>
          <div style={{ position: 'relative', paddingLeft: 24 }}>
            <div style={{ position: 'absolute', left: 7, top: 0, bottom: 0, width: 2, background: '#2a3050' }} />
            {events.map((e, i) => (
              <div key={i} style={{ position: 'relative', marginBottom: 16 }}>
                <div style={{ position: 'absolute', left: -21, top: 6, width: 12, height: 12, borderRadius: '50%', background: eventTypeColors[e.type] || '#64748b', border: '2px solid #1a1f35' }} />
                <div style={{ padding: '12px 16px', background: 'rgba(255,255,255,0.02)', borderRadius: 8, borderLeft: `3px solid ${eventTypeColors[e.type] || '#64748b'}` }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{ padding: '1px 6px', borderRadius: 3, fontSize: 10, fontWeight: 700, background: `${eventTypeColors[e.type]}22`, color: eventTypeColors[e.type] }}>{e.type}</span>
                      <span style={{ fontSize: 12, fontWeight: 600, color: '#e2e8f0' }}>{e.reason}</span>
                    </div>
                    <span style={{ fontSize: 10, color: '#64748b' }}>{e.age}</span>
                  </div>
                  <div style={{ fontSize: 11, color: '#94a3b8', fontFamily: 'monospace', marginBottom: 2 }}>{e.object}</div>
                  <div style={{ fontSize: 12, color: '#cbd5e1' }}>{e.message}</div>
                  {e.ns && <div style={{ fontSize: 10, color: '#64748b', marginTop: 4 }}>ns: {e.ns}</div>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
