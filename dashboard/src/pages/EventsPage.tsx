import { events, agents } from '../data/agents';

const typeConfig: Record<string, { color: string; label: string }> = {
  success: { color: 'var(--accent-green)', label: '成功' },
  warning: { color: 'var(--accent-yellow)', label: '警告' },
  error: { color: 'var(--accent-red)', label: '错误' },
  info: { color: 'var(--accent-blue)', label: '信息' },
};

export default function EventsPage() {
  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">📡 事件日志</h1>
          <p className="page-subtitle">实时事件流 · 告警记录</p>
        </div>
        <div style={{display:'flex',gap:8}}>
          {Object.entries(typeConfig).map(([type, config]) => (
            <span key={type} className="badge" style={{background:`${config.color}20`,color:config.color}}>
              {config.label}
            </span>
          ))}
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>时间</th>
              <th>级别</th>
              <th>事件</th>
              <th>描述</th>
              <th>智能体</th>
            </tr>
          </thead>
          <tbody>
            {events.map((e, i) => {
              const config = typeConfig[e.type] || typeConfig.info;
              return (
                <tr key={i}>
                  <td style={{color:'var(--text-muted)',fontFamily:'monospace'}}>{e.time}</td>
                  <td>
                    <span className="badge" style={{background:`${config.color}20`,color:config.color}}>
                      {config.label}
                    </span>
                  </td>
                  <td style={{fontWeight:500}}>{e.title}</td>
                  <td style={{color:'var(--text-secondary)',maxWidth:300}}>{e.desc}</td>
                  <td>
                    <span style={{display:'inline-flex',alignItems:'center',gap:4}}>
                      {(() => { const a = agents.find(a=>a.id===e.agent); return a ? `${a.icon} ${a.name}` : e.agent; })()}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
