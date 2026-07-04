import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Line, BarChart, Bar } from 'recharts';

// ===== 模拟数据：24小时CPU趋势 =====
const now = Date.now();
const cpuData = Array.from({ length: 96 }, (_, i) => {
  const t = now - (95 - i) * 900000; // 每15分钟一个点
  const hour = new Date(t).getHours();
  const base = hour >= 9 && hour <= 18 ? 55 + Math.sin((hour - 6) * Math.PI / 12) * 20 : 25 + Math.sin(hour * 0.5) * 8;
  const noise = Math.sin(i * 0.7) * 6 + Math.cos(i * 0.3) * 4;
  return {
    time: `${String(hour).padStart(2, '0')}:${String(new Date(t).getMinutes()).padStart(2, '0')}`,
    cpu: Math.max(5, Math.min(95, base + noise)),
    cpuUser: Math.max(3, Math.min(60, (base + noise) * 0.6)),
    cpuSystem: Math.max(2, Math.min(30, (base + noise) * 0.25)),
  };
});

const memData = Array.from({ length: 96 }, (_, i) => {
  const t = now - (95 - i) * 900000;
  const hour = new Date(t).getHours();
  const base = hour >= 9 && hour <= 18 ? 62 + Math.sin((hour - 6) * Math.PI / 12) * 12 : 42 + Math.sin(hour * 0.5) * 5;
  return {
    time: `${String(hour).padStart(2, '0')}:${String(new Date(t).getMinutes()).padStart(2, '0')}`,
    used: Math.max(25, Math.min(92, base + Math.sin(i * 0.5) * 4)),
    cached: Math.max(10, Math.min(30, 18 + Math.sin(i * 0.3) * 5)),
  };
});

const diskIoData = Array.from({ length: 48 }, (_, i) => {
  const t = now - (47 - i) * 1800000;
  const hour = new Date(t).getHours();
  const base = hour >= 9 && hour <= 18 ? 45 + Math.random() * 20 : 15 + Math.random() * 8;
  return {
    time: `${String(hour).padStart(2, '0')}:${String(new Date(t).getMinutes()).padStart(2, '0')}`,
    read: Math.max(5, base + Math.random() * 10),
    write: Math.max(3, base * 0.7 + Math.random() * 8),
  };
});

const netData = Array.from({ length: 48 }, (_, i) => {
  const t = now - (47 - i) * 1800000;
  const hour = new Date(t).getHours();
  const base = hour >= 9 && hour <= 18 ? 18 : 6;
  return {
    time: `${String(hour).padStart(2, '0')}:${String(new Date(t).getMinutes()).padStart(2, '0')}`,
    inbound: Math.max(1, base + Math.sin(i * 0.4) * 5 + Math.random() * 3),
    outbound: Math.max(0.5, base * 0.6 + Math.sin(i * 0.3) * 3 + Math.random() * 2),
  };
});

const alerts = [
  { severity: 'critical', name: 'DiskSpaceLow', instance: 'prod-03:9100', summary: '磁盘空间不足 10%', desc: '/data 分区使用率 93.2%，剩余 27.6GB', since: '47m', source: 'Prometheus' },
  { severity: 'warning', name: 'HighCPUUsage', instance: 'prod-02:9100', summary: 'CPU 使用率超过 80%', desc: '持续 15 分钟超过阈值，当前 87.3%', since: '19m', source: 'Prometheus' },
  { severity: 'warning', name: 'PodRestarting', instance: 'production/api-gateway', summary: 'Pod 频繁重启', desc: 'api-gateway-6f4c8b9a3 在 1h 内重启 8 次', since: '2h', source: 'K8s Events' },
];

const targets = [
  { url: 'prod-01:9100', job: 'node-exporter', health: 'up', lastScrape: '12s ago' },
  { url: 'prod-02:9100', job: 'node-exporter', health: 'up', lastScrape: '8s ago' },
  { url: 'prod-03:9100', job: 'node-exporter', health: 'up', lastScrape: '15s ago' },
  { url: 'prod-01:8080', job: 'app-metrics', health: 'up', lastScrape: '5s ago' },
  { url: 'k8s-master:6443', job: 'kube-apiserver', health: 'up', lastScrape: '3s ago' },
  { url: 'prod-04:9090', job: 'custom-exporter', health: 'down', lastScrape: '5m ago' },
];

