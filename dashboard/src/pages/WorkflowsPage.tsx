import { useState } from 'react';
import { workflowTemplates, agents, type Workflow } from '../data/agents';

// ── 常量 ──
const categoryLabels: Record<string, { label: string; icon: string; color: string }> = {
  incident:  { label: '故障应急', icon: '🚨', color: '#ef4444' },
  deploy:    { label: '发布部署', icon: '🚀', color: '#3b82f6' },
  optimize:  { label: '性能优化', icon: '⚡', color: '#10b981' },
  security:  { label: '安全响应', icon: '🔒', color: '#f97316' },
  compliance:{ label: '合规审计', icon: '📋', color: '#8b5cf6' },
  provision: { label: '资源编排', icon: '🏗️', color: '#06b6d4' },
};

const triggerLabels: Record<string, string> = {
  alert: '🔔 告警触发', schedule: '⏰ 定时调度', manual: '👤 手动触发',
  webhook: '🔗 Webhook', api: '📡 API 调用',
};

const priorityColors: Record<string, string> = {
  P0: '#ef4444', P1: '#f97316', P2: '#eab308', P3: '#6b7280',
};

const statusConfig: Record<string, { icon: string; label: string; color: string }> = {
  completed: { icon: '✅', label: '已完成', color: '#10b981' },
  running:   { icon: '🔄', label: '执行中', color: '#3b82f6' },
  pending:   { icon: '⏳', label: '待执行', color: '#6b7280' },
  error:     { icon: '❌', label: '失败',   color: '#ef4444' },
};

const stepStatusConfig: Record<string, { icon: string; color: string; bg: string; border: string }> = {
  completed: { icon: '✅', color: '#10b981', bg: 'rgba(16,185,129,0.08)', border: 'rgba(16,185,129,0.25)' },
  running:   { icon: '🔄', color: '#3b82f6', bg: 'rgba(59,130,246,0.08)', border: 'rgba(59,130,246,0.25)' },
  pending:   { icon: '⏳', color: '#6b7280', bg: 'rgba(255,255,255,0.02)', border: 'var(--border)' },
  error:     { icon: '❌', color: '#ef4444', bg: 'rgba(239,68,68,0.08)',  border: 'rgba(239,68,68,0.25)' },
  skipped:   { icon: '⏭️', color: '#6b7280', bg: 'rgba(255,255,255,0.02)', border: 'var(--border)' },
};

// ── 统计卡片 ──
function SummaryStats() {
  const total = workflowTemplates.length;
  const completed = workflowTemplates.filter(w => w.status === 'completed').length;
  const running = workflowTemplates.filter(w => w.status === 'running').length;
  const avgSuccess = Math.round(workflowTemplates.reduce((s, w) => s + w.successRate, 0) / total * 10) / 10;
  const totalRuns = workflowTemplates.reduce((s, w) => s + w.totalRuns, 0);

  const stats = [
    { label: '工作流总数', value: total, icon: '⚡', color: '#3b82f6' },
    { label: '已完成', value: completed, icon: '✅', color: '#10b981' },
    { label: '执行中', value: running, icon: '🔄', color: '#f59e0b' },
    { label: '平均成功率', value: `${avgSuccess}%`, icon: '📊', color: '#8b5cf6' },
    { label: '累计执行', value: totalRuns.toLocaleString(), icon: '📈', color: '#06b6d4' },
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 12, marginBottom: 20 }}>
      {stats.map(s => (
        <div key={s.label} className="card" style={{ padding: '14px 16px', textAlign: 'center' }}>
          <div style={{ fontSize: 20, marginBottom: 4 }}>{s.icon}</div>
          <div style={{ fontSize: 22, fontWeight: 700, color: s.color }}>{s.value}</div>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>{s.label}</div>
        </div>
      ))}
    </div>
  );
}

