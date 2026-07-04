import { workflows, agents } from '../data/agents';

const statusColors: Record<string, string> = {
  completed: 'var(--accent-green)',
  running: 'var(--accent-blue)',
  pending: 'var(--text-muted)',
  error: 'var(--accent-red)',
};

const stepStatus: Record<string, { icon: string; color: string }> = {
  completed: { icon: '✅', color: 'var(--accent-green)' },
  running: { icon: '🔄', color: 'var(--accent-blue)' },
  pending: { icon: '⏳', color: 'var(--text-muted)' },
  error: { icon: '❌', color: 'var(--accent-red)' },
};

export default function WorkflowsPage() {
  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">⚡ 工作流</h1>
          <p className="page-subtitle">自动化运维编排 · 执行状态</p>
        </div>
      </div>

      <div style={{display:'flex',flexDirection:'column',gap:16}}>
        {workflows.map(wf => (
          <div key={wf.id} className="card">
            <div className="card-header">
              <div style={{display:'flex',alignItems:'center',gap:12}}>
                <span style={{fontSize:16,fontWeight:600}}>{wf.name}</span>
                <span className="badge" style={{
                  background: `${statusColors[wf.status]}20`,
                  color: statusColors[wf.status]
                }}>
                  {wf.status === 'completed' ? '✅ 已完成' : wf.status === 'running' ? '🔄 执行中' : '⏳ 待执行'}
                </span>
              </div>
              <span style={{fontSize:12,color:'var(--text-muted)'}}>
                触发: {wf.triggeredAt} {wf.completedAt ? `· 完成: ${wf.completedAt}` : ''}
              </span>
            </div>

            {/* Steps */}
            <div style={{display:'flex',gap:0,alignItems:'center',overflowX:'auto',padding:'8px 0'}}>
              {wf.steps.map((step, i) => (
                <div key={i} style={{display:'flex',alignItems:'center'}}>
                  <div style={{
                    minWidth:120,
                    padding:'12px 16px',
                    background: step.status === 'completed' ? 'rgba(16,185,129,0.08)' :
                               step.status === 'running' ? 'rgba(59,130,246,0.08)' :
                               'rgba(255,255,255,0.02)',
                    border: `1px solid ${step.status === 'completed' ? 'rgba(16,185,129,0.2)' :
                                         step.status === 'running' ? 'rgba(59,130,246,0.2)' :
                                         'var(--border)'}`,
                    borderRadius: 8,
                    textAlign: 'center',
                  }}>
                    <div style={{fontSize:16}}>{stepStatus[step.status].icon}</div>
                    <div style={{fontSize:12,fontWeight:500,marginTop:4}}>{step.name}</div>
                    <div style={{fontSize:10,color:'var(--text-muted)',marginTop:2}}>
                      {agents.find(a=>a.id===step.agent)?.icon} {step.agent} · {step.duration}
                    </div>
                  </div>
                  {i < wf.steps.length - 1 && (
                    <div style={{width:24,height:2,background:step.status==='completed'?'var(--accent-green)':'var(--border)',flexShrink:0}}/>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
