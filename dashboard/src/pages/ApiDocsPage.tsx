import { useState } from 'react';

interface Endpoint {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  title: string;
  category: string;
  description: string;
  params?: { name: string; type: string; required: boolean; desc: string }[];
  requestExample?: string;
  responseExample?: string;
}

const endpoints: Endpoint[] = [
  {
    method: 'GET', path: '/api/v1/health', title: '健康检查', category: '基础',
    description: '检查 API 服务是否正常运行，无需认证',
    responseExample: `{\n  "status": "healthy",\n  "version": "4.2.0"\n}`
  },
  {
    method: 'GET', path: '/api/v1/version', title: '版本信息', category: '基础',
    description: '获取当前系统版本',
    responseExample: `{\n  "version": "4.2.0",\n  "python": "3.12.3"\n}`
  },
  {
    method: 'POST', path: '/api/v1/diagnose', title: '执行诊断', category: '诊断',
    description: '执行完整诊断任务，自动选择合适的 Agent',
    params: [
      { name: 'host', type: 'string', required: true, desc: '目标主机 IP' },
      { name: 'symptom', type: 'string', required: false, desc: '症状描述' },
      { name: 'agent', type: 'string', required: false, desc: '指定 Agent' },
      { name: 'timeout', type: 'integer', required: false, desc: '超时秒数' },
    ],
    requestExample: `{\n  "host": "10.0.0.1",\n  "symptom": "CPU 高",\n  "agent": "linux"\n}`,
    responseExample: `{\n  "status": "completed",\n  "root_cause": "Java Full GC",\n  "confidence": 0.94,\n  "suggestion": "增大 JVM 堆内存"\n}`
  },
  {
    method: 'GET', path: '/api/v1/agents', title: '列出智能体', category: '智能体',
    description: '列出所有 12 个可用智能体及其状态',
    responseExample: `{\n  "agents": [\n    {"name": "linux", "status": "ready"},\n    {"name": "k8s", "status": "ready"},\n    {"name": "db", "status": "ready"}\n  ]\n}`
  },
  {
    method: 'GET', path: '/api/v1/agents/{agent}', title: '智能体详情', category: '智能体',
    description: '获取指定智能体的详细信息',
    responseExample: `{\n  "name": "linux",\n  "status": "ready",\n  "tools": ["ssh_exec", "top", "ps"],\n  "stats": {"total_tasks": 1247, "success_rate": 0.94}\n}`
  },
  {
    method: 'POST', path: '/api/v1/agents/{agent}/run', title: '运行智能体', category: '智能体',
    description: '运行指定智能体执行任务',
    params: [
      { name: 'task', type: 'string', required: true, desc: '任务描述' },
      { name: 'context', type: 'object', required: false, desc: '上下文信息' },
      { name: 'timeout', type: 'integer', required: false, desc: '超时秒数' },
    ],
    requestExample: `{\n  "task": "检查 CPU 使用情况",\n  "timeout": 60\n}`,
    responseExample: `{\n  "status": "completed",\n  "result": {"answer": "CPU 23%，正常"}\n}`
  },
  {
    method: 'GET', path: '/api/v1/tools', title: '列出工具', category: '工具',
    description: '列出所有可用的 MCP 工具',
    responseExample: `{\n  "tools": [\n    {"name": "ssh_exec", "category": "system"},\n    {"name": "mysql_query", "category": "database"},\n    {"name": "prometheus_query", "category": "monitoring"}\n  ]\n}`
  },
  {
    method: 'POST', path: '/api/v1/tools/execute', title: '执行工具', category: '工具',
    description: '执行指定工具',
    params: [
      { name: 'tool', type: 'string', required: true, desc: '工具名称' },
      { name: 'params', type: 'object', required: true, desc: '工具参数' },
    ],
    requestExample: `{\n  "tool": "ssh_exec",\n  "params": {"host": "10.0.0.1", "command": "df -h"}\n}`,
    responseExample: `{\n  "tool": "ssh_exec",\n  "result": {"output": "Filesystem Size Used...", "exit_code": 0}\n}`
  },
  {
    method: 'POST', path: '/api/v1/workflows/run', title: '运行工作流', category: '工作流',
    description: '运行指定的自动化工作流',
    params: [
      { name: 'workflow', type: 'string', required: true, desc: '工作流名称' },
      { name: 'variables', type: 'object', required: false, desc: '工作流变量' },
    ],
    requestExample: `{\n  "workflow": "cpu-high-diagnosis",\n  "variables": {"host": "10.0.0.1"}\n}`,
    responseExample: `{\n  "run_id": "run_xyz789",\n  "status": "started"\n}`
  },
  {
    method: 'POST', path: '/api/v1/knowledge/search', title: '搜索知识库', category: '知识库',
    description: '语义搜索知识库中的 Runbook、文档、历史案例',
    params: [
      { name: 'query', type: 'string', required: true, desc: '搜索关键词' },
      { name: 'type', type: 'string', required: false, desc: '类型：runbook/incident/document' },
      { name: 'limit', type: 'integer', required: false, desc: '返回数量' },
    ],
    requestExample: `{\n  "query": "Redis 连接池耗尽",\n  "type": "runbook"\n}`,
    responseExample: `{\n  "results": [\n    {"title": "Redis 连接超时处理", "score": 0.92}\n  ]\n}`
  },
  {
    method: 'GET', path: '/api/v1/memory/stats', title: '记忆统计', category: '记忆系统',
    description: '获取 5 类记忆系统的统计信息',
    responseExample: `{\n  "total_memories": 1247,\n  "by_type": {\n    "working": 15, "short_term": 89,\n    "long_term": 567, "semantic": 312,\n    "episodic": 264\n  }\n}`
  },
  {
    method: 'POST', path: '/api/v1/approvals/create', title: '创建审批', category: '审批',
    description: '创建审批请求，用于高风险操作审批',
    params: [
      { name: 'title', type: 'string', required: true, desc: '审批标题' },
      { name: 'command', type: 'string', required: true, desc: '待执行命令' },
      { name: 'risk_level', type: 'string', required: false, desc: 'low/medium/high' },
    ],
    requestExample: `{\n  "title": "重启 Nginx",\n  "command": "systemctl restart nginx",\n  "risk_level": "low"\n}`,
    responseExample: `{\n  "request_id": "apr_003",\n  "status": "pending"\n}`
  },
  {
    method: 'GET', path: '/api/v1/events', title: '事件列表', category: '事件总线',
    description: '获取事件总线中的事件流',
    params: [
      { name: 'level', type: 'string', required: false, desc: 'info/warning/error/critical' },
      { name: 'limit', type: 'integer', required: false, desc: '返回数量' },
    ],
    responseExample: `{\n  "events": [\n    {\n      "level": "error",\n      "title": "CPU 超阈值",\n      "source": "agent:linux"\n    }\n  ]\n}`
  },
  {
    method: 'POST', path: '/api/v1/events/emit', title: '发布事件', category: '事件总线',
    description: '发布事件到事件总线',
    params: [
      { name: 'level', type: 'string', required: true, desc: '事件级别' },
      { name: 'title', type: 'string', required: true, desc: '事件标题' },
      { name: 'metadata', type: 'object', required: false, desc: '元数据' },
    ],
    requestExample: `{\n  "level": "warning",\n  "title": "磁盘空间不足",\n  "metadata": {"disk_percent": 85}\n}`
  },
];

