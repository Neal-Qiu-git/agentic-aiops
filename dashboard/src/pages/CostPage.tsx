import { useState, useEffect, useCallback } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { fetchApi, demoCostData, type CostData } from '../api';

// 优化建议数据
const recommendations = [
  { type: 'savings', provider: 'AWS', resource: 'ec2-prod-05', action: '降配 m5.xlarge → m5.large', savings: 280, confidence: 92 },
  { type: 'savings', provider: '阿里云', resource: 'ecs-dev-03', action: '关机 (非工作时间)', savings: 156, confidence: 95 },
  { type: 'savings', provider: 'AWS', resource: 'rds-backup', action: '清理 30 天前备份', savings: 89, confidence: 88 },
  { type: 'savings', provider: '华为云', resource: 'ecs-burst-01', action: '弹性伸缩替代固定实例', savings: 120, confidence: 78 },
];

const providerColors: Record<string, string> = {
  '阿里云': '#ff6a00', 'AWS': '#ff9900', '华为云': '#cf0a2c', '腾讯云': '#006eff', 'Azure': '#0078d4',
};

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, padding: '8px 12px', fontSize: 12 }}>
      <div style={{ fontWeight: 600 }}>{payload[0].name || payload[0].payload?.provider}</div>
      <div style={{ color: '#10b981' }}>¥{payload[0].value?.toLocaleString()}</div>
    </div>
  );
};

export default function CostPage() {
  const [costData, setCostData] = useState<CostData[]>(demoCostData);
  const [mode, setMode] = useState<'live' | 'demo'>('demo');

  const refresh = useCallback(async () => {
    const { data, mode: m } = await fetchApi<CostData[]>('/api/v1/cost/summary', demoCostData);
    setCostData(data);
    setMode(m);
  }, []);

  useEffect(() => { refresh(); }, [refresh]);
  useEffect(() => { const t = setInterval(refresh, 60000); return () => clearInterval(t); }, [refresh]);

  // 按云厂商汇总
  const providerMap: Record<string, { total: number; services: { name: string; cost: number }[] }> = {};
  costData.forEach(c => {
    if (!providerMap[c.provider]) providerMap[c.provider] = { total: 0, services: [] };
    providerMap[c.provider].total += c.monthly;
    providerMap[c.provider].services.push({ name: c.service, cost: c.monthly });
  });
  const providers = Object.entries(providerMap).sort((a, b) => b[1].total - a[1].total);

  const totalMonthly = costData.reduce((a, c) => a + c.monthly, 0);
  const totalSavings = recommendations.reduce((a, r) => a + r.savings, 0);
  const chartData = providers.map(([name, v]) => ({ name, value: v.total }));
  const pieColors = ['#ff6a00', '#ff9900', '#cf0a2c', '#006eff', '#0078d4'];

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">💰 成本分析</h1>
          <p className="page-subtitle">多云费用汇总 · 服务明细 · 优化建议 · 实时数据</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ fontSize: 11, padding: '3px 10px', borderRadius: 8,
            background: mode === 'live' ? 'rgba(16,185,129,0.15)' : 'rgba(245,158,11,0.15)',
            color: mode === 'live' ? '#10b981' : '#f59e0b' }}>
            {mode === 'live' ? '🟢 实时' : '🟡 Demo'}
          </span>
          <span className="badge badge-blue">本月</span>
        </div>
      </div>

      {/* 统计卡片 */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-blue)'}}>💸</div>
          <div>
            <div className="stat-value">¥{(totalMonthly / 10000).toFixed(1)}万</div>
            <div className="stat-label">本月总成本</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-green)'}}>📊</div>
          <div>
            <div className="stat-value">{providers.length}</div>
            <div className="stat-label">云平台</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(245,158,11,0.15)'}}>💡</div>
          <div>
            <div className="stat-value">¥{totalSavings}</div>
            <div className="stat-label">可节省/月</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-purple)'}}>📈</div>
          <div>
            <div className="stat-value">{costData.length}</div>
            <div className="stat-label">计费服务</div>
          </div>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 16 }}>
        {/* 费用分布饼图 */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">费用分布</span>
          </div>
          <div style={{ height: 200 }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={chartData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" label={({ name, percent }: any) => `${name} ${((percent || 0) * 100).toFixed(0)}%`} labelLine={false}>
                  {chartData.map((_: any, i: number) => <Cell key={i} fill={pieColors[i % pieColors.length]} />)}
                </Pie>
                <Tooltip formatter={(v: any) => `¥${Number(v).toLocaleString()}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 云厂商对比 */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">厂商对比</span>
          </div>
          <div style={{ height: 200 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis type="number" tick={{ fontSize: 10, fill: '#64748b' }} tickFormatter={v => `¥${(v/10000).toFixed(0)}万`} />
                <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: '#94a3b8' }} width={60} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {chartData.map((entry, i) => <Cell key={i} fill={pieColors[i % pieColors.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* 各厂商服务明细 */}
      <div style={{ display: 'grid', gridTemplateColumns: `repeat(${Math.min(providers.length, 4)}, 1fr)`, gap: 12, marginBottom: 16 }}>
        {providers.map(([name, v]) => {
          const color = providerColors[name] || '#6b7280';
          return (
            <div key={name} className="card" style={{ padding: '14px 16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                <span style={{ fontWeight: 700, fontSize: 14, color }}>{name}</span>
                <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{v.services.length} 服务</span>
              </div>
              <div style={{ fontSize: 22, fontWeight: 700, marginBottom: 10 }}>¥{v.total.toLocaleString()}</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                {v.services.sort((a, b) => b.cost - a.cost).map(s => (
                  <div key={s.name} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11 }}>
                    <span style={{ color: 'var(--text-secondary)' }}>{s.name}</span>
                    <span style={{ fontWeight: 600 }}>¥{s.cost.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* 优化建议 */}
      <div className="card">
        <div className="card-header">
          <span className="card-title">💡 优化建议</span>
          <span className="badge badge-green">可节省 ¥{totalSavings}/月</span>
        </div>
        {recommendations.map((r, i) => (
          <div key={i} style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '12px 0',
            borderBottom: i < recommendations.length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none',
          }}>
            <div>
              <div style={{ fontSize: 13, fontWeight: 500 }}>{r.action}</div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{r.provider} · {r.resource} · 置信度 {r.confidence}%</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: 14, fontWeight: 700, color: 'var(--accent-green)' }}>-¥{r.savings}/月</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
