import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { agents, systemHealth, events } from '../data/agents';
import { fetchApi, type PlatformOverview, type AlertData, demoPlatformOverview, demoAlerts } from '../api';

// ══════════════════════════════════════════
// 仪表盘 — 平台介绍 + 操作指引 + 实时状态
// 企业实际使用场景：一页看清全局
// ══════════════════════════════════════════

export default function DashboardPage() {
  const navigate = useNavigate();
  const [overview, setOverview] = useState<PlatformOverview>(demoPlatformOverview);
  const [alerts, setAlerts] = useState<AlertData>(demoAlerts);
  const [mode, setMode] = useState<'live' | 'demo'>('demo');
  const [lastUpdate, setLastUpdate] = useState(Date.now());

  const refresh = useCallback(async () => {
    const [ov, al] = await Promise.all([
      fetchApi<PlatformOverview>('/api/v1/monitoring/summary', demoPlatformOverview),
      fetchApi<AlertData>('/api/v1/monitoring/alerts', demoAlerts),
    ]);
    setOverview(ov.data);
    setAlerts(al.data);
    setMode(ov.mode);
    setLastUpdate(Date.now());
  }, []);

  useEffect(() => { refresh(); }, [refresh]);
  useEffect(() => {
    const t = setInterval(refresh, 15000);
    return () => clearInterval(t);
  }, [refresh]);

  const sys = overview.system;
  const res = overview.resources;
  const evt = overview.events_today;
  const cost = overview.cost;

  return (
    <div className="animate-fade-in">
      {/* ═══ 顶部状态栏 ═══ */}
      <div className="page-header">
        <div>
          <h1 className="page-title">🤖 Agentic AIOps</h1>
          <p className="page-subtitle">AI原生智能运维平台 · 企业级全场景覆盖</p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{
            fontSize: 11, padding: '3px 10px', borderRadius: 8,
            background: mode === 'live' ? 'rgba(16,185,129,0.15)' : 'rgba(245,158,11,0.15)',
            color: mode === 'live' ? '#10b981' : '#f59e0b',
          }}>
            {mode === 'live' ? '🟢 实时数据' : '🟡 Demo 演示'}
          </span>
          <span className="badge badge-green">● {sys.status === 'healthy' ? '系统正常' : sys.status}</span>
          <span className="badge badge-blue">运行 {sys.uptime}</span>
        </div>
      </div>

      {/* ═══ 平台介绍区 ═══ */}
      <div className="card" style={{
        padding: '24px 28px', marginBottom: 20,
        background: 'linear-gradient(135deg, rgba(59,130,246,0.06), rgba(139,92,246,0.06))',
        border: '1px solid rgba(59,130,246,0.15)',
      }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 24 }}>
          {/* 是什么 */}
          <div>
            <div style={{ fontSize: 14, fontWeight: 700, color: '#3b82f6', marginBottom: 8 }}>🎯 是什么</div>
            <div style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.7 }}>
              Agentic AIOps 是一个<strong style={{ color: 'var(--text-primary)' }}>AI 驱动的智能运维平台</strong>，
              通过 21 个专业 Agent 和 148 个 MCP 工具，自动完成监控、告警、部署、安全、成本优化等运维工作。
            </div>
            <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 6 }}>
              支持：Linux / Windows / K8s / Docker / 多云 / 混合云 / 信创
            </div>
          </div>

          {/* 能做什么 */}
          <div>
            <div style={{ fontSize: 14, fontWeight: 700, color: '#8b5cf6', marginBottom: 8 }}>⚡ 能做什么</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4, fontSize: 12, color: 'var(--text-secondary)' }}>
              <span>🔍 <strong style={{ color: 'var(--text-primary)' }}>环境发现</strong> — 自动探测服务器，推荐 Agent</span>
              <span>📊 <strong style={{ color: 'var(--text-primary)' }}>实时监控</strong> — CPU/内存/磁盘，Prometheus 接入</span>
              <span>🚨 <strong style={{ color: 'var(--text-primary)' }}>智能告警</strong> — 分级、关联、修复建议</span>
              <span>🚀 <strong style={{ color: 'var(--text-primary)' }}>自动部署</strong> — K8s 滚动更新、灰度、回滚</span>
              <span>🔒 <strong style={{ color: 'var(--text-primary)' }}>安全合规</strong> — 漏洞扫描、等保检查</span>
              <span>💰 <strong style={{ color: 'var(--text-primary)' }}>成本优化</strong> — 多云费用分析、优化建议</span>
            </div>
          </div>

          {/* 怎么接入 */}
          <div>
            <div style={{ fontSize: 14, fontWeight: 700, color: '#10b981', marginBottom: 8 }}>🚀 快速开始</div>
            <div style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.8 }}>
              <div><span style={{ display: 'inline-block', width: 20, height: 20, borderRadius: '50%', background: 'rgba(16,185,129,0.15)', color: '#10b981', textAlign: 'center', lineHeight: '20px', fontSize: 11, fontWeight: 700, marginRight: 6 }}>1</span>安装 agentic-aiops</div>
              <div><span style={{ display: 'inline-block', width: 20, height: 20, borderRadius: '50%', background: 'rgba(16,185,129,0.15)', color: '#10b981', textAlign: 'center', lineHeight: '20px', fontSize: 11, fontWeight: 700, marginRight: 6 }}>2</span>运行 <code style={{ background: 'rgba(255,255,255,0.08)', padding: '1px 6px', borderRadius: 4, fontSize: 11 }}>aiops discover</code></div>
              <div><span style={{ display: 'inline-block', width: 20, height: 20, borderRadius: '50%', background: 'rgba(16,185,129,0.15)', color: '#10b981', textAlign: 'center', lineHeight: '20px', fontSize: 11, fontWeight: 700, marginRight: 6 }}>3</span>配置数据源（Prometheus/K8s）</div>
              <div><span style={{ display: 'inline-block', width: 20, height: 20, borderRadius: '50%', background: 'rgba(16,185,129,0.15)', color: '#10b981', textAlign: 'center', lineHeight: '20px', fontSize: 11, fontWeight: 700, marginRight: 6 }}>4</span>启动 <code style={{ background: 'rgba(255,255,255,0.08)', padding: '1px 6px', borderRadius: 4, fontSize: 11 }}>aiops serve</code></div>
            </div>
            <button onClick={() => navigate('/environments')} style={{
              marginTop: 8, padding: '6px 14px', borderRadius: 6, border: 'none',
              background: 'rgba(16,185,129,0.15)', color: '#10b981',
              cursor: 'pointer', fontSize: 11, fontWeight: 600,
            }}>
              🔍 开始环境探测 →
            </button>
          </div>
        </div>
      </div>

      {/* ═══ 核心指标 ═══ */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-blue)'}}>🤖</div>
          <div>
            <div className="stat-value">{sys.agents_active}/{sys.agents_total}</div>
            <div className="stat-label">活跃智能体</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-purple)'}}>🔌</div>
          <div>
            <div className="stat-value">{sys.tools_total}</div>
            <div className="stat-label">MCP 工具</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-green)'}}>⚡</div>
          <div>
            <div className="stat-value">{sys.tasks_today}</div>
            <div className="stat-label">今日任务</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(245,158,11,0.15)'}}>✅</div>
          <div>
            <div className="stat-value">{sys.success_rate}%</div>
            <div className="stat-label">成功率</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(239,68,68,0.15)'}}>🚨</div>
          <div>
            <div className="stat-value" style={{ color: evt.critical > 0 ? '#ef4444' : undefined }}>{alerts.summary.firing}</div>
            <div className="stat-label">活跃告警</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(245,158,11,0.15)'}}>💰</div>
          <div>
            <div className="stat-value">¥{(cost.monthly_total / 10000).toFixed(1)}万</div>
            <div className="stat-label">月度费用</div>
          </div>
        </div>
      </div>

      {/* ═══ 双列：资源概览 + 告警快览 ═══ */}
      <div className="grid-2">
        {/* 资源概览 */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">📊 资源概览</span>
            <span className="badge badge-blue">{res.servers + res.vms + res.containers} 实例</span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
            {[
              { icon: '🖥️', label: '物理服务器', value: res.servers, color: '#8b5cf6' },
              { icon: '💻', label: '虚拟机', value: res.vms, color: '#3b82f6' },
              { icon: '🐳', label: '容器', value: res.containers, color: '#0ea5e9' },
              { icon: '☸️', label: 'K8s 集群', value: res.k8s_clusters, color: '#8b5cf6' },
              { icon: '🗄️', label: '数据库', value: res.databases, color: '#10b981' },
              { icon: '🌐', label: '网络设备', value: res.network_devices, color: '#f97316' },
            ].map(item => (
              <div key={item.label} style={{
                display: 'flex', alignItems: 'center', gap: 10,
                padding: '10px 12px', borderRadius: 8,
                background: 'rgba(255,255,255,0.02)',
              }}>
                <span style={{ fontSize: 20 }}>{item.icon}</span>
                <div>
                  <div style={{ fontSize: 16, fontWeight: 700, color: item.color }}>{item.value}</div>
                  <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>{item.label}</div>
                </div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 12, textAlign: 'right' }}>
            <button onClick={() => navigate('/environments')} style={{
              padding: '4px 12px', borderRadius: 6, border: '1px solid var(--border)',
              background: 'transparent', color: 'var(--accent-blue)', cursor: 'pointer', fontSize: 11,
            }}>
              查看环境详情 →
            </button>
          </div>
        </div>

        {/* 告警快览 */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">🚨 告警快览</span>
            <button onClick={() => navigate('/alerts')} style={{
              fontSize: 12, color: 'var(--accent-blue)', background: 'none',
              border: 'none', cursor: 'pointer',
            }}>
              查看全部 →
            </button>
          </div>
          <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
            {[
              { label: 'Critical', count: alerts.summary.by_severity.critical, color: '#ef4444' },
              { label: 'Warning', count: alerts.summary.by_severity.warning, color: '#f59e0b' },
              { label: 'Info', count: alerts.summary.by_severity.info, color: '#3b82f6' },
            ].map(s => (
              <div key={s.label} style={{
                flex: 1, padding: '8px 10px', borderRadius: 6,
                background: `${s.color}10`, border: `1px solid ${s.color}25`, textAlign: 'center',
              }}>
                <div style={{ fontSize: 18, fontWeight: 700, color: s.color }}>{s.count}</div>
                <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>{s.label}</div>
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {alerts.alerts.filter(a => a.state === 'firing').slice(0, 4).map((alert, i) => (
              <div key={i} style={{
                display: 'flex', alignItems: 'center', gap: 10,
                padding: '8px 10px', borderRadius: 6,
                background: alert.severity === 'critical' ? 'rgba(239,68,68,0.06)' : 'rgba(255,255,255,0.02)',
              }}>
                <div style={{
                  width: 8, height: 8, borderRadius: '50%', flexShrink: 0,
                  background: alert.severity === 'critical' ? '#ef4444' : alert.severity === 'warning' ? '#f59e0b' : '#3b82f6',
                }} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 12, fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {alert.name}
                  </div>
                  <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>{alert.description}</div>
                </div>
                <span style={{ fontSize: 10, color: 'var(--text-muted)', flexShrink: 0 }}>{alert.started_at}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ═══ 快速入口 ═══ */}
      <div style={{ marginTop: 16 }}>
        <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 10 }}>⚡ 快速入口</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 10 }}>
          {[
            { icon: '🔍', label: '环境发现', path: '/environments', color: '#3b82f6', desc: '探测环境' },
            { icon: '📊', label: '实时监控', path: '/monitoring', color: '#10b981', desc: '系统指标' },
            { icon: '🚨', label: '告警中心', path: '/alerts', color: '#ef4444', desc: '告警处理' },
            { icon: '🚀', label: '部署管理', path: '/deployment', color: '#8b5cf6', desc: 'K8s 部署' },
            { icon: '💰', label: '成本分析', path: '/cost', color: '#f59e0b', desc: '费用优化' },
            { icon: '🔒', label: '安全态势', path: '/security', color: '#ec4899', desc: '漏洞扫描' },
          ].map(item => (
            <button key={item.path} onClick={() => navigate(item.path)} style={{
              padding: '16px 12px', borderRadius: 10, border: `1px solid ${item.color}25`,
              background: `${item.color}08`, cursor: 'pointer', textAlign: 'center',
              transition: 'all 0.15s',
            }}
            onMouseEnter={e => { (e.target as HTMLElement).style.background = `${item.color}15`; }}
            onMouseLeave={e => { (e.target as HTMLElement).style.background = `${item.color}08`; }}
            >
              <div style={{ fontSize: 24, marginBottom: 4 }}>{item.icon}</div>
              <div style={{ fontSize: 12, fontWeight: 600, color: item.color }}>{item.label}</div>
              <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 2 }}>{item.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* ═══ 系统健康度 ═══ */}
      <div className="card" style={{ marginTop: 16 }}>
        <div className="card-header">
          <span className="card-title">🏥 系统健康度</span>
          <span className="badge badge-green">95.2 分</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
          {[
            { label: '可用性', value: '99.97%', status: 'ok', color: '#10b981', desc: '过去30天' },
            { label: '平均响应', value: '1.2s', status: 'ok', color: '#10b981', desc: 'API P95' },
            { label: 'MTTR', value: '4m 23s', status: 'ok', color: '#10b981', desc: '平均恢复时间' },
            { label: '错误预算', value: '95%', status: 'ok', color: '#10b981', desc: '剩余可用' },
          ].map((item, i) => (
            <div key={i} style={{ padding: '12px 16px', borderRadius: 8, background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.04)' }}>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>{item.label}</div>
              <div style={{ fontSize: 20, fontWeight: 700, color: item.color }}>{item.value}</div>
              <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 2 }}>{item.desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* ═══ 最近部署 ═══ */}
      <div className="card" style={{ marginTop: 16 }}>
        <div className="card-header">
          <span className="card-title">🚀 最近部署</span>
          <a href="#/deployment" style={{ fontSize: 12, color: 'var(--accent-blue)', textDecoration: 'none' }}>查看全部 →</a>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
          {[
            { name: 'nginx-frontend', version: 'v2.3.2', status: 'success', time: '10分钟前', env: 'production' },
            { name: 'api-gateway', version: 'v2.3.1', status: 'success', time: '2小时前', env: 'staging' },
            { name: 'user-service', version: 'v1.8.0', status: 'failed', time: '4小时前', env: 'production' },
          ].map((d, i) => (
            <div key={i} style={{ padding: '12px 16px', borderRadius: 8, background: 'rgba(255,255,255,0.02)', borderLeft: `3px solid ${d.status === 'success' ? '#10b981' : '#ef4444'}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>{d.name}</span>
                <span style={{ padding: '2px 6px', borderRadius: 4, fontSize: 10, background: `${d.status === 'success' ? '#10b981' : '#ef4444'}20`, color: d.status === 'success' ? '#10b981' : '#ef4444' }}>
                  {d.status === 'success' ? '✅ 成功' : '❌ 失败'}
                </span>
              </div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                {d.version} · {d.env} · {d.time}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ═══ 最近事件 ═══ */}
      <div className="card" style={{ marginTop: 16 }}>
        <div className="card-header">
          <span className="card-title">📡 最近事件</span>
          <a href="#/events" style={{ fontSize: 12, color: 'var(--accent-blue)', textDecoration: 'none' }}>查看全部 →</a>
        </div>
        {events.slice(0, 5).map((e: any, i) => (
          <div key={i} className="event-item">
            <span className="event-time">{e.time}</span>
            <div className="event-dot" style={{ background: e.type === 'error' ? 'var(--accent-red)' : e.type === 'warning' ? 'var(--accent-yellow)' : e.type === 'info' ? 'var(--accent-blue)' : 'var(--accent-green)' }} />
            <div className="event-content">
              <div className="event-title">{e.title}</div>
              <div className="event-desc">{e.desc}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
