import { useState, useEffect, useCallback } from 'react';
import { fetchApi, type EventLog, demoEvents } from '../api';

const typeConfig: Record<string, { color: string; label: string }> = {
  error: { color: '#ef4444', label: '错误' },
  warning: { color: '#f59e0b', label: '警告' },
  info: { color: '#3b82f6', label: '信息' },
  success: { color: '#10b981', label: '成功' },
};

export default function EventsPage() {
  const [events, setEvents] = useState<EventLog[]>(demoEvents);
  const [mode, setMode] = useState<'loading' | 'demo' | 'real'>('loading');
  const [filter, setFilter] = useState<string>('all');

  const load = useCallback(async () => {
    const r = await fetchApi<EventLog[]>('/api/v1/events', demoEvents);
    setEvents(r.data);
    setMode(r.mode === 'live' ? 'real' : 'demo');
  }, []);

  useEffect(() => { load(); }, [load]);
  useEffect(() => {
    if (mode !== 'real') return;
    const iv = setInterval(load, 10000);
    return () => clearInterval(iv);
  }, [mode, load]);

  const filtered = filter === 'all' ? events : events.filter(e => e.level === filter);
  const counts = { error: events.filter(e => e.level === 'error').length, warning: events.filter(e => e.level === 'warning').length, info: events.filter(e => e.level === 'info').length };

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>📡 事件日志</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>实时事件流 · 告警记录</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ padding: '6px 12px', borderRadius: 8, background: mode === 'real' ? 'rgba(16,185,129,0.12)' : 'rgba(245,158,11,0.12)', color: mode === 'real' ? '#10b981' : '#f59e0b', fontSize: 12, fontWeight: 600 }}>
            {mode === 'real' ? '🟢 实时模式' : mode === 'demo' ? '🟡 Demo 模式' : '⏳ 检测中...'}
          </span>
        </div>
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 20, background: '#111827', borderRadius: 10, padding: 4, width: 'fit-content' }}>
        {[
          { key: 'all', label: `全部 (${events.length})` },
          { key: 'error', label: `🔴 ${counts.error}` },
          { key: 'warning', label: `🟡 ${counts.warning}` },
          { key: 'info', label: `🔵 ${counts.info}` },
        ].map(t => (
          <button key={t.key} onClick={() => setFilter(t.key)} style={{ padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: 600, background: filter === t.key ? 'rgba(59,130,246,0.2)' : 'transparent', color: filter === t.key ? '#3b82f6' : '#94a3b8' }}>
            {t.label}
          </button>
        ))}
      </div>

      {/* Events Table */}
      <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #2a3050' }}>
              {['时间', '级别', '来源', '事件', '描述'].map(h => (
                <th key={h} style={{ padding: '10px 12px', textAlign: 'left', color: '#64748b', fontWeight: 500 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((e, i) => {
              const config = typeConfig[e.level] || typeConfig.info;
              return (
                <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                  <td style={{ padding: '10px 12px', color: '#64748b', fontFamily: 'monospace', fontSize: 11 }}>{e.time}</td>
                  <td style={{ padding: '10px 12px' }}>
                    <span style={{ padding: '3px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: `${config.color}20`, color: config.color }}>
                      {config.label}
                    </span>
                  </td>
                  <td style={{ padding: '10px 12px', color: '#94a3b8', fontSize: 11 }}>{e.source}</td>
                  <td style={{ padding: '10px 12px', fontWeight: 500, color: '#e2e8f0' }}>{e.title}</td>
                  <td style={{ padding: '10px 12px', color: '#94a3b8', maxWidth: 300 }}>{e.description}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
