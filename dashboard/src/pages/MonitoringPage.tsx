import { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Line } from 'recharts';
import { detectMode, fetchMonitoringSummary, fetchAlerts, fetchTargets, type MonitoringSummary, type Alert, type Target } from '../api';

// ===== 生成趋势数据（demo 模式用） =====
function genCpuData() {
  const now = Date.now();
  return Array.from({ length: 96 }, (_, i) => {
    const t = now - (95 - i) * 900000;
    const hour = new Date(t).getHours();
    const base = hour >= 9 && hour <= 18 ? 55 + Math.sin((hour - 6) * Math.PI / 12) * 20 : 25 + Math.sin(hour * 0.5) * 8;
    const noise = Math.sin(i * 0.7) * 6 + Math.cos(i * 0.3) * 4;
    return { time: `${String(hour).padStart(2, '0')}:${String(new Date(t).getMinutes()).padStart(2, '0')}`, cpu: Math.max(5, Math.min(95, base + noise)), cpuUser: Math.max(3, Math.min(60, (base + noise) * 0.6)), cpuSystem: Math.max(2, Math.min(30, (base + noise) * 0.25)) };
  });
}

function genMemData() {
  const now = Date.now();
  return Array.from({ length: 96 }, (_, i) => {
    const t = now - (95 - i) * 900000;
    const hour = new Date(t).getHours();
    const base = hour >= 9 && hour <= 18 ? 62 + Math.sin((hour - 6) * Math.PI / 12) * 12 : 42 + Math.sin(hour * 0.5) * 5;
    return { time: `${String(hour).padStart(2, '0')}:${String(new Date(t).getMinutes()).padStart(2, '0')}`, used: Math.max(25, Math.min(92, base + Math.sin(i * 0.5) * 4)) };
  });
}

function genNetData() {
  const now = Date.now();
  return Array.from({ length: 48 }, (_, i) => {
    const t = now - (47 - i) * 1800000;
    const hour = new Date(t).getHours();
    const base = hour >= 9 && hour <= 18 ? 18 : 6;
    return { time: `${String(hour).padStart(2, '0')}:${String(new Date(t).getMinutes()).padStart(2, '0')}`, inbound: Math.max(1, base + Math.sin(i * 0.4) * 5 + Math.random() * 3), outbound: Math.max(0.5, base * 0.6 + Math.sin(i * 0.3) * 3 + Math.random() * 2) };
  });
}

const statusColors: Record<string, string> = { critical: '#ef4444', warning: '#f59e0b', info: '#3b82f6' };
const healthColors: Record<string, string> = { up: '#10b981', down: '#ef4444' };

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 8, padding: '10px 14px', fontSize: 12 }}>
      <div style={{ color: '#94a3b8', marginBottom: 6 }}>{label}</div>
      {payload.map((p: any, i: number) => (
        <div key={i} style={{ color: p.color, marginBottom: 2 }}>{p.name}: <strong>{typeof p.value === 'number' ? p.value.toFixed(1) : p.value}</strong></div>
      ))}
    </div>
  );
};

