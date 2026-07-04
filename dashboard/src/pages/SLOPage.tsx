import { useState, useEffect, useCallback } from 'react';
import { fetchApi, type SLOData, demoSLOs } from '../api';

interface Incident {
  id: string; title: string; severity: string; started: string;
  mttr: string; status: string; rootCause: string;
}
const demoIncidents: Incident[] = [
  { id: 'INC-2847', title: 'API 网关超时', severity: 'P1', started: '08:32', mttr: '4m 23s', status: 'resolved', rootCause: '上游服务连接池耗尽' },
  { id: 'INC-2846', title: 'Kafka 消费延迟', severity: 'P2', started: '07:15', mttr: '12m 08s', status: 'resolved', rootCause: 'Consumer Group rebalance' },
  { id: 'INC-2845', title: '数据库慢查询', severity: 'P2', started: '06:48', mttr: '8m 45s', status: 'resolved', rootCause: '缺少索引' },
];

export default function SLOPage() {
  const [slos, setSlos] = useState<SLOData[]>(demoSLOs);
  const [mode, setMode] = useState<'loading' | 'demo' | 'real'>('loading');

  const load = useCallback(async () => {
    const r = await fetchApi<SLOData[]>('/api/v1/slo', demoSLOs);
    setSlos(r.data);
    setMode(r.mode === 'live' ? 'real' : 'demo');
  }, []);

  useEffect(() => { load(); }, [load]);
  useEffect(() => {
    if (mode !== 'real') return;
    const iv = setInterval(load, 30000);
    return () => clearInterval(iv);
  }, [mode, load]);

  const totalBudget = slos.reduce((a, s) => a + (100 - s.error_budget_remaining), 0) / slos.length;
  const okCount = slos.filter(s => s.status === 'healthy').length;

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>🎯 SLO 仪表盘</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>SLI/SLO 追踪 · 错误预算 · MTTR</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ padding: '6px 12px', borderRadius: 8, background: mode === 'real' ? 'rgba(16,185,129,0.12)' : 'rgba(245,158,11,0.12)', color: mode === 'real' ? '#10b981' : '#f59e0b', fontSize: 12, fontWeight: 600 }}>
            {mode === 'real' ? '🟢 实时模式' : mode === 'demo' ? '🟡 Demo 模式' : '⏳ 检测中...'}
          </span>
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 20 }}>
        {[
          { label: 'SLO 达标', value: `${okCount}/${slos.length}`, icon: '✅', color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
          { label: '平均 MTTR', value: '4m 23s', icon: '⏱️', color: '#3b82f6', bg: 'rgba(59,130,246,0.12)' },
          { label: '预算消耗', value: `${totalBudget.toFixed(0)}%`, icon: '💰', color: totalBudget > 50 ? '#ef4444' : '#f59e0b', bg: totalBudget > 50 ? 'rgba(239,68,68,0.12)' : 'rgba(245,158,11,0.12)' },
          { label: '本月事件', value: '3', icon: '📊', color: '#8b5cf6', bg: 'rgba(139,92,246,0.12)' },
        ].map((item, i) => (
          <div key={i} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{ width: 48, height: 48, borderRadius: 12, background: item.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22 }}>{item.icon}</div>
            <div><div style={{ fontSize: 12, color: '#94a3b8' }}>{item.label}</div><div style={{ fontSize: 28, fontWeight: 700, color: item.color }}>{item.value}</div></div>
          </div>
        ))}
      </div>

      {/* SLO Table */}
      <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, marginBottom: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <span style={{ fontSize: 14, fontWeight: 600 }}>SLO 追踪</span>
          <span style={{ padding: '4px 10px', borderRadius: 6, background: 'rgba(16,185,129,0.12)', color: '#10b981', fontSize: 11 }}>过去 30 天</span>
        </div>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #2a3050' }}>
              {['SLO 名称', '目标', '当前值', '描述', '错误预算', '状态'].map(h => (
                <th key={h} style={{ padding: '10px 12px', textAlign: 'left', color: '#64748b', fontWeight: 500 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {slos.map((s, i) => {
              const budgetUsed = 100 - s.error_budget_remaining;
              return (
                <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                  <td style={{ padding: '10px 12px', fontWeight: 600, color: '#e2e8f0' }}>{s.name}</td>
                  <td style={{ padding: '10px 12px', color: '#94a3b8' }}>{s.target}{s.slo_type === 'latency' ? 'ms' : s.slo_type === 'error_rate' ? '%' : '%'}</td>
                  <td style={{ padding: '10px 12px', color: s.status === 'healthy' ? '#10b981' : '#f59e0b', fontWeight: 600 }}>{s.current}{s.slo_type === 'latency' ? 'ms' : s.slo_type === 'error_rate' ? '%' : '%'}</td>
                  <td style={{ padding: '10px 12px', color: '#64748b', fontSize: 11 }}>{s.description}</td>
                  <td style={{ padding: '10px 12px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <div style={{ flex: 1, height: 6, background: '#2a3050', borderRadius: 3 }}>
                        <div style={{ height: '100%', width: `${budgetUsed}%`, background: budgetUsed > 80 ? '#ef4444' : budgetUsed > 50 ? '#f59e0b' : '#10b981', borderRadius: 3 }} />
                      </div>
                      <span style={{ fontSize: 11, color: '#94a3b8', whiteSpace: 'nowrap' }}>{s.error_budget_remaining}%</span>
                    </div>
                  </td>
                  <td style={{ padding: '10px 12px' }}>
                    <span style={{ padding: '3px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: s.status === 'healthy' ? 'rgba(16,185,129,0.12)' : 'rgba(245,158,11,0.12)', color: s.status === 'healthy' ? '#10b981' : '#f59e0b' }}>
                      {s.status === 'healthy' ? '达标' : '告警'}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Incident Timeline */}
      <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <span style={{ fontSize: 14, fontWeight: 600 }}>事件时间线</span>
          <span style={{ padding: '4px 10px', borderRadius: 6, background: 'rgba(59,130,246,0.12)', color: '#3b82f6', fontSize: 11 }}>本月 3 起</span>
        </div>
        {demoIncidents.map((inc, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 12, padding: '12px 0', borderBottom: i < demoIncidents.length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none' }}>
            <div style={{ width: 8, height: 8, borderRadius: '50%', background: inc.severity === 'P1' ? '#ef4444' : '#f59e0b', marginTop: 6, flexShrink: 0 }} />
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontSize: 13, fontWeight: 600, color: '#e2e8f0' }}>{inc.id} {inc.title}</span>
                <span style={{ padding: '2px 8px', borderRadius: 4, fontSize: 10, background: 'rgba(16,185,129,0.12)', color: '#10b981' }}>{inc.status}</span>
              </div>
              <div style={{ fontSize: 11, color: '#94a3b8' }}>
                {inc.severity} · 开始 {inc.started} · MTTR {inc.mttr} · 根因: {inc.rootCause}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