const methodColors: Record<string, string> = {
  GET: '#22c55e', POST: '#3b82f6', PUT: '#f59e0b', DELETE: '#ef4444',
};

const methodBg: Record<string, string> = {
  GET: 'rgba(34,197,94,0.15)', POST: 'rgba(59,130,246,0.15)', PUT: 'rgba(245,158,11,0.15)', DELETE: 'rgba(239,68,68,0.15)',
};

export default function ApiDocsPage() {
  const [expanded, setExpanded] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('全部');
  const categories = ['全部', ...Array.from(new Set(endpoints.map(e => e.category)))];
  const filtered = filter === '全部' ? endpoints : endpoints.filter(e => e.category === filter);

  return (
    <div>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:24}}>
        <div>
          <h2 style={{fontSize:24,fontWeight:700,marginBottom:4}}>📖 API 文档</h2>
          <p style={{fontSize:14,color:'#64748b'}}>REST API · Base URL: http://localhost:8000/api/v1 · Bearer Token 认证</p>
        </div>
        <a href="https://gitee.com/neal4752/agentic-aiops/blob/main/docs/api.md"
           target="_blank" rel="noreferrer"
           style={{padding:'8px 16px',background:'rgba(59,130,246,0.15)',border:'1px solid rgba(59,130,246,0.3)',borderRadius:8,color:'#3b82f6',fontSize:13,textDecoration:'none'}}>
          📄 完整 Markdown 文档
        </a>
      </div>

      {/* Category Tabs */}
      <div style={{display:'flex',gap:8,marginBottom:20,flexWrap:'wrap'}}>
        {categories.map(c => (
          <button key={c} onClick={() => setFilter(c)}
            style={{padding:'6px 14px',borderRadius:6,border:'1px solid',fontSize:13,cursor:'pointer',
              background: filter===c ? 'rgba(59,130,246,0.2)' : 'transparent',
              borderColor: filter===c ? '#3b82f6' : 'rgba(59,130,246,0.2)',
              color: filter===c ? '#3b82f6' : '#94a3b8'}}>
            {c} ({c==='全部' ? endpoints.length : endpoints.filter(e=>e.category===c).length})
          </button>
        ))}
      </div>

      {/* Endpoint List */}
      <div style={{display:'flex',flexDirection:'column',gap:8}}>
        {filtered.map(ep => {
          const isOpen = expanded === `${ep.method}-${ep.path}`;
          return (
            <div key={`${ep.method}-${ep.path}`}
              style={{background:'rgba(15,23,42,0.6)',border:'1px solid rgba(59,130,246,0.12)',borderRadius:10,overflow:'hidden',cursor:'pointer'}}
              onClick={() => setExpanded(isOpen ? null : `${ep.method}-${ep.path}`)}>

              {/* Header */}
              <div style={{display:'flex',alignItems:'center',gap:12,padding:'14px 18px'}}>
                <span style={{background:methodBg[ep.method],color:methodColors[ep.method],padding:'3px 10px',borderRadius:5,fontSize:12,fontWeight:700,fontFamily:'monospace',minWidth:60,textAlign:'center'}}>
                  {ep.method}
                </span>
                <code style={{color:'#e2e8f0',fontSize:14,fontFamily:'monospace',flex:1}}>{ep.path}</code>
                <span style={{color:'#94a3b8',fontSize:13}}>{ep.title}</span>
                <span style={{color:'#475569',fontSize:12}}>{isOpen ? '▲' : '▼'}</span>
              </div>

              {/* Expanded Detail */}
              {isOpen && (
                <div style={{padding:'0 18px 18px',borderTop:'1px solid rgba(59,130,246,0.1)'}}>
                  <p style={{color:'#94a3b8',fontSize:13,margin:'14px 0'}}>{ep.description}</p>

                  {/* Parameters */}
                  {ep.params && ep.params.length > 0 && (
                    <div style={{marginBottom:16}}>
                      <h4 style={{color:'#e2e8f0',fontSize:13,marginBottom:8}}>参数</h4>
                      <div style={{background:'rgba(30,41,59,0.5)',borderRadius:8,overflow:'hidden'}}>
                        <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
                          <thead>
                            <tr style={{background:'rgba(59,130,246,0.08)'}}>
                              <th style={{textAlign:'left',padding:'8px 12px',color:'#64748b',fontWeight:500}}>名称</th>
                              <th style={{textAlign:'left',padding:'8px 12px',color:'#64748b',fontWeight:500}}>类型</th>
                              <th style={{textAlign:'left',padding:'8px 12px',color:'#64748b',fontWeight:500}}>必填</th>
                              <th style={{textAlign:'left',padding:'8px 12px',color:'#64748b',fontWeight:500}}>说明</th>
                            </tr>
                          </thead>
                          <tbody>
                            {ep.params.map(p => (
                              <tr key={p.name} style={{borderTop:'1px solid rgba(59,130,246,0.08)'}}>
                                <td style={{padding:'8px 12px',color:'#e2e8f0',fontFamily:'monospace'}}>{p.name}</td>
                                <td style={{padding:'8px 12px',color:'#8b5cf6'}}>{p.type}</td>
                                <td style={{padding:'8px 12px'}}>{p.required
                                  ? <span style={{color:'#ef4444',fontSize:11}}>必填</span>
                                  : <span style={{color:'#475569'}}>可选</span>}</td>
                                <td style={{padding:'8px 12px',color:'#94a3b8'}}>{p.desc}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {/* Request / Response Examples */}
                  <div style={{display:'grid',gridTemplateColumns: ep.requestExample ? '1fr 1fr' : '1fr',gap:12}}>
                    {ep.requestExample && (
                      <div>
                        <h4 style={{color:'#22c55e',fontSize:12,marginBottom:6}}>📝 请求示例</h4>
                        <pre style={{background:'rgba(30,41,59,0.7)',border:'1px solid rgba(34,197,94,0.15)',borderRadius:8,padding:14,color:'#94a3b8',fontSize:12,fontFamily:'monospace',overflow:'auto',margin:0}}>
                          {ep.requestExample}
                        </pre>
                      </div>
                    )}
                    {ep.responseExample && (
                      <div>
                        <h4 style={{color:'#3b82f6',fontSize:12,marginBottom:6}}>📤 响应示例</h4>
                        <pre style={{background:'rgba(30,41,59,0.7)',border:'1px solid rgba(59,130,246,0.15)',borderRadius:8,padding:14,color:'#94a3b8',fontSize:12,fontFamily:'monospace',overflow:'auto',margin:0}}>
                          {ep.responseExample}
                        </pre>
                      </div>
                    )}
                  </div>

                  {/* curl Example */}
                  <div style={{marginTop:12}}>
                    <h4 style={{color:'#f59e0b',fontSize:12,marginBottom:6}}>⚡ curl 测试</h4>
                    <pre style={{background:'rgba(30,41,59,0.7)',border:'1px solid rgba(245,158,11,0.15)',borderRadius:8,padding:14,color:'#f59e0b',fontSize:12,fontFamily:'monospace',overflow:'auto',margin:0}}>
{ep.method === 'GET'
  ? `curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000${ep.path}`
  : `curl -X ${ep.method} -H "Authorization: Bearer <TOKEN>" \\\n  -H "Content-Type: application/json" \\\n  -d '${ep.requestExample || '{}'}' \\\n  http://localhost:8000${ep.path}`}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Error Codes Section */}
      <div style={{marginTop:32,background:'rgba(15,23,42,0.6)',border:'1px solid rgba(59,130,246,0.12)',borderRadius:12,padding:20}}>
        <h3 style={{color:'#e2e8f0',fontSize:16,marginBottom:16}}>❌ 错误码</h3>
        <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
          <thead>
            <tr style={{background:'rgba(59,130,246,0.08)'}}>
              <th style={{textAlign:'left',padding:'10px 14px',color:'#64748b',fontWeight:500}}>HTTP 状态码</th>
              <th style={{textAlign:'left',padding:'10px 14px',color:'#64748b',fontWeight:500}}>错误码</th>
              <th style={{textAlign:'left',padding:'10px 14px',color:'#64748b',fontWeight:500}}>说明</th>
            </tr>
          </thead>
          <tbody>
            {[['400','INVALID_REQUEST','请求参数错误'],['401','UNAUTHORIZED','未认证或 Token 无效'],['403','FORBIDDEN','权限不足'],['404','NOT_FOUND','资源不存在'],['429','RATE_LIMITED','请求频率超限'],['500','INTERNAL_ERROR','服务器内部错误']].map(([code,err,msg])=>(
              <tr key={code} style={{borderTop:'1px solid rgba(59,130,246,0.08)'}}>
                <td style={{padding:'10px 14px',color:'#e2e8f0',fontFamily:'monospace'}}>{code}</td>
                <td style={{padding:'10px 14px',color:'#8b5cf6',fontFamily:'monospace'}}>{err}</td>
                <td style={{padding:'10px 14px',color:'#94a3b8'}}>{msg}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
