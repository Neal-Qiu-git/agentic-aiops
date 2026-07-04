import { useState, useEffect } from 'react';

interface DataSource {
  id: string; name: string; type: string; endpoint: string;
  auth_type: string; enabled: boolean; status: string;
  last_check: string; metrics_count?: number;
}

const STORAGE_KEY = 'aiops-datasources';

const defaults: DataSource[] = [
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
  loki: '📋', redis: '🗄️', mysql: '🐬', postgres: '🐘', zookeeper: '🦁', kafka: '📨',
};
const typeColors: Record<string, string> = {
  prometheus: '#e6522c', grafana: '#f46800', kubernetes: '#326ce5', elasticsearch: '#005571',
  loki: '#f56e00', redis: '#dc382d', mysql: '#00758f', postgres: '#336791', zookeeper: '#5B7F3B', kafka: '#231F20',
};

const emptyForm: Partial<DataSource> = { name: '', type: 'prometheus', endpoint: '', auth_type: 'none', enabled: true };

export default function DataSourcePage() {
  const [sources, setSources] = useState<DataSource[]>(() => {
    try { const s = localStorage.getItem(STORAGE_KEY); return s ? JSON.parse(s) : defaults; } catch { return defaults; }
  });
  const [filter, setFilter] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<DataSource | null>(null);
  const [form, setForm] = useState<Partial<DataSource>>(emptyForm);
  const [testing, setTesting] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<{ id: string; ok: boolean; msg: string } | null>(null);
  const [confirmDelete, setConfirmDelete] = useState<string | null>(null);

  useEffect(() => { localStorage.setItem(STORAGE_KEY, JSON.stringify(sources)); }, [sources]);

  const connectedCount = sources.filter(s => s.status === 'connected').length;
  const types = [...new Set(sources.map(s => s.type))];
  const filtered = filter === 'all' ? sources : sources.filter(s => s.type === filter);

  const openAdd = () => { setEditing(null); setForm(emptyForm); setShowModal(true); };
  const openEdit = (src: DataSource, e: React.MouseEvent) => {
    e.stopPropagation(); setEditing(src); setForm({ ...src }); setShowModal(true);
  };
  const saveForm = () => {
    if (!form.name || !form.endpoint) return;
    if (editing) {
      setSources(prev => prev.map(s => s.id === editing.id ? { ...s, ...form } as DataSource : s));
    } else {
      const newSrc: DataSource = { ...emptyForm, ...form, id: `ds-${Date.now()}`, status: 'disconnected', last_check: '刚刚添加', metrics_count: 0 } as DataSource;
      setSources(prev => [...prev, newSrc]);
    }
    setShowModal(false);
  };
  const deleteSource = (id: string, e: React.MouseEvent) => {
    e.stopPropagation(); setConfirmDelete(id);
  };
  const confirmDel = () => {
    if (confirmDelete) setSources(prev => prev.filter(s => s.id !== confirmDelete));
    setConfirmDelete(null);
  };
  const toggleSource = (id: string) => {
    setSources(prev => prev.map(s => s.id === id ? { ...s, enabled: !s.enabled, status: !s.enabled ? 'connected' : 'disconnected', last_check: '刚刚切换' } : s));
  };
  const testConnection = (src: DataSource, e: React.MouseEvent) => {
    e.stopPropagation(); setTesting(src.id); setTestResult(null);
    setTimeout(() => {
      const ok = src.endpoint.startsWith('http') || src.endpoint.startsWith('redis://');
      setTestResult({ id: src.id, ok, msg: ok ? '连接成功' : '连接失败：无效的 URL 协议' });
      setTesting(null);
    }, 1500);
  };

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>🔌 数据源配置</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>管理监控、日志、指标数据源接入</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ padding: '6px 12px', borderRadius: 8, background: 'rgba(16,185,129,0.12)', color: '#10b981', fontSize: 12, fontWeight: 600 }}>✅ {connectedCount} 已连接</span>
          <span style={{ padding: '6px 12px', borderRadius: 8, background: 'rgba(239,68,68,0.12)', color: '#ef4444', fontSize: 12, fontWeight: 600 }}>⚠️ {sources.length - connectedCount} 未连接</span>
        </div>
      </div>

      {/* Filter */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 20, background: '#111827', borderRadius: 10, padding: 4, width: 'fit-content' }}>
        <button onClick={() => setFilter('all')} style={{ padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: 600, background: filter === 'all' ? 'rgba(59,130,246,0.2)' : 'transparent', color: filter === 'all' ? '#3b82f6' : '#94a3b8' }}>
          全部 ({sources.length})
        </button>
        {types.map(t => (
          <button key={t} onClick={() => setFilter(t)} style={{ padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: 600, background: filter === t ? 'rgba(59,130,246,0.2)' : 'transparent', color: filter === t ? '#3b82f6' : '#94a3b8' }}>
            {typeIcons[t] || '📦'} {t}
          </button>
        ))}
      </div>

      {/* Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
        {filtered.map(src => (
          <div key={src.id} onClick={() => toggleSource(src.id)} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 20, opacity: src.enabled ? 1 : 0.6, cursor: 'pointer', transition: 'border-color 0.2s' }}>
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
                {testResult && testResult.id === src.id && (
                  <span style={{ fontSize: 10, color: testResult.ok ? '#10b981' : '#ef4444', fontWeight: 600 }}>{testResult.msg}</span>
                )}
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
              <div style={{ display: 'flex', gap: 6 }}>
                <button onClick={(e) => testConnection(src, e)} disabled={testing === src.id} style={{ padding: '4px 10px', borderRadius: 6, border: '1px solid rgba(59,130,246,0.3)', background: 'rgba(59,130,246,0.1)', color: '#3b82f6', cursor: 'pointer', fontSize: 10, fontWeight: 600, opacity: testing === src.id ? 0.5 : 1 }}>
                  {testing === src.id ? '⏳ 测试中...' : '🔗 测试'}
                </button>
                <button onClick={(e) => openEdit(src, e)} style={{ padding: '4px 10px', borderRadius: 6, border: '1px solid rgba(139,92,246,0.3)', background: 'rgba(139,92,246,0.1)', color: '#8b5cf6', cursor: 'pointer', fontSize: 10, fontWeight: 600 }}>
                  ✏️ 编辑
                </button>
                <button onClick={(e) => deleteSource(src.id, e)} style={{ padding: '4px 10px', borderRadius: 6, border: '1px solid rgba(239,68,68,0.3)', background: 'rgba(239,68,68,0.1)', color: '#ef4444', cursor: 'pointer', fontSize: 10, fontWeight: 600 }}>
                  🗑️
                </button>
                <button onClick={(e) => { e.stopPropagation(); toggleSource(src.id); }} style={{ padding: '4px 10px', borderRadius: 6, border: `1px solid ${src.enabled ? '#10b981' : '#ef4444'}40`, background: src.enabled ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)', color: src.enabled ? '#10b981' : '#ef4444', cursor: 'pointer', fontSize: 10, fontWeight: 600 }}>
                  {src.enabled ? '已启用' : '已禁用'}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add Button */}
      <div style={{ marginTop: 20, textAlign: 'center' }}>
        <button onClick={openAdd} style={{ padding: '10px 24px', borderRadius: 8, border: '1px dashed #3b82f6', background: 'rgba(59,130,246,0.05)', color: '#3b82f6', cursor: 'pointer', fontSize: 13, fontWeight: 600 }}>
          + 添加数据源
        </button>
      </div>

      {/* Add/Edit Modal */}
      {showModal && (
        <div onClick={() => setShowModal(false)} style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }}>
          <div onClick={e => e.stopPropagation()} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 16, padding: 28, width: 480, maxHeight: '80vh', overflow: 'auto' }}>
            <h3 style={{ fontSize: 18, fontWeight: 700, color: '#e2e8f0', marginBottom: 20 }}>{editing ? '✏️ 编辑数据源' : '➕ 添加数据源'}</h3>

            {/* Name */}
            <div style={{ marginBottom: 14 }}>
              <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 6 }}>名称 *</label>
              <input value={form.name || ''} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} placeholder="例如：Prometheus 主集群" style={{ width: '100%', padding: '10px 14px', borderRadius: 8, border: '1px solid #2a3050', background: '#0f1629', color: '#e2e8f0', fontSize: 13, boxSizing: 'border-box' }} />
            </div>

            {/* Type */}
            <div style={{ marginBottom: 14 }}>
              <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 6 }}>类型</label>
              <select value={form.type || 'prometheus'} onChange={e => setForm(f => ({ ...f, type: e.target.value }))} style={{ width: '100%', padding: '10px 14px', borderRadius: 8, border: '1px solid #2a3050', background: '#0f1629', color: '#e2e8f0', fontSize: 13 }}>
                {Object.keys(typeIcons).map(t => <option key={t} value={t}>{typeIcons[t]} {t}</option>)}
              </select>
            </div>

            {/* Endpoint */}
            <div style={{ marginBottom: 14 }}>
              <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 6 }}>连接地址 *</label>
              <input value={form.endpoint || ''} onChange={e => setForm(f => ({ ...f, endpoint: e.target.value }))} placeholder="http://prometheus:9090" style={{ width: '100%', padding: '10px 14px', borderRadius: 8, border: '1px solid #2a3050', background: '#0f1629', color: '#e2e8f0', fontSize: 13, fontFamily: 'monospace', boxSizing: 'border-box' }} />
            </div>

            {/* Auth */}
            <div style={{ marginBottom: 14 }}>
              <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 6 }}>认证方式</label>
              <select value={form.auth_type || 'none'} onChange={e => setForm(f => ({ ...f, auth_type: e.target.value }))} style={{ width: '100%', padding: '10px 14px', borderRadius: 8, border: '1px solid #2a3050', background: '#0f1629', color: '#e2e8f0', fontSize: 13 }}>
                <option value="none">无认证</option>
                <option value="token">Token</option>
                <option value="tls">TLS 证书</option>
                <option value="basic">Basic Auth</option>
              </select>
            </div>

            {/* Buttons */}
            <div style={{ display: 'flex', gap: 10, marginTop: 20 }}>
              <button onClick={() => setShowModal(false)} style={{ flex: 1, padding: '10px 0', borderRadius: 8, border: '1px solid #2a3050', background: 'transparent', color: '#94a3b8', cursor: 'pointer', fontSize: 13 }}>取消</button>
              <button onClick={saveForm} disabled={!form.name || !form.endpoint} style={{ flex: 1, padding: '10px 0', borderRadius: 8, border: 'none', background: form.name && form.endpoint ? '#3b82f6' : '#374151', color: 'white', cursor: form.name && form.endpoint ? 'pointer' : 'not-allowed', fontSize: 13, fontWeight: 600 }}>
                {editing ? '💾 保存修改' : '➕ 添加'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirm */}
      {confirmDelete && (
        <div onClick={() => setConfirmDelete(null)} style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }}>
          <div onClick={e => e.stopPropagation()} style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 16, padding: 28, width: 400 }}>
            <h3 style={{ fontSize: 16, fontWeight: 700, color: '#ef4444', marginBottom: 12 }}>🗑️ 确认删除</h3>
            <p style={{ fontSize: 13, color: '#94a3b8', marginBottom: 20 }}>确定要删除数据源 <strong style={{ color: '#e2e8f0' }}>{sources.find(s => s.id === confirmDelete)?.name}</strong> 吗？此操作不可撤销。</p>
            <div style={{ display: 'flex', gap: 10 }}>
              <button onClick={() => setConfirmDelete(null)} style={{ flex: 1, padding: '10px 0', borderRadius: 8, border: '1px solid #2a3050', background: 'transparent', color: '#94a3b8', cursor: 'pointer', fontSize: 13 }}>取消</button>
              <button onClick={confirmDel} style={{ flex: 1, padding: '10px 0', borderRadius: 8, border: 'none', background: '#ef4444', color: 'white', cursor: 'pointer', fontSize: 13, fontWeight: 600 }}>确认删除</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
