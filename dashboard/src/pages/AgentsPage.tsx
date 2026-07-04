import { agents, toolCategories } from '../data/agents';

export default function AgentsPage() {
  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">🤖 智能体 & 工具</h1>
          <p className="page-subtitle">{agents.length} 个专业智能体 · {toolCategories.reduce((a,c)=>a+c.count,0)} 个 MCP 工具 · 统一调度</p>
        </div>
      </div>

      {/* Tool Categories */}
      <div style={{marginBottom:24}}>
        <h2 style={{fontSize:16,fontWeight:600,marginBottom:12,color:'var(--text-primary)'}}>🔌 工具覆盖 (15 类 {toolCategories.reduce((a,c)=>a+c.count,0)} 个)</h2>
        <div style={{display:'grid',gridTemplateColumns:'repeat(5,1fr)',gap:12}}>
          {toolCategories.map((cat,i) => (
            <div key={i} className="card" style={{padding:12}}>
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:8}}>
                <span style={{fontSize:20}}>{cat.icon}</span>
                <div>
                  <div style={{fontSize:13,fontWeight:600}}>{cat.name}</div>
                  <div style={{fontSize:20,fontWeight:700,color:cat.color}}>{cat.count}</div>
                </div>
              </div>
              <div style={{fontSize:10,color:'var(--text-muted)',lineHeight:1.4}}>
                {cat.tools.join(' · ')}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Agents */}
      <h2 style={{fontSize:16,fontWeight:600,marginBottom:12,color:'var(--text-primary)'}}>🤖 智能体列表</h2>
      <div style={{display:'grid',gridTemplateColumns:'repeat(3, 1fr)',gap:16}}>
        {agents.map(agent => (
          <div key={agent.id} className="card" style={{cursor:'pointer'}}>
            <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:12}}>
              <div style={{fontSize:32}}>{agent.icon}</div>
              <div>
                <div style={{fontSize:15,fontWeight:600}}>{agent.name}</div>
                <div style={{fontSize:12,color:'var(--text-muted)'}}>{agent.description}</div>
              </div>
            </div>
            <div style={{display:'flex',gap:8,marginBottom:12}}>
              <span className={`badge ${agent.status==='active'?'badge-green':agent.status==='idle'?'badge-yellow':'badge-red'}`}>
                {agent.status==='active'?'运行中':agent.status==='idle'?'空闲':'异常'}
              </span>
              <span className="badge badge-blue">{agent.category}</span>
            </div>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:8}}>
              <div style={{textAlign:'center',padding:8,background:'rgba(255,255,255,0.02)',borderRadius:8}}>
                <div style={{fontSize:18,fontWeight:700,color:'var(--accent-blue)'}}>{agent.tasks}</div>
                <div style={{fontSize:10,color:'var(--text-muted)'}}>总任务</div>
              </div>
              <div style={{textAlign:'center',padding:8,background:'rgba(255,255,255,0.02)',borderRadius:8}}>
                <div style={{fontSize:18,fontWeight:700,color:'var(--accent-green)'}}>{agent.successRate}%</div>
                <div style={{fontSize:10,color:'var(--text-muted)'}}>成功率</div>
              </div>
              <div style={{textAlign:'center',padding:8,background:'rgba(255,255,255,0.02)',borderRadius:8}}>
                <div style={{fontSize:18,fontWeight:700,color:'var(--accent-purple)'}}>{agent.avgResponseTime}</div>
                <div style={{fontSize:10,color:'var(--text-muted)'}}>响应时间</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
