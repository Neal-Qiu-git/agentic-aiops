import { useState, useEffect, useCallback } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { fetchApi, type SecurityData, demoSecurityData } from '../api';

const severityColors: Record<string, string> = {
  critical: '#ef4444', high: '#f59e0b', medium: '#3b82f6', low: '#6b7280',
};

export default function SecurityPage() {
  const [securityData, setSecurityData] = useState<SecurityData[]>(demoSecurityData);
  const [mode, setMode] = useState<'live' | 'demo'>('demo');

  const refresh = useCallback(async () => {
    const { data, mode: m } = await fetchApi<SecurityData[]>('/api/v1/security/summary', demoSecurityData);
    setSecurityData(data);
    setMode(m);
  }, []);

  useEffect(() => { refresh(); }, [refresh]);
  useEffect(() => { const t = setInterval(refresh, 60000); return () => clearInterval(t); }, [refresh]);

  // 汇总统计
  const allItems = securityData.flatMap(s => s.items);
  const totalCritical = securityData.reduce((a, s) => a + s.critical, 0);
  const totalHigh = securityData.reduce((a, s) => a + s.high, 0);
  const totalMedium = securityData.reduce((a, s) => a + s.medium, 0);
  const totalLow = securityData.reduce((a, s) => a + s.low, 0);
  const totalOpen = allItems.filter(i => i.status === 'open').length;
  const totalMitigated = allItems.filter(i => i.status !== 'open').length;

  const pieData = [
    { name: '严重', value: totalCritical, color: '#ef4444' },
    { name: '高危', value: totalHigh, color: '#f59e0b' },
    { name: '中危', value: totalMedium, color: '#3b82f6' },
    { name: '低危', value: totalLow, color: '#6b7280' },
  ].filter(d => d.value > 0);

  // 合规评分
  const complianceFrameworks = [
    { framework: 'CIS Kubernetes', score: 92, passed: 46, failed: 4, total: 50, lastScan: '2h ago' },
    { framework: '等保 2.0 三级', score: 88, passed: 22, failed: 3, total: 25, lastScan: '4h ago' },
    { framework: 'PCI-DSS', score: 95, passed: 19, failed: 1, total: 20, lastScan: '1d ago' },
    { framework: 'SOC 2', score: 90, passed: 18, failed: 2, total: 20, lastScan: '1d ago' },
  ];
  const avgCompliance = Math.round(complianceFrameworks.reduce((a, c) => a + c.score, 0) / complianceFrameworks.length);

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">🔒 安全态势</h1>
          <p className="page-subtitle">漏洞扫描 · 合规检查 · 配置审计 · 实时数据</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ fontSize: 11, padding: '3px 10px', borderRadius: 8,
            background: mode === 'live' ? 'rgba(16,185,129,0.15)' : 'rgba(245,158,11,0.15)',
            color: mode === 'live' ? '#10b981' : '#f59e0b' }}>
            {mode === 'live' ? '🟢 实时' : '🟡 Demo'}
          </span>
          <span className={`badge ${avgCompliance >= 90 ? 'badge-green' : 'badge-yellow'}`}>合规 {avgCompliance}%</span>
        </div>
      </div>

      {/* 统计卡片 */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(239,68,68,0.15)'}}>🐛</div>
          <div>
            <div className="stat-value" style={{color:'var(--accent-red)'}}>{totalCritical}</div>
            <div className="stat-label">严重漏洞</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(245,158,11,0.15)'}}>⚠️</div>
          <div>
            <div className="stat-value" style={{color:'var(--accent-yellow)'}}>{totalHigh}</div>
            <div className="stat-label">高危漏洞</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-green)'}}>✅</div>
          <div>
            <div className="stat-value">{avgCompliance}%</div>
            <div className="stat-label">合规评分</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-blue)'}}>🔍</div>
          <div>
            <div className="stat-value">{totalOpen}</div>
            <div className="stat-label">待修复</div>
          </div>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 16 }}>
        {/* 漏洞分布饼图 */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">漏洞分布</span>
            <span className="badge badge-red">{totalOpen} 待修复</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
            <div style={{ width: 150, height: 150 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" innerRadius={35} outerRadius={60} dataKey="value">
                    {pieData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {pieData.map(d => (
                <div key={d.name} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12 }}>
                  <div style={{ width: 10, height: 10, borderRadius: 3, background: d.color }} />
                  <span style={{ color: 'var(--text-secondary)' }}>{d.name}</span>
                  <span style={{ fontWeight: 700, color: d.color }}>{d.value}</span>
                </div>
              ))}
              <div style={{ marginTop: 4, fontSize: 11, color: 'var(--text-muted)' }}>
                已修复: {totalMitigated}
              </div>
            </div>
          </div>
        </div>

        {/* 合规框架 */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">合规框架</span>
            <span className="badge badge-green">{complianceFrameworks.length} 个</span>
          </div>
          {complianceFrameworks.map((c, i) => (
            <div key={i} style={{ padding: '10px 0', borderBottom: i < complianceFrameworks.length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                <span style={{ fontSize: 13, fontWeight: 600 }}>{c.framework}</span>
                <span style={{ fontSize: 13, fontWeight: 700, color: c.score >= 90 ? 'var(--accent-green)' : 'var(--accent-yellow)' }}>{c.score}%</span>
              </div>
              <div style={{ display: 'flex', gap: 8, fontSize: 11, color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-green)' }}>✅ {c.passed}</span>
                <span style={{ color: 'var(--accent-red)' }}>❌ {c.failed}</span>
                <span>⏱️ {c.lastScan}</span>
              </div>
              <div style={{ height: 4, background: 'rgba(255,255,255,0.06)', borderRadius: 2, marginTop: 6 }}>
                <div style={{ height: '100%', width: `${c.score}%`, background: c.score >= 90 ? 'var(--accent-green)' : 'var(--accent-yellow)', borderRadius: 2 }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 漏洞详情列表 */}
      <div className="card">
        <div className="card-header">
          <span className="card-title">漏洞详情</span>
          <span className="badge badge-blue">{securityData.length} 个分类</span>
        </div>
        {securityData.map((category, ci) => (
          <div key={ci} style={{ marginBottom: ci < securityData.length - 1 ? 16 : 0 }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
              <span>{category.category}</span>
              <span style={{ fontSize: 10, padding: '2px 6px', borderRadius: 4, background: 'rgba(255,255,255,0.05)' }}>
                {category.items.length} 项
              </span>
            </div>
            {category.items.map((item, ii) => (
              <div key={ii} style={{
                display: 'flex', alignItems: 'center', gap: 12,
                padding: '10px 0',
                borderBottom: ii < category.items.length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none',
              }}>
                <div style={{
                  width: 8, height: 8, borderRadius: '50%', flexShrink: 0,
                  background: severityColors[item.severity] || '#6b7280',
                }} />
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
                    <span style={{ fontSize: 12, fontWeight: 600, fontFamily: item.name.startsWith('CVE') ? 'monospace' : 'inherit' }}>{item.name}</span>
                    <span style={{
                      fontSize: 10, padding: '2px 8px', borderRadius: 4,
                      background: `${severityColors[item.severity] || '#6b7280'}15`,
                      color: severityColors[item.severity] || '#6b7280',
                    }}>
                      {item.severity}
                    </span>
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{item.description}</div>
                </div>
                <span style={{
                  fontSize: 10, padding: '2px 8px', borderRadius: 4,
                  background: item.status === 'open' ? 'rgba(239,68,68,0.1)' : 'rgba(16,185,129,0.1)',
                  color: item.status === 'open' ? '#ef4444' : '#10b981',
                }}>
                  {item.status === 'open' ? '待修复' : '已处理'}
                </span>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
