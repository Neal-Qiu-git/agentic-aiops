import { useState } from 'react';

interface DataSource {
  id: string; name: string; type: string; endpoint: string;
  auth_type: string; enabled: boolean; status: string;
  last_check: string; metrics_count?: number;
}

const defaultSources: DataSource[] = [
  { id: 'prometheus-1', name: 'Prometheus 主集群', type: 'prometheus', endpoint: 'http://prometheus:9090', auth_type: 'none', enabled: true, status: 'connected', last_check: '10s 前', metrics_count: 1247 },
  { id: 'prometheus-2', name: 'Prometheus 备集群', type: 'prometheus', endpoint: 'http://prometheus-standby:9090', auth_type: 'none', enabled: true, status: 'connected', last_check: '12s 前', metrics_count: 1189 },
  { id: 'grafana-1', name: 'Grafana 监控', type: 'grafana', endpoint: 'http://grafana:3000', auth_type: 'token', enabled: true, status: 'connected', last_check: '5s 前', metrics_count: 86 },
  { id: 'k8s-1', name: 'K8s 集群 Prod', type: 'kubernetes', endpoint: 'https://k8s-prod:6443', auth_type: 'tls', enabled: true, status: 'connected', last_check: '8s 前', metrics_count: 342 },
  { id: 'k8s-2', name: 'K8s 集群 Staging', type: 'kubernetes', endpoint: 'https://k8s-staging:6443', auth_type: 'tls', enabled: true, status: 'connected', last_check: '15s 前', metrics_count: 128 },
  { id: 'es-1', name: 'Elasticsearch 日志', type: 'elasticsearch', endpoint: 'http://elasticsearch:9200', auth_type: 'basic', enabled: false, status: 'disconnected', last_check: '2分钟前' },
  { id: 'loki-1', name: 'Loki 日志', type: 'loki', endpoint: 'http://loki:3100', auth_type: 'none', enabled: true, status: 'connected', last_check: '3s 前', metrics_count: 0 },
  { id: 'redis-1', name: 'Redis 缓存', type: 'redis', endpoint: 'redis://redis-cluster:6379', auth_type: 'none', enabled: false, status: 'disconnected', last_check: '1小时前' },
];

const typeIcons: Record<string, string> = {
  prometheus: '📊', grafana: '📈', kubernetes: '☸️', elasticsearch: '🔍',
  loki: '📋', redis: '🗄️', mysql: '🐬', postgres: '🐘',
};
const typeColors: Record<string, string> = {
  prometheus: '#e6522c', grafana: '#f46800', kubernetes: '#326ce5', elasticsearch: '#005571',
  loki: '#f56e00', redis: '#dc382d', mysql: '#00758f', postgres: '#336791',
};

export default function DataSourcePage() {
  const [sources, setSources] = useState(defaultSources);
  const [filter, setFilter] = useState('all');

  const toggleSource = (id: string) => {
    setSources(prev => prev.map(s =>
      s.id === id ? { ...s, enabled: !s.enabled, status: !s.enabled ? 'connected' : 'disconnected' } : s
    ));
  };

  const filtered = filter === 'all' ? sources : sources.filter(s => s.type === filter);
  const connectedCount = sources.filter(s => s.status === 'connected').length;
  const types = [...new Set(sources.map(s => s.type))];

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>🔌 数据源配置</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>管理监控、日志、指标数据源接入</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <span style={{ padding: '6px 12px', borderRadius: 8, background: 'rgba(16,185,129,0.12)', color: '#10b981', fontSize: 12, fontWeight: 600 }}>
            ✅ {connectedCount} 已连接
          </span>
          <span style={{ padding: '6px 12px', borderRadius: 8, background: 'rgba(239,68,68,0.12)', color: '#ef4444', fontSize: 12, fontWeight: 600 }}>
            ⚠️ {sources.length - connectedCount} 未连接
          </span>
        </div>
      </div>

      {/* Type Filter */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 20, background: '#111827', borderRadius: 10, padding: 4, width: 'fit-content' }}>
        {['all', ...types].map(t => (
          <button key={t} onClick={() => setFilter(t)} style={{ padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: 600, background: filter === t ? 'rgba(59,130,246,0.2)' : 'transparent', color: filter === t ? '#3b82f6' : '#94a3b8' }}>
            {t === 'all' ? '全部' : `${typeIcons[t] || '📦'} ${t}`}
          </button>
        ))}
      </div>

      {/* Data Sources */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
        {filtered.map(src => (
          <div key={src.id} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, opacity: src.enabled ? 1 : 0.6 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ width: 44, height: 44, borderRadius: 10, background: `${typeColors[src.type] || '#3b82f6'}20`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 20 }}>
                  {typeIcons[src.type] || '📦'}
                </div>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 600, color: '#e2e8f0' }}>{src.name}</div>
                  <div style={{ fontSize: 11, color: '#64748b', fontFamily: 'monospace' }}>{src.endpoint}</div>
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ padding: '3px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: src.status === 'connected' ? 'rgba(16,185,129,0.12)' : 'rgba(239,68,68,0.12)', color: src.status === 'connected' ? '#10b981' : '#ef4444' }}>
                  {src.status === 'connected' ? '● 已连接' : '○ 未连接'}
                </span>
              </div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: 12, borderTop: '1px solid rgba(255,255,255,0.04)' }}>
              <div style={{ display: 'flex', gap: 12, fontSize: 11, color: '#94a3b8' }}>
                <span>认证: {src.auth_type}</span>
                <span>更新: {src.last_check}</span>
                {src.metrics_count !== undefined && <span>指标: {src.metrics_count}</span>}
              </div>
              <button onClick={() => toggleSource(src.id)} style={{ padding: '4px 12px', borderRadius: 6, border: `1px solid ${src.enabled ? '#10b981' : '#ef4444'}40`, background: src.enabled ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)', color: src.enabled ? '#10b981' : '#ef4444', cursor: 'pointer', fontSize: 11, fontWeight: 600 }}>
                {src.enabled ? '已启用' : '已禁用'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Add Source Button */}
      <div style={{ marginTop: 20, textAlign: 'center' }}>
        <button style={{ padding: '10px 24px', borderRadius: 8, border: '1px dashed #3b82f6', background: 'rgba(59,130,246,0.05)', color: '#3b82f6', cursor: 'pointer', fontSize: 13, fontWeight: 600 }}>
          + 添加数据源
        </button>
      </div>
    </div>
  );
}
