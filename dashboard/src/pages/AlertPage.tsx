import { useState, useEffect, useCallback } from 'react';
import { fetchApi, type AlertData, demoAlerts } from '../api';

export default function AlertPage() {
  const [alertData, setAlertData] = useState<AlertData>(demoAlerts);
  const [mode, setMode] = useState<'live' | 'demo'>('demo');
  const [filter, setFilter] = useState<string>('all');

  const refresh = useCallback(async () => {
    const { data, mode: m } = await fetchApi<AlertData>('/api/v1/monitoring/alerts', demoAlerts);
    setAlertData(data);
    setMode(m);
  }, []);

  useEffect(() => { refresh(); }, [refresh]);
  useEffect(() => { const t = setInterval(refresh, 15000); return () => clearInterval(t); }, [refresh]);

  const alerts = alertData.alerts;
  const filtered = filter === 'all' ? alerts : alerts.filter(a => a.severity === filter);
  const firing = alerts.filter(a => a.state === 'firing');
  const critical = firing.filter(a => a.severity === 'critical').length;
  const warning = firing.filter(a => a.severity === 'warning').length;
  const info = firing.filter(a => a.severity === 'info').length;

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">🚨 告警中心</h1>
          <p className="page-subtitle">活跃告警 · 分级处理 · 修复建议 · 15秒自动刷新</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ fontSize: 11, padding: '3px 10px', borderRadius: 8,
            background: mode === 'live' ? 'rgba(16,185,129,0.15)' : 'rgba(245,158,11,0.15)',
            color: mode === 'live' ? '#10b981' : '#f59e0b' }}>
            {mode === 'live' ? '🟢 实时' : '🟡 Demo'}
          </span>
          <span className="badge badge-red">{critical} 严重</span>
          <span className="badge badge-yellow">{warning} 警告</span>
        </div>
      </div>

      {/* 统计卡片 */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(239,68,68,0.15)'}}>🔴</div>
          <div>
            <div className="stat-value" style={{color:'var(--accent-red)'}}>{critical}</div>
            <div className="stat-label">严重告警</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(245,158,11,0.15)'}}>🟡</div>
          <div>
            <div className="stat-value" style={{color:'var(--accent-yellow)'}}>{warning}</div>
            <div className="stat-label">警告</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(59,130,246,0.15)'}}>🔵</div>
          <div>
            <div className="stat-value" style={{color:'#3b82f6'}}>{info}</div>
            <div className="stat-label">通知</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-green)'}}>✅</div>
          <div>
            <div className="stat-value">{alertData.summary.resolved}</div>
            <div className="stat-label">已恢复</div>
          </div>
        </div>
      </div>

      {/* 筛选标签 */}
      <div style={{ display: 'flex', gap: 6, marginBottom: 16 }}>
        {[
          { key: 'all', label: '全部', count: alerts.length, color: '#6b7280' },
          { key: 'critical', label: '🔴 严重', count: critical, color: '#ef4444' },
          { key: 'warning', label: '🟡 警告', count: warning, color: '#f59e0b' },
          { key: 'info', label: '🔵 通知', count: info, color: '#3b82f6' },
        ].map(opt => (
          <button key={opt.key} onClick={() => setFilter(opt.key)} style={{
            padding: '5px 12px', borderRadius: 8, cursor: 'pointer', fontSize: 11,
            border: `1px solid ${filter === opt.key ? opt.color + '60' : 'var(--border)'}`,
            background: filter === opt.key ? `${opt.color}18` : 'transparent',
            color: filter === opt.key ? opt.color : 'var(--text-secondary)',
            fontWeight: 500, transition: 'all 0.15s',
          }}>
            {opt.label} ({opt.count})
          </button>
        ))}
      </div>

      {/* 告警列表 */}
      <div className="card">
        <div className="card-header">
          <span className="card-title">活跃告警</span>
          <span className="badge badge-blue">{filtered.length} 条</span>
        </div>
        {filtered.map((a, i) => (
          <div key={i} style={{
            display: 'flex', alignItems: 'flex-start', gap: 12,
            padding: '12px 0',
            borderBottom: i < filtered.length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none',
            opacity: a.silenced ? 0.5 : 1,
          }}>
            <div style={{
              width: 8, height: 8, borderRadius: '50%', marginTop: 6, flexShrink: 0,
              background: a.severity === 'critical' ? '#ef4444' : a.severity === 'warning' ? '#f59e0b' : '#3b82f6',
            }} />
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontSize: 13, fontWeight: 600 }}>{a.name}</span>
                <div style={{ display: 'flex', gap: 6 }}>
                  {a.silenced && <span className="badge" style={{ background: 'rgba(107,114,128,0.2)', color: '#9ca3af', fontSize: 10 }}>🔇 静默</span>}
                  {a.runbook_url && <span style={{ fontSize: 10, color: '#3b82f6', cursor: 'pointer' }}>📋 Runbook</span>}
                  <span className={`badge ${a.severity === 'critical' ? 'badge-red' : a.severity === 'warning' ? 'badge-yellow' : 'badge-blue'}`} style={{ fontSize: 10 }}>{a.severity}</span>
                </div>
              </div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 4 }}>{a.description}</div>
              <div style={{ display: 'flex', gap: 12, fontSize: 11, color: 'var(--text-muted)' }}>
                <span>📡 {a.instance}</span>
                <span>⏱️ {a.started_at}</span>
                {a.labels && Object.entries(a.labels).slice(0, 2).map(([k, v]) => (
                  <span key={k} style={{ fontFamily: 'monospace' }}>{k}={v}</span>
                ))}
              </div>
            </div>
          </div>
        ))}
        {filtered.length === 0 && (
          <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
            <div style={{ fontSize: 32, marginBottom: 8 }}>✅</div>
            <div>暂无活跃告警</div>
          </div>
        )}
      </div>
    </div>
  );
}