export default function MonitoringPage() {
  const [summary, setSummary] = useState<MonitoringSummary | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [targets, setTargets] = useState<Target[]>([]);
  const [mode, setMode] = useState<'loading' | 'demo' | 'real'>('loading');

  useEffect(() => {
    detectMode().then(real => {
      setMode(real ? 'real' : 'demo');
      fetchMonitoringSummary().then(setSummary);
      fetchAlerts().then(setAlerts);
      fetchTargets().then(setTargets);
    });
  }, []);

  // 定时刷新
  useEffect(() => {
    if (mode !== 'real') return;
    const iv = setInterval(() => {
      fetchMonitoringSummary().then(setSummary);
      fetchAlerts().then(setAlerts);
      fetchTargets().then(setTargets);
    }, 10000);
    return () => clearInterval(iv);
  }, [mode]);

  const s = summary || { cpu_usage: 0, memory_usage: 0, disk_usage: 0, network_in_mbps: 0, total_alerts: 0, firing_alerts: 0, targets_up: 0, targets_down: 0 };
  const cpuData = genCpuData();
  const memData = genMemData();
  const netData = genNetData();

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>📊 实时监控</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>Prometheus 指标 · 趋势分析 · 告警管理</p>
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
          { label: 'CPU 使用率', value: `${s.cpu_usage.toFixed(1)}%`, icon: '🖥️', color: '#3b82f6', bg: 'rgba(59,130,246,0.12)' },
          { label: '内存使用率', value: `${s.memory_usage.toFixed(1)}%`, icon: '💾', color: '#8b5cf6', bg: 'rgba(139,92,246,0.12)' },
          { label: '磁盘使用率', value: `${s.disk_usage.toFixed(1)}%`, icon: '📀', color: '#06b6d4', bg: 'rgba(6,182,212,0.12)' },
          { label: '活跃告警', value: String(s.firing_alerts), icon: '🚨', color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
        ].map((item, i) => (
          <div key={i} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{ width: 48, height: 48, borderRadius: 12, background: item.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22 }}>{item.icon}</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 12, color: '#94a3b8', marginBottom: 4 }}>{item.label}</div>
              <div style={{ fontSize: 28, fontWeight: 700, color: item.color, lineHeight: 1 }}>{item.value}</div>
            </div>
          </div>
        ))}
      </div>

      {/* CPU 主图表 */}
      <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, marginBottom: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <span style={{ fontSize: 14, fontWeight: 600 }}>CPU 使用率趋势</span>
          <div style={{ display: 'flex', gap: 12, fontSize: 11 }}>
            <span style={{ color: '#3b82f6' }}>● 总计</span>
            <span style={{ color: '#8b5cf6' }}>● User</span>
            <span style={{ color: '#06b6d4' }}>● System</span>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={cpuData}>
            <defs>
              <linearGradient id="cpuGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a3050" />
            <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 10 }} interval={11} />
            <YAxis stroke="#64748b" tick={{ fontSize: 10 }} domain={[0, 100]} unit="%" />
            <Tooltip content={<CustomTooltip />} />
            <Area type="monotone" dataKey="cpu" stroke="#3b82f6" fill="url(#cpuGrad)" strokeWidth={2} name="总计" dot={false} />
            <Area type="monotone" dataKey="cpuUser" stroke="#8b5cf6" fill="none" strokeWidth={1.5} name="User" dot={false} />
            <Line type="monotone" dataKey="cpuSystem" stroke="#06b6d4" strokeWidth={1.5} name="System" dot={false} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* 二级图表 */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 20 }}>
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>💾 内存趋势</div>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={memData}>
              <defs><linearGradient id="memGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} /><stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} /></linearGradient></defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a3050" />
              <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 9 }} interval={11} />
              <YAxis stroke="#64748b" tick={{ fontSize: 9 }} domain={[0, 100]} unit="%" />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="used" stroke="#8b5cf6" fill="url(#memGrad)" strokeWidth={2} name="已用" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>🌐 网络流量</div>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={netData}>
              <defs><linearGradient id="netIn" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#10b981" stopOpacity={0.3} /><stop offset="95%" stopColor="#10b981" stopOpacity={0} /></linearGradient></defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a3050" />
              <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 9 }} interval={11} />
              <YAxis stroke="#64748b" tick={{ fontSize: 9 }} unit=" Mbps" />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="inbound" stroke="#10b981" fill="url(#netIn)" strokeWidth={2} name="入站" dot={false} />
              <Line type="monotone" dataKey="outbound" stroke="#f97316" strokeWidth={1.5} name="出站" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 告警 + 采集目标 */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16 }}>
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>🚨 活跃告警 ({alerts.length})</div>
          {alerts.map((a, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 12, padding: '12px 16px', background: 'rgba(255,255,255,0.02)', borderRadius: 8, marginBottom: 8, borderLeft: `3px solid ${statusColors[a.severity] || '#64748b'}` }}>
              <span style={{ display: 'inline-block', padding: '2px 8px', borderRadius: 4, fontSize: 10, fontWeight: 700, textTransform: 'uppercase', background: `${statusColors[a.severity]}22`, color: statusColors[a.severity] }}>{a.severity}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: '#e2e8f0' }}>{a.name}</div>
                <div style={{ fontSize: 12, color: '#94a3b8' }}>{a.summary}</div>
              </div>
              <div style={{ fontSize: 10, color: '#64748b' }}>持续 {a.since}</div>
            </div>
          ))}
        </div>
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>🎯 采集目标</div>
          <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: 16 }}>
            <div style={{ textAlign: 'center' }}><div style={{ fontSize: 28, fontWeight: 700, color: '#10b981' }}>{s.targets_up}</div><div style={{ fontSize: 11, color: '#64748b' }}>在线</div></div>
            <div style={{ textAlign: 'center' }}><div style={{ fontSize: 28, fontWeight: 700, color: '#ef4444' }}>{s.targets_down}</div><div style={{ fontSize: 11, color: '#64748b' }}>离线</div></div>
          </div>
          {targets.map((t, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '5px 0', borderBottom: i < targets.length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none', fontSize: 11 }}>
              <div style={{ width: 6, height: 6, borderRadius: '50%', background: healthColors[t.health] || '#64748b' }} />
              <span style={{ color: '#e2e8f0', flex: 1, fontFamily: 'monospace' }}>{t.url}</span>
              <span style={{ color: '#64748b' }}>{t.lastScrape}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
