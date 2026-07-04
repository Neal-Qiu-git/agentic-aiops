import { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { detectMode, fetchDeploymentSummary, fetchNodes, fetchPods, fetchDeployments, fetchEvents, type K8sNode, type K8sPod, type K8sDeployment, type K8sEvent, type DeploymentSummary } from '../api';

const statusConfig: Record<string, { color: string; bg: string }> = {
  Running: { color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
  Ready: { color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
  Pending: { color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
  CrashLoopBackOff: { color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
  healthy: { color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
  progressing: { color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
};
const eventTypeColors: Record<string, string> = { Warning: '#f59e0b', Normal: '#3b82f6', Error: '#ef4444' };

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 8, padding: '8px 12px', fontSize: 12 }}>
      <div style={{ color: '#94a3b8', marginBottom: 4 }}>{label}</div>
      {payload.map((p: any, i: number) => <div key={i} style={{ color: p.color }}>{p.name}: <strong>{p.value}%</strong></div>)}
    </div>
  );
};

export default function DeploymentPage() {
  const [tab, setTab] = useState<'overview' | 'pods' | 'events'>('overview');
  const [summary, setSummary] = useState<DeploymentSummary | null>(null);
  const [nodes, setNodes] = useState<K8sNode[]>([]);
  const [pods, setPods] = useState<K8sPod[]>([]);
  const [deployments, setDeployments] = useState<K8sDeployment[]>([]);
  const [events, setEvents] = useState<K8sEvent[]>([]);
  const [mode, setMode] = useState<'loading' | 'demo' | 'real'>('loading');

  useEffect(() => {
    detectMode().then(real => {
      setMode(real ? 'real' : 'demo');
      loadAll();
    });
  }, []);

  const loadAll = () => {
    fetchDeploymentSummary().then(setSummary);
    fetchNodes().then(setNodes);
    fetchPods().then(setPods);
    fetchDeployments().then(setDeployments);
    fetchEvents().then(setEvents);
  };

  useEffect(() => {
    if (mode !== 'real') return;
    const iv = setInterval(loadAll, 15000);
    return () => clearInterval(iv);
  }, [mode]);

  const s = summary || { total_pods: 0, running_pods: 0, pending_pods: 0, failed_pods: 0, total_deployments: 0, healthy_deployments: 0, total_nodes: 0, ready_nodes: 0, total_namespaces: 0 };

  const podStatusCounts = pods.reduce((acc, p) => { acc[p.status] = (acc[p.status] || 0) + 1; return acc; }, {} as Record<string, number>);
  const pieData = Object.entries(podStatusCounts).map(([name, value]) => ({ name, value }));
  const pieColors: Record<string, string> = { Running: '#10b981', Pending: '#f59e0b', CrashLoopBackOff: '#ef4444' };
  const nodeCpuMem = nodes.map(n => ({ name: n.name, cpu: n.cpu, memory: n.memory }));

  const sortedPods = [...pods].sort((a, b) => {
    const order: Record<string, number> = { CrashLoopBackOff: 0, Error: 1, Pending: 2, Running: 3 };
    return (order[a.status] ?? 4) - (order[b.status] ?? 4);
  });

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>🚀 部署管理</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>Kubernetes 集群资源 · Pod 状态 · 事件追踪</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ padding: '6px 12px', borderRadius: 8, background: mode === 'real' ? 'rgba(16,185,129,0.12)' : 'rgba(245,158,11,0.12)', color: mode === 'real' ? '#10b981' : '#f59e0b', fontSize: 12, fontWeight: 600 }}>
            {mode === 'real' ? '🟢 实时模式' : mode === 'demo' ? '🟡 Demo 模式' : '⏳ 检测中...'}
          </span>
        </div>
      </div>

      {/* 统计卡片 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 20 }}>
        {[
          { label: 'Pod 总数', value: s.total_pods, icon: '📦', color: '#3b82f6', bg: 'rgba(59,130,246,0.12)' },
          { label: '运行中', value: s.running_pods, icon: '✅', color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
          { label: '异常 Pod', value: s.pending_pods + s.failed_pods, icon: '⚠️', color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
          { label: 'Deployment', value: s.total_deployments, icon: '🚀', color: '#8b5cf6', bg: 'rgba(139,92,246,0.12)' },
        ].map((item, i) => (
          <div key={i} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{ width: 48, height: 48, borderRadius: 12, background: item.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22 }}>{item.icon}</div>
            <div><div style={{ fontSize: 12, color: '#94a3b8' }}>{item.label}</div><div style={{ fontSize: 28, fontWeight: 700, color: item.color }}>{item.value}</div></div>
          </div>
        ))}
      </div>

      {/* Tab 按钮 */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 20, background: '#111827', borderRadius: 10, padding: 4, width: 'fit-content' }}>
        {[{ key: 'overview', label: '📊 概览' }, { key: 'pods', label: '📦 Pod 列表' }, { key: 'events', label: '📡 事件' }].map(t => (
          <button key={t.key} onClick={() => setTab(t.key as any)} style={{ padding: '8px 20px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 13, fontWeight: 600, background: tab === t.key ? 'rgba(59,130,246,0.2)' : 'transparent', color: tab === t.key ? '#3b82f6' : '#94a3b8' }}>{t.label}</button>
        ))}
      </div>

      {/* Overview Tab */}
      {tab === 'overview' && (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16, marginBottom: 20 }}>
            <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
              <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>🖥️ 集群节点 ({nodes.length})</div>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
                <thead><tr style={{ color: '#64748b', textAlign: 'left', borderBottom: '1px solid #2a3050' }}>
                  <th style={{ padding: '8px 0' }}>节点</th><th>状态</th><th>角色</th><th>CPU</th><th>内存</th>
                </tr></thead>
                <tbody>
                  {nodes.map((n, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                      <td style={{ padding: '10px 0', fontFamily: 'monospace', color: '#e2e8f0' }}>{n.name}</td>
                      <td><span style={{ padding: '2px 8px', borderRadius: 4, fontSize: 11, background: 'rgba(16,185,129,0.12)', color: '#10b981' }}>● {n.status}</span></td>
                      <td style={{ color: '#94a3b8' }}>{n.roles}</td>
                      <td style={{ width: 120 }}><div style={{ display: 'flex', alignItems: 'center', gap: 6 }}><div style={{ flex: 1, height: 6, background: '#2a3050', borderRadius: 3 }}><div style={{ height: '100%', width: `${n.cpu}%`, background: n.cpu > 70 ? '#ef4444' : '#3b82f6', borderRadius: 3 }} /></div><span style={{ fontSize: 11, color: '#94a3b8', minWidth: 30 }}>{n.cpu}%</span></div></td>
                      <td style={{ width: 120 }}><div style={{ display: 'flex', alignItems: 'center', gap: 6 }}><div style={{ flex: 1, height: 6, background: '#2a3050', borderRadius: 3 }}><div style={{ height: '100%', width: `${n.memory}%`, background: n.memory > 80 ? '#ef4444' : '#8b5cf6', borderRadius: 3 }} /></div><span style={{ fontSize: 11, color: '#94a3b8', minWidth: 30 }}>{n.memory}%</span></div></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
              <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>📊 Pod 状态</div>
              <ResponsiveContainer width="100%" height={180}>
                <PieChart><Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={45} outerRadius={70} paddingAngle={3}>
                  {pieData.map(e => <Cell key={e.name} fill={pieColors[e.name] || '#64748b'} />)}
                </Pie><Tooltip /></PieChart>
              </ResponsiveContainer>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, justifyContent: 'center', marginTop: 8 }}>
                {pieData.map(d => <div key={d.name} style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 11 }}><div style={{ width: 8, height: 8, borderRadius: 2, background: pieColors[d.name] || '#64748b' }} /><span style={{ color: '#94a3b8' }}>{d.name}: <strong style={{ color: '#e2e8f0' }}>{d.value}</strong></span></div>)}
              </div>
            </div>
          </div>
          {/* Deployments */}
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
                    <div style={{ fontSize: 11, color: '#94a3b8', marginBottom: 6 }}>NS: {d.ns || d.namespace} · Age: {d.age}</div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: 14, fontWeight: 700, color: ready === desired ? '#10b981' : '#f59e0b' }}>{d.ready}</span>
                      <span style={{ fontSize: 10, color: '#64748b', fontFamily: 'monospace' }}>{d.containers}</span>
                    </div>
                    <div style={{ marginTop: 8, height: 4, background: '#2a3050', borderRadius: 2 }}><div style={{ height: '100%', width: `${(ready / desired) * 100}%`, background: cfg.color, borderRadius: 2 }} /></div>
                  </div>
                );
              })}
            </div>
          </div>
          <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
            <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>📈 节点资源</div>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={nodeCpuMem} barGap={4}><CartesianGrid strokeDasharray="3 3" stroke="#2a3050" /><XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 11 }} /><YAxis stroke="#64748b" tick={{ fontSize: 11 }} domain={[0, 100]} unit="%" /><Tooltip content={<CustomTooltip />} /><Bar dataKey="cpu" fill="#3b82f6" name="CPU" radius={[4, 4, 0, 0]} /><Bar dataKey="memory" fill="#8b5cf6" name="内存" radius={[4, 4, 0, 0]} /></BarChart>
            </ResponsiveContainer>
          </div>
        </>
      )}

      {/* Pods Tab */}
      {tab === 'pods' && (
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>📦 Pod 列表 ({pods.length})</div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
            <thead><tr style={{ color: '#64748b', textAlign: 'left', borderBottom: '1px solid #2a3050' }}>
              <th style={{ padding: '8px 0' }}>状态</th><th>名称</th><th>命名空间</th><th>就绪</th><th>重启</th><th>节点</th><th>存活</th>
            </tr></thead>
            <tbody>
              {sortedPods.map((p, i) => {
                const cfg = statusConfig[p.status] || statusConfig.Running;
                return (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)', background: p.status !== 'Running' ? 'rgba(239,68,68,0.04)' : 'transparent' }}>
                    <td style={{ padding: '10px 0' }}><span style={{ padding: '2px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: cfg.bg, color: cfg.color }}>{p.status}</span></td>
                    <td style={{ fontFamily: 'monospace', color: '#e2e8f0', fontSize: 11 }}>{p.name}</td>
                    <td style={{ color: '#94a3b8' }}>{p.namespace}</td>
                    <td style={{ color: p.ready.includes('0') ? '#ef4444' : '#10b981', fontWeight: 600 }}>{p.ready}</td>
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

      {/* Events Tab */}
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
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
