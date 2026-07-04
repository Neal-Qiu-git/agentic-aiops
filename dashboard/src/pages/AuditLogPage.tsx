import { useState, useEffect, useCallback } from 'react';
import { fetchApi } from '../api';

interface AuditLog {
  id: string; time: string; user: string; action: string;
  resource: string; detail: string; ip: string; result: string;
}

const demoLogs: AuditLog[] = [
  { id: 'LOG-001', time: '14:32:15', user: 'admin', action: '部署', resource: 'nginx-frontend', detail: '滚动更新 v2.3.1 → v2.3.2', ip: '10.0.1.100', result: 'success' },
  { id: 'LOG-002', time: '14:28:03', user: 'sre-bot', action: '告警处理', resource: 'HighCPUUsage', detail: '自动扩容 worker-03', ip: '10.0.1.50', result: 'success' },
  { id: 'LOG-003', time: '14:15:42', user: 'devops', action: '配置变更', resource: 'nginx.conf', detail: '更新 upstream 配置', ip: '10.0.1.200', result: 'success' },
  { id: 'LOG-004', time: '14:02:18', user: 'security-bot', action: '安全扫描', resource: 'docker-image', detail: '扫描 nginx:1.25 镜像 CVE', ip: '10.0.1.50', result: 'warning' },
  { id: 'LOG-005', time: '13:45:00', user: 'admin', action: '权限变更', resource: 'user-service', detail: '授权 devops 用户部署权限', ip: '10.0.1.100', result: 'success' },
  { id: 'LOG-006', time: '13:30:22', user: 'sre-bot', action: '备份', resource: 'postgres-primary', detail: '每日全量备份完成', ip: '10.0.1.50', result: 'success' },
  { id: 'LOG-007', time: '13:15:11', user: 'devops', action: '回滚', resource: 'api-gateway', detail: '版本 v2.3.0 → v2.2.9', ip: '10.0.1.200', result: 'success' },
  { id: 'LOG-008', time: '13:00:00', user: 'admin', action: '用户管理', resource: 'platform', detail: '创建新用户 devops-02', ip: '10.0.1.100', result: 'success' },
];

const actionColors: Record<string, string> = {
  '部署': '#3b82f6', '告警处理': '#f59e0b', '配置变更': '#8b5cf6',
  '安全扫描': '#ef4444', '权限变更': '#ec4899', '备份': '#10b981',
  '回滚': '#f97316', '用户管理': '#06b6d4',
};

export default function AuditLogPage() {
  const [logs, setLogs] = useState(demoLogs);
  const [filter, setFilter] = useState('all');
  const [mode, setMode] = useState<'demo' | 'real'>('demo');

  const load = useCallback(async () => {
    const r = await fetchApi<AuditLog[]>('/api/v1/audit', demoLogs);
    setLogs(r.data);
    setMode(r.mode === 'live' ? 'real' : 'demo');
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = filter === 'all' ? logs : logs.filter(l => l.action === filter);
  const actions = [...new Set(logs.map(l => l.action))];

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>📋 审计日志</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>操作审计 · 变更追踪 · 合规记录</p>
        </div>
        <span style={{ padding: '6px 12px', borderRadius: 8, background: mode === 'real' ? 'rgba(16,185,129,0.12)' : 'rgba(245,158,11,0.12)', color: mode === 'real' ? '#10b981' : '#f59e0b', fontSize: 12, fontWeight: 600 }}>
          {mode === 'real' ? '🟢 实时' : '🟡 Demo'}
        </span>
      </div>

      {/* Filter */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 20, background: '#111827', borderRadius: 10, padding: 4, width: 'fit-content' }}>
        <button onClick={() => setFilter('all')} style={{ padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: 600, background: filter === 'all' ? 'rgba(59,130,246,0.2)' : 'transparent', color: filter === 'all' ? '#3b82f6' : '#94a3b8' }}>
          全部 ({logs.length})
        </button>
        {actions.map(a => (
          <button key={a} onClick={() => setFilter(a)} style={{ padding: '8px 12px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: 600, background: filter === a ? `${actionColors[a] || '#3b82f6'}20` : 'transparent', color: filter === a ? (actionColors[a] || '#3b82f6') : '#94a3b8' }}>
            {a}
          </button>
        ))}
      </div>

      {/* Log Table */}
      <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #2a3050' }}>
              {['时间', '用户', '操作', '资源', '详情', 'IP', '结果'].map(h => (
                <th key={h} style={{ padding: '10px 12px', textAlign: 'left', color: '#64748b', fontWeight: 500 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((log, i) => (
              <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                <td style={{ padding: '10px 12px', color: '#64748b', fontFamily: 'monospace', fontSize: 11 }}>{log.time}</td>
                <td style={{ padding: '10px 12px', fontWeight: 500, color: '#e2e8f0' }}>{log.user}</td>
                <td style={{ padding: '10px 12px' }}>
                  <span style={{ padding: '3px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: `${actionColors[log.action] || '#3b82f6'}20`, color: actionColors[log.action] || '#3b82f6' }}>
                    {log.action}
                  </span>
                </td>
                <td style={{ padding: '10px 12px', fontFamily: 'monospace', fontSize: 11, color: '#94a3b8' }}>{log.resource}</td>
                <td style={{ padding: '10px 12px', color: '#94a3b8', maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{log.detail}</td>
                <td style={{ padding: '10px 12px', color: '#64748b', fontFamily: 'monospace', fontSize: 10 }}>{log.ip}</td>
                <td style={{ padding: '10px 12px' }}>
                  <span style={{ padding: '3px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: log.result === 'success' ? 'rgba(16,185,129,0.12)' : log.result === 'warning' ? 'rgba(245,158,11,0.12)' : 'rgba(239,68,68,0.12)', color: log.result === 'success' ? '#10b981' : log.result === 'warning' ? '#f59e0b' : '#ef4444' }}>
                    {log.result === 'success' ? '✅ 成功' : log.result === 'warning' ? '⚠️ 警告' : '❌ 失败'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Export */}
      <div style={{ marginTop: 16, display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
        <button onClick={() => {
          const header = '时间,用户,操作,资源,详情,IP,结果\n';
          const rows = filtered.map(l => `${l.time},${l.user},${l.action},${l.resource},"${l.detail}",${l.ip},${l.result}`).join('\n');
          const blob = new Blob([header + rows], { type: 'text/csv;charset=utf-8;' });
          const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'audit-log.csv'; a.click();
        }} style={{ padding: '8px 16px', borderRadius: 6, border: '1px solid #2a3050', background: 'transparent', color: '#94a3b8', cursor: 'pointer', fontSize: 12 }}>
          📥 导出 CSV
        </button>
        <button onClick={() => {
          const blob = new Blob([JSON.stringify(filtered, null, 2)], { type: 'application/json' });
          const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'audit-log.json'; a.click();
        }} style={{ padding: '8px 16px', borderRadius: 6, border: '1px solid #2a3050', background: 'transparent', color: '#94a3b8', cursor: 'pointer', fontSize: 12 }}>
          📤 导出 JSON
        </button>
      </div>
    </div>
  );
}