// ── 步骤详情面板 ──
function StepDetail({ step, index, isLast }: { step: Workflow['steps'][0]; index: number; isLast: boolean }) {
  const cfg = stepStatusConfig[step.status];
  const agentInfo = agents.find(a => a.id === step.agent);

  return (
    <div style={{ display: 'flex', gap: 0 }}>
      {/* 时间线 */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 32, flexShrink: 0 }}>
        <div style={{
          width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
          background: cfg.bg, border: `2px solid ${cfg.border}`, fontSize: 13, flexShrink: 0,
        }}>
          {cfg.icon}
        </div>
        {!isLast && <div style={{ width: 2, flex: 1, background: 'var(--border)', margin: '4px 0' }} />}
      </div>

      {/* 步骤内容 */}
      <div style={{ flex: 1, paddingBottom: isLast ? 0 : 16, marginLeft: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
          <span style={{ fontWeight: 600, fontSize: 13 }}>步骤 {index + 1}: {step.name}</span>
          <span className="badge" style={{ fontSize: 10, padding: '2px 8px', background: `${cfg.color}20`, color: cfg.color }}>
            {step.duration}
          </span>
        </div>

        {/* Agent + Tool */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 6, fontSize: 12, color: 'var(--text-secondary)' }}>
          <span>{agentInfo?.icon || '🤖'} {agentInfo?.name || step.agent}</span>
          {step.tool && (
            <span style={{
              fontSize: 10, padding: '1px 6px', borderRadius: 4,
              background: 'rgba(139,92,246,0.1)', color: '#a78bfa', fontFamily: 'monospace',
            }}>
              {step.tool}
            </span>
          )}
        </div>

        {/* Input / Output */}
        {step.input && (
          <div style={{
            marginTop: 6, padding: '6px 10px', borderRadius: 6, fontSize: 11,
            background: 'rgba(59,130,246,0.06)', border: '1px solid rgba(59,130,246,0.12)',
            fontFamily: 'monospace', color: '#93c5fd', wordBreak: 'break-all',
          }}>
            <span style={{ color: 'var(--text-muted)', fontFamily: 'inherit' }}>📥 </span>{step.input}
          </div>
        )}
        {step.output && (
          <div style={{
            marginTop: 4, padding: '6px 10px', borderRadius: 6, fontSize: 11,
            background: 'rgba(16,185,129,0.06)', border: '1px solid rgba(16,185,129,0.12)',
            fontFamily: 'monospace', color: '#6ee7b7', wordBreak: 'break-all',
          }}>
            <span style={{ color: 'var(--text-muted)', fontFamily: 'inherit' }}>📤 </span>{step.output}
          </div>
        )}
      </div>
    </div>
  );
}

