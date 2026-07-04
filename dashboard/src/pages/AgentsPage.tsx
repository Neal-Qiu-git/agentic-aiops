import { agents } from '../data/agents';

export default function AgentsPage() {
  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">🤖 智能体管理</h1>
          <p className="page-subtitle">12 个专业运维智能体 · 统一调度</p>
        </div>
      </div>

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
