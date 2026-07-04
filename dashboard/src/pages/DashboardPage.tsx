import { agents, systemHealth, events } from '../data/agents';

export default function DashboardPage() {
  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">仪表盘</h1>
          <p className="page-subtitle">系统运行概览 · 实时状态</p>
        </div>
        <div style={{display:'flex',gap:8}}>
          <span className="badge badge-green">● 系统正常</span>
          <span className="badge badge-blue">运行 {systemHealth.uptime}</span>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-blue)'}}>🤖</div>
          <div>
            <div className="stat-value">{systemHealth.activeAgents}/{systemHealth.totalAgents}</div>
            <div className="stat-label">活跃智能体</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-purple)'}}>🔌</div>
          <div>
            <div className="stat-value">{systemHealth.totalTools}</div>
            <div className="stat-label">MCP 工具</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'var(--glow-green)'}}>⚡</div>
          <div>
            <div className="stat-value">{systemHealth.totalTasks.toLocaleString()}</div>
            <div className="stat-label">累计任务</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{background:'rgba(245,158,11,0.15)'}}>✅</div>
          <div>
            <div className="stat-value">{systemHealth.successRate}%</div>
            <div className="stat-label">成功率</div>
          </div>
        </div>
      </div>

      <div className="grid-2">
        {/* System Health */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">系统健康</span>
            <span className="badge badge-green">正常</span>
          </div>
          {[
            {label:'CPU', value: systemHealth.cpu, color:'var(--accent-blue)'},
            {label:'内存', value: systemHealth.memory, color:'var(--accent-purple)'},
            {label:'磁盘', value: systemHealth.disk, color:'var(--accent-cyan)'},
            {label:'网络', value: systemHealth.network, color:'var(--accent-green)'},
          ].map(item => (
            <div key={item.label} style={{marginBottom:12}}>
              <div style={{display:'flex',justifyContent:'space-between',marginBottom:4,fontSize:12}}>
                <span style={{color:'var(--text-secondary)'}}>{item.label}</span>
                <span style={{color: item.value > 80 ? 'var(--accent-red)' : 'var(--text-primary)',fontWeight:600}}>{item.value}%</span>
              </div>
              <div className="progress-bar">
                <div className="progress-fill" style={{width:`${item.value}%`,background: item.value > 80 ? 'var(--accent-red)' : item.color}}/>
              </div>
            </div>
          ))}
        </div>

        {/* Agent Status */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">智能体状态</span>
            <span className="badge badge-blue">{agents.filter(a=>a.status==='active').length} 活跃</span>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:8}}>
            {agents.map(agent => (
              <div key={agent.id} style={{display:'flex',alignItems:'center',gap:8,padding:'8px 12px',background:'rgba(255,255,255,0.02)',borderRadius:8}}>
                <span>{agent.icon}</span>
                <div style={{flex:1,minWidth:0}}>
                  <div style={{fontSize:12,fontWeight:500,whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{agent.name}</div>
                  <div style={{fontSize:10,color:'var(--text-muted)'}}>{agent.tasks} 任务</div>
                </div>
                <div style={{width:8,height:8,borderRadius:'50%',background:agent.status==='active'?'var(--accent-green)':agent.status==='idle'?'var(--accent-yellow)':'var(--accent-red)'}}/>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Events */}
      <div className="card" style={{marginTop:16}}>
        <div className="card-header">
          <span className="card-title">最近事件</span>
          <a href="/events" style={{fontSize:12,color:'var(--accent-blue)',textDecoration:'none'}}>查看全部 →</a>
        </div>
        {events.slice(0,5).map((e,i) => (
          <div key={i} className="event-item">
            <span className="event-time">{e.time}</span>
            <div className="event-dot" style={{background:e.type==='success'?'var(--accent-green)':e.type==='warning'?'var(--accent-yellow)':e.type==='error'?'var(--accent-red)':'var(--accent-blue)'}}/>
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
