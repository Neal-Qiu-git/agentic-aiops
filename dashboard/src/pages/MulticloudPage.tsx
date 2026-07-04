import { useState, useEffect, useCallback } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { fetchApi, type MulticloudData, demoMulticloud } from '../api';

const providerIcons: Record<string, string> = { '阿里云': '🟣', 'AWS': '🟠', '华为云': '🔴', '腾讯云': '🔵', 'Azure': '🔵', 'GCP': '🔴' };
const statusConfig: Record<string, { color: string; bg: string }> = {
  healthy: { color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
  degraded: { color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
  error: { color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
};

export default function MulticloudPage() {
  const [clouds, setClouds] = useState<MulticloudData[]>(demoMulticloud);
  const [mode, setMode] = useState<'loading' | 'demo' | 'real'>('loading');

  const load = useCallback(async () => {
    const r = await fetchApi<MulticloudData[]>('/api/v1/multicloud', demoMulticloud);
    setClouds(r.data);
    setMode(r.mode === 'live' ? 'real' : 'demo');
  }, []);

  useEffect(() => { load(); }, [load]);
  useEffect(() => {
    if (mode !== 'real') return;
    const iv = setInterval(load, 30000);
    return () => clearInterval(iv);
  }, [mode, load]);

  const totalCost = clouds.reduce((a, c) => a + c.monthly_cost, 0);
  const totalInstances = clouds.reduce((a, c) => a + c.instances, 0);
  const costData = clouds.map(c => ({ name: c.provider, value: c.monthly_cost }));
  const pieColors = ['#8b5cf6', '#f97316', '#ef4444', '#3b82f6', '#06b6d4'];

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>☁️ 多云概览</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>{clouds.length} 个云平台 · 统一管理</p>
        </div>
        <span style={{ padding: '6px 12px', borderRadius: 8, background: mode === 'real' ? 'rgba(16,185,129,0.12)' : 'rgba(245,158,11,0.12)', color: mode === 'real' ? '#10b981' : '#f59e0b', fontSize: 12, fontWeight: 600 }}>
          {mode === 'real' ? '🟢 实时' : '🟡 Demo'}
        </span>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 20 }}>
        {[
          { label: '云平台', value: clouds.length, icon: '☁️', color: '#3b82f6', bg: 'rgba(59,130,246,0.12)' },
          { label: '总实例', value: totalInstances, icon: '🖥️', color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
          { label: '月费用', value: `¥${(totalCost / 10000).toFixed(1)}万`, icon: '💰', color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
          { label: '告警', value: clouds.reduce((a, c) => a + c.regions.length, 0), icon: '🔔', color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
        ].map((item, i) => (
          <div key={i} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{ width: 48, height: 48, borderRadius: 12, background: item.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22 }}>{item.icon}</div>
            <div><div style={{ fontSize: 12, color: '#94a3b8' }}>{item.label}</div><div style={{ fontSize: 28, fontWeight: 700, color: item.color }}>{item.value}</div></div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16, marginBottom: 20 }}>
        {/* Cloud Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          {clouds.map((c, i) => {
            const cfg = statusConfig[c.status] || statusConfig.healthy;
            return (
              <div key={i} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, borderLeft: `3px solid ${cfg.color}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ fontSize: 24 }}>{providerIcons[c.provider] || '☁️'}</span>
                    <span style={{ fontSize: 16, fontWeight: 700, color: '#e2e8f0' }}>{c.provider}</span>
                  </div>
                  <span style={{ padding: '3px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: cfg.bg, color: cfg.color }}>{c.status}</span>
                </div>
                <div style={{ fontSize: 11, color: '#94a3b8', marginBottom: 8 }}>
                  {c.regions.join(' · ')}
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8 }}>
                  <div style={{ textAlign: 'center', padding: 8, background: 'rgba(255,255,255,0.02)', borderRadius: 8 }}>
                    <div style={{ fontSize: 18, fontWeight: 700, color: '#3b82f6' }}>{c.instances}</div>
                    <div style={{ fontSize: 10, color: '#64748b' }}>实例</div>
                  </div>
                  <div style={{ textAlign: 'center', padding: 8, background: 'rgba(255,255,255,0.02)', borderRadius: 8 }}>
                    <div style={{ fontSize: 18, fontWeight: 700, color: '#f59e0b' }}>¥{(c.monthly_cost / 1000).toFixed(0)}k</div>
                    <div style={{ fontSize: 10, color: '#64748b' }}>月费</div>
                  </div>
                  <div style={{ textAlign: 'center', padding: 8, background: 'rgba(255,255,255,0.02)', borderRadius: 8 }}>
                    <div style={{ fontSize: 14, fontWeight: 600, color: '#10b981', marginTop: 4 }}>{c.services.length}</div>
                    <div style={{ fontSize: 10, color: '#64748b' }}>服务</div>
                  </div>
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 10 }}>
                  {c.services.map((s, j) => (
                    <span key={j} style={{ padding: '2px 6px', borderRadius: 4, fontSize: 9, background: 'rgba(59,130,246,0.1)', color: '#60a5fa' }}>{s}</span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Cost Pie */}
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>💰 费用分布</div>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={costData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" label={({ name, percent }: any) => `${name} ${((percent || 0) * 100).toFixed(0)}%`} labelLine={false}>
                {costData.map((_: any, i: number) => <Cell key={i} fill={pieColors[i % pieColors.length]} />)}
              </Pie>
              <Tooltip formatter={(v: any) => `¥${Number(v).toLocaleString()}`} />
            </PieChart>
          </ResponsiveContainer>
          <div style={{ borderTop: '1px solid #2a3050', paddingTop: 12, marginTop: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#94a3b8' }}>
              <span>总月费</span>
              <span style={{ fontWeight: 700, color: '#f59e0b' }}>¥{totalCost.toLocaleString()}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