// ── 工作流卡片 ──
function WorkflowCard({ workflow }: { workflow: Workflow }) {
  const [expanded, setExpanded] = useState(false);
  const st = statusConfig[workflow.status];
  const cat = categoryLabels[workflow.category];

  return (
    <div className="card" style={{ overflow: 'hidden', transition: 'all 0.2s' }}>
      {/* 卡片头部 */}
      <div
        onClick={() => setExpanded(!expanded)}
        style={{ cursor: 'pointer', padding: '16px 20px' }}
      >
        {/* 第一行: 名称 + 状态 */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, minWidth: 0 }}>
            <span style={{ fontSize: 18 }}>{cat.icon}</span>
            <span style={{ fontSize: 15, fontWeight: 600, whiteSpace: 'nowrap' }}>{workflow.name}</span>
            <span style={{
              fontSize: 10, padding: '2px 6px', borderRadius: 4, fontWeight: 700,
              background: `${priorityColors[workflow.priority]}20`, color: priorityColors[workflow.priority],
            }}>
              {workflow.priority}
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
            <span className="badge" style={{ background: `${st.color}18`, color: st.color, fontSize: 11 }}>
              {st.icon} {st.label}
            </span>
            <span style={{ fontSize: 14, color: 'var(--text-muted)', transition: 'transform 0.2s', transform: expanded ? 'rotate(180deg)' : 'rotate(0)' }}>
              ▼
            </span>
          </div>
        </div>

        {/* 第二行: 描述 */}
        <p style={{ margin: '8px 0 0', fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.5 }}>
          {workflow.description}
        </p>

        {/* 第三行: 元数据 */}
        <div style={{ display: 'flex', gap: 16, marginTop: 10, fontSize: 11, color: 'var(--text-muted)', flexWrap: 'wrap' }}>
          <span>{triggerLabels[workflow.trigger]}</span>
          <span>⏱️ 平均 {workflow.avgDuration}</span>
          <span>✅ 成功率 {workflow.successRate}%</span>
          <span>📊 累计 {workflow.totalRuns} 次</span>
          <span>🕐 最近: {workflow.lastRun}</span>
        </div>

        {/* 第四行: Agent 标签 */}
        <div style={{ display: 'flex', gap: 6, marginTop: 10, flexWrap: 'wrap' }}>
          {workflow.agents.map(aid => {
            const a = agents.find(ag => ag.id === aid);
            return a ? (
              <span key={aid} style={{
                fontSize: 10, padding: '2px 8px', borderRadius: 10,
                background: `${a.color}15`, color: a.color, border: `1px solid ${a.color}30`,
              }}>
                {a.icon} {a.name.replace(' Agent', '').replace('AI ', '')}
              </span>
            ) : null;
          })}
        </div>

        {/* 第五行: 步骤进度条 */}
        <div style={{ display: 'flex', gap: 3, marginTop: 12, height: 4, borderRadius: 2, overflow: 'hidden' }}>
          {workflow.steps.map((s, i) => (
            <div key={i} style={{
              flex: 1, borderRadius: 2,
              background: s.status === 'completed' ? '#10b981' :
                          s.status === 'running' ? '#3b82f6' :
                          s.status === 'error' ? '#ef4444' : 'rgba(255,255,255,0.08)',
            }} />
          ))}
        </div>
      </div>

      {/* 展开: 步骤详情 */}
      {expanded && (
        <div style={{ padding: '0 20px 20px', borderTop: '1px solid var(--border)' }}>
          {/* 步骤流程图 */}
          <div style={{ marginTop: 16 }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 12 }}>
              📋 执行步骤 ({workflow.steps.filter(s => s.status === 'completed').length}/{workflow.steps.length} 完成)
            </div>
            {workflow.steps.map((step, i) => (
              <StepDetail key={i} step={step} index={i} isLast={i === workflow.steps.length - 1} />
            ))}
          </div>

          {/* 底部: 执行时间线 */}
          {workflow.triggeredAt && (
            <div style={{
              marginTop: 16, padding: '10px 14px', borderRadius: 8,
              background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border)',
              display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--text-muted)',
            }}>
              <span>🕐 触发: {workflow.triggeredAt}</span>
              {workflow.completedAt && <span>✅ 完成: {workflow.completedAt}</span>}
              <span>📈 共 {workflow.steps.length} 个步骤</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── 主页面 ──
export default function WorkflowsPage() {
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [activeStatus, setActiveStatus] = useState<string>('all');

  const filtered = workflowTemplates.filter(w => {
    if (activeCategory !== 'all' && w.category !== activeCategory) return false;
    if (activeStatus !== 'all' && w.status !== activeStatus) return false;
    return true;
  });

  const categories = Object.entries(categoryLabels);

  return (
    <div className="animate-fade-in">
      {/* 页面头部 */}
      <div className="page-header">
        <div>
          <h1 className="page-title">⚡ 工作流引擎</h1>
          <p className="page-subtitle">企业级自动化运维编排 · {workflowTemplates.length} 条真实工作流 · 覆盖 6 大场景</p>
        </div>
      </div>

      {/* 统计概览 */}
      <SummaryStats />

      {/* 分类筛选 */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
        <button
          onClick={() => setActiveCategory('all')}
          style={{
            padding: '6px 14px', borderRadius: 8, border: '1px solid var(--border)',
            background: activeCategory === 'all' ? 'rgba(59,130,246,0.15)' : 'transparent',
            color: activeCategory === 'all' ? '#3b82f6' : 'var(--text-secondary)',
            cursor: 'pointer', fontSize: 12, fontWeight: 500, transition: 'all 0.15s',
          }}
        >
          🏠 全部 ({workflowTemplates.length})
        </button>
        {categories.map(([key, cat]) => {
          const count = workflowTemplates.filter(w => w.category === key).length;
          return (
            <button
              key={key}
              onClick={() => setActiveCategory(key)}
              style={{
                padding: '6px 14px', borderRadius: 8, border: `1px solid ${activeCategory === key ? cat.color + '60' : 'var(--border)'}`,
                background: activeCategory === key ? `${cat.color}18` : 'transparent',
                color: activeCategory === key ? cat.color : 'var(--text-secondary)',
                cursor: 'pointer', fontSize: 12, fontWeight: 500, transition: 'all 0.15s',
              }}
            >
              {cat.icon} {cat.label} ({count})
            </button>
          );
        })}
      </div>

      {/* 状态筛选 */}
      <div style={{ display: 'flex', gap: 6, marginBottom: 16 }}>
        {(['all', 'completed', 'running', 'pending', 'error'] as const).map(s => {
          const cfg = s === 'all' ? { icon: '📋', label: '全部', color: '#6b7280' } : statusConfig[s];
          const count = s === 'all' ? workflowTemplates.length : workflowTemplates.filter(w => w.status === s).length;
          return (
            <button
              key={s}
              onClick={() => setActiveStatus(s)}
              style={{
                padding: '4px 10px', borderRadius: 6, border: `1px solid ${activeStatus === s ? cfg.color + '60' : 'var(--border)'}`,
                background: activeStatus === s ? `${cfg.color}18` : 'transparent',
                color: activeStatus === s ? cfg.color : 'var(--text-muted)',
                cursor: 'pointer', fontSize: 11, transition: 'all 0.15s',
              }}
            >
              {cfg.icon} {cfg.label} ({count})
            </button>
          );
        })}
      </div>

      {/* 工作流列表 */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {filtered.map(wf => (
          <WorkflowCard key={wf.id} workflow={wf} />
        ))}
        {filtered.length === 0 && (
          <div className="card" style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
            <div style={{ fontSize: 32, marginBottom: 8 }}>🔍</div>
            <div>暂无匹配的工作流</div>
          </div>
        )}
      </div>
    </div>
  );
}