const statusColors = { critical: '#ef4444', warning: '#f59e0b', info: '#3b82f6' };
const healthColors = { up: '#10b981', down: '#ef4444' };

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 8, padding: '10px 14px', fontSize: 12 }}>
      <div style={{ color: '#94a3b8', marginBottom: 6 }}>{label}</div>
      {payload.map((p: any, i: number) => (
        <div key={i} style={{ color: p.color, marginBottom: 2 }}>
          {p.name}: <strong>{typeof p.value === 'number' ? p.value.toFixed(1) : p.value}%</strong>
        </div>
      ))}
    </div>
  );
};

export default function MonitoringPage() {
  const latestCpu = cpuData[cpuData.length - 1]?.cpu || 0;
  const latestMem = memData[memData.length - 1]?.used || 0;

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>📊 实时监控</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>Prometheus 指标 · 24h 趋势 · 告警管理</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '6px 12px', borderRadius: 8, background: 'rgba(245,158,11,0.12)', color: '#f59e0b', fontSize: 12, fontWeight: 600 }}>
            🟡 Demo Mode
          </span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '6px 12px', borderRadius: 8, background: 'rgba(16,185,129,0.12)', color: '#10b981', fontSize: 12 }}>
            ● Prometheus 连接就绪
          </span>
        </div>
      </div>

      {/* ===== 统计卡片 ===== */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 20 }}>
        {[
          { label: 'CPU 使用率', value: `${latestCpu.toFixed(1)}%`, icon: '🖥️', color: '#3b82f6', bg: 'rgba(59,130,246,0.12)', trend: latestCpu > 50 ? '↑' : '↓', trendColor: latestCpu > 70 ? '#ef4444' : '#10b981' },
          { label: '内存使用率', value: `${latestMem.toFixed(1)}%`, icon: '💾', color: '#8b5cf6', bg: 'rgba(139,92,246,0.12)', trend: '→', trendColor: '#94a3b8' },
          { label: '磁盘使用率', value: '67.8%', icon: '📀', color: '#06b6d4', bg: 'rgba(6,182,212,0.12)', trend: '↑', trendColor: '#f59e0b' },
          { label: '活跃告警', value: '3', icon: '🚨', color: '#ef4444', bg: 'rgba(239,68,68,0.12)', trend: '+1', trendColor: '#ef4444' },
        ].map((s, i) => (
          <div key={i} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{ width: 48, height: 48, borderRadius: 12, background: s.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22 }}>{s.icon}</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 12, color: '#94a3b8', marginBottom: 4 }}>{s.label}</div>
              <div style={{ fontSize: 28, fontWeight: 700, color: s.color, lineHeight: 1 }}>{s.value}</div>
            </div>
            <div style={{ fontSize: 14, fontWeight: 600, color: s.trendColor }}>{s.trend}</div>
          </div>
        ))}
      </div>

      {/* ===== CPU 主图表 ===== */}
      <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, marginBottom: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div>
            <span style={{ fontSize: 14, fontWeight: 600 }}>CPU 使用率趋势</span>
            <span style={{ fontSize: 11, color: '#64748b', marginLeft: 10 }}>node_cpu_seconds_total · 24h</span>
          </div>
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
              <linearGradient id="cpuUserGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a3050" />
            <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 10 }} interval={11} />
            <YAxis stroke="#64748b" tick={{ fontSize: 10 }} domain={[0, 100]} unit="%" />
            <Tooltip content={<CustomTooltip />} />
            <Area type="monotone" dataKey="cpu" stroke="#3b82f6" fill="url(#cpuGrad)" strokeWidth={2} name="总计" dot={false} />
            <Area type="monotone" dataKey="cpuUser" stroke="#8b5cf6" fill="url(#cpuUserGrad)" strokeWidth={1.5} name="User" dot={false} />
            <Line type="monotone" dataKey="cpuSystem" stroke="#06b6d4" strokeWidth={1.5} name="System" dot={false} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* ===== 二级图表网格 ===== */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 20 }}>
        {/* 内存 */}
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>💾 内存趋势</div>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={memData}>
              <defs>
                <linearGradient id="memGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a3050" />
              <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 9 }} interval={11} />
              <YAxis stroke="#64748b" tick={{ fontSize: 9 }} domain={[0, 100]} unit="%" />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="used" stroke="#8b5cf6" fill="url(#memGrad)" strokeWidth={2} name="已用" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* 磁盘IO */}
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>📀 磁盘 I/O</div>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={diskIoData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a3050" />
              <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 9 }} interval={11} />
              <YAxis stroke="#64748b" tick={{ fontSize: 9 }} unit=" MB/s" />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="read" fill="#06b6d4" name="读取" radius={[2, 2, 0, 0]} />
              <Bar dataKey="write" fill="#f59e0b" name="写入" radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* 网络流量 */}
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>🌐 网络流量</div>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={netData}>
              <defs>
                <linearGradient id="netIn" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a3050" />
              <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 9 }} interval={11} />
              <YAxis stroke="#64748b" tick={{ fontSize: 9 }} unit=" Mbps" />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="inbound" stroke="#10b981" fill="url(#netIn)" strokeWidth={2} name="入站" dot={false} />
              <Line type="monotone" dataKey="outbound" stroke="#f97316" strokeWidth={1.5} name="出站" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* 采集目标 */}
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>🎯 采集目标</div>
          <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: 16 }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 32, fontWeight: 700, color: '#10b981' }}>5</div>
              <div style={{ fontSize: 11, color: '#64748b' }}>在线</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 32, fontWeight: 700, color: '#ef4444' }}>1</div>
              <div style={{ fontSize: 11, color: '#64748b' }}>离线</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 32, fontWeight: 700, color: '#3b82f6' }}>6</div>
              <div style={{ fontSize: 11, color: '#64748b' }}>总计</div>
            </div>
          </div>
          {targets.map((t, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 0', borderBottom: i < targets.length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none', fontSize: 12 }}>
              <div style={{ width: 8, height: 8, borderRadius: '50%', background: healthColors[t.health as keyof typeof healthColors] }} />
              <span style={{ color: '#e2e8f0', flex: 1, fontFamily: 'monospace' }}>{t.url}</span>
              <span style={{ color: '#94a3b8' }}>{t.job}</span>
              <span style={{ color: t.health === 'up' ? '#10b981' : '#ef4444', fontSize: 11 }}>{t.lastScrape}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ===== 告警列表 ===== */}
      <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <span style={{ fontSize: 14, fontWeight: 600 }}>🚨 活跃告警 ({alerts.length})</span>
          <span style={{ fontSize: 11, color: '#64748b' }}>Prometheus AlertManager</span>
        </div>
        {alerts.map((a, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 12, padding: '14px 16px', background: 'rgba(255,255,255,0.02)', borderRadius: 8, marginBottom: 8, borderLeft: `3px solid ${statusColors[a.severity as keyof typeof statusColors]}` }}>
            <div style={{ minWidth: 60 }}>
              <span style={{ display: 'inline-block', padding: '2px 8px', borderRadius: 4, fontSize: 10, fontWeight: 700, textTransform: 'uppercase', background: `${statusColors[a.severity as keyof typeof statusColors]}22`, color: statusColors[a.severity as keyof typeof statusColors] }}>
                {a.severity}
              </span>
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: '#e2e8f0', marginBottom: 2 }}>{a.name}</div>
              <div style={{ fontSize: 12, color: '#94a3b8' }}>{a.summary}</div>
              <div style={{ fontSize: 11, color: '#64748b', marginTop: 2 }}>{a.desc}</div>
            </div>
            <div style={{ textAlign: 'right', minWidth: 100 }}>
              <div style={{ fontSize: 11, color: '#94a3b8' }}>{a.instance}</div>
              <div style={{ fontSize: 10, color: '#64748b', marginTop: 2 }}>持续 {a.since}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
