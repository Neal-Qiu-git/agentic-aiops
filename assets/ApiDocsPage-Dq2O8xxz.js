import{i as e,s as t,t as n}from"./index-BqmZOcYQ.js";var r=t(e(),1),i=n(),a=[{method:`GET`,path:`/api/v1/health`,title:`健康检查`,category:`基础`,description:`检查 API 服务是否正常运行，无需认证`,responseExample:`{
  "status": "healthy",
  "version": "4.2.0"
}`},{method:`GET`,path:`/api/v1/version`,title:`版本信息`,category:`基础`,description:`获取当前系统版本`,responseExample:`{
  "version": "4.2.0",
  "python": "3.12.3"
}`},{method:`POST`,path:`/api/v1/diagnose`,title:`执行诊断`,category:`诊断`,description:`执行完整诊断任务，自动选择合适的 Agent`,params:[{name:`host`,type:`string`,required:!0,desc:`目标主机 IP`},{name:`symptom`,type:`string`,required:!1,desc:`症状描述`},{name:`agent`,type:`string`,required:!1,desc:`指定 Agent`},{name:`timeout`,type:`integer`,required:!1,desc:`超时秒数`}],requestExample:`{
  "host": "10.0.0.1",
  "symptom": "CPU 高",
  "agent": "linux"
}`,responseExample:`{
  "status": "completed",
  "root_cause": "Java Full GC",
  "confidence": 0.94,
  "suggestion": "增大 JVM 堆内存"
}`},{method:`GET`,path:`/api/v1/agents`,title:`列出智能体`,category:`智能体`,description:`列出所有 12 个可用智能体及其状态`,responseExample:`{
  "agents": [
    {"name": "linux", "status": "ready"},
    {"name": "k8s", "status": "ready"},
    {"name": "db", "status": "ready"}
  ]
}`},{method:`GET`,path:`/api/v1/agents/{agent}`,title:`智能体详情`,category:`智能体`,description:`获取指定智能体的详细信息`,responseExample:`{
  "name": "linux",
  "status": "ready",
  "tools": ["ssh_exec", "top", "ps"],
  "stats": {"total_tasks": 1247, "success_rate": 0.94}
}`},{method:`POST`,path:`/api/v1/agents/{agent}/run`,title:`运行智能体`,category:`智能体`,description:`运行指定智能体执行任务`,params:[{name:`task`,type:`string`,required:!0,desc:`任务描述`},{name:`context`,type:`object`,required:!1,desc:`上下文信息`},{name:`timeout`,type:`integer`,required:!1,desc:`超时秒数`}],requestExample:`{
  "task": "检查 CPU 使用情况",
  "timeout": 60
}`,responseExample:`{
  "status": "completed",
  "result": {"answer": "CPU 23%，正常"}
}`},{method:`GET`,path:`/api/v1/tools`,title:`列出工具`,category:`工具`,description:`列出所有可用的 MCP 工具`,responseExample:`{
  "tools": [
    {"name": "ssh_exec", "category": "system"},
    {"name": "mysql_query", "category": "database"},
    {"name": "prometheus_query", "category": "monitoring"}
  ]
}`},{method:`POST`,path:`/api/v1/tools/execute`,title:`执行工具`,category:`工具`,description:`执行指定工具`,params:[{name:`tool`,type:`string`,required:!0,desc:`工具名称`},{name:`params`,type:`object`,required:!0,desc:`工具参数`}],requestExample:`{
  "tool": "ssh_exec",
  "params": {"host": "10.0.0.1", "command": "df -h"}
}`,responseExample:`{
  "tool": "ssh_exec",
  "result": {"output": "Filesystem Size Used...", "exit_code": 0}
}`},{method:`POST`,path:`/api/v1/workflows/run`,title:`运行工作流`,category:`工作流`,description:`运行指定的自动化工作流`,params:[{name:`workflow`,type:`string`,required:!0,desc:`工作流名称`},{name:`variables`,type:`object`,required:!1,desc:`工作流变量`}],requestExample:`{
  "workflow": "cpu-high-diagnosis",
  "variables": {"host": "10.0.0.1"}
}`,responseExample:`{
  "run_id": "run_xyz789",
  "status": "started"
}`},{method:`POST`,path:`/api/v1/knowledge/search`,title:`搜索知识库`,category:`知识库`,description:`语义搜索知识库中的 Runbook、文档、历史案例`,params:[{name:`query`,type:`string`,required:!0,desc:`搜索关键词`},{name:`type`,type:`string`,required:!1,desc:`类型：runbook/incident/document`},{name:`limit`,type:`integer`,required:!1,desc:`返回数量`}],requestExample:`{
  "query": "Redis 连接池耗尽",
  "type": "runbook"
}`,responseExample:`{
  "results": [
    {"title": "Redis 连接超时处理", "score": 0.92}
  ]
}`},{method:`GET`,path:`/api/v1/memory/stats`,title:`记忆统计`,category:`记忆系统`,description:`获取 5 类记忆系统的统计信息`,responseExample:`{
  "total_memories": 1247,
  "by_type": {
    "working": 15, "short_term": 89,
    "long_term": 567, "semantic": 312,
    "episodic": 264
  }
}`},{method:`POST`,path:`/api/v1/approvals/create`,title:`创建审批`,category:`审批`,description:`创建审批请求，用于高风险操作审批`,params:[{name:`title`,type:`string`,required:!0,desc:`审批标题`},{name:`command`,type:`string`,required:!0,desc:`待执行命令`},{name:`risk_level`,type:`string`,required:!1,desc:`low/medium/high`}],requestExample:`{
  "title": "重启 Nginx",
  "command": "systemctl restart nginx",
  "risk_level": "low"
}`,responseExample:`{
  "request_id": "apr_003",
  "status": "pending"
}`},{method:`GET`,path:`/api/v1/events`,title:`事件列表`,category:`事件总线`,description:`获取事件总线中的事件流`,params:[{name:`level`,type:`string`,required:!1,desc:`info/warning/error/critical`},{name:`limit`,type:`integer`,required:!1,desc:`返回数量`}],responseExample:`{
  "events": [
    {
      "level": "error",
      "title": "CPU 超阈值",
      "source": "agent:linux"
    }
  ]
}`},{method:`POST`,path:`/api/v1/events/emit`,title:`发布事件`,category:`事件总线`,description:`发布事件到事件总线`,params:[{name:`level`,type:`string`,required:!0,desc:`事件级别`},{name:`title`,type:`string`,required:!0,desc:`事件标题`},{name:`metadata`,type:`object`,required:!1,desc:`元数据`}],requestExample:`{
  "level": "warning",
  "title": "磁盘空间不足",
  "metadata": {"disk_percent": 85}
}`}],o={GET:`#22c55e`,POST:`#3b82f6`,PUT:`#f59e0b`,DELETE:`#ef4444`},s={GET:`rgba(34,197,94,0.15)`,POST:`rgba(59,130,246,0.15)`,PUT:`rgba(245,158,11,0.15)`,DELETE:`rgba(239,68,68,0.15)`};function c(){let[e,t]=(0,r.useState)(null),[n,c]=(0,r.useState)(`全部`),l=[`全部`,...Array.from(new Set(a.map(e=>e.category)))],u=n===`全部`?a:a.filter(e=>e.category===n);return(0,i.jsxs)(`div`,{children:[(0,i.jsxs)(`div`,{style:{display:`flex`,justifyContent:`space-between`,alignItems:`center`,marginBottom:24},children:[(0,i.jsxs)(`div`,{children:[(0,i.jsx)(`h2`,{style:{fontSize:24,fontWeight:700,marginBottom:4},children:`📖 API 文档`}),(0,i.jsx)(`p`,{style:{fontSize:14,color:`#64748b`},children:`REST API · Base URL: http://localhost:8000/api/v1 · Bearer Token 认证`})]}),(0,i.jsx)(`a`,{href:`https://gitee.com/neal4752/agentic-aiops/blob/main/docs/api.md`,target:`_blank`,rel:`noreferrer`,style:{padding:`8px 16px`,background:`rgba(59,130,246,0.15)`,border:`1px solid rgba(59,130,246,0.3)`,borderRadius:8,color:`#3b82f6`,fontSize:13,textDecoration:`none`},children:`📄 完整 Markdown 文档`})]}),(0,i.jsx)(`div`,{style:{display:`flex`,gap:8,marginBottom:20,flexWrap:`wrap`},children:l.map(e=>(0,i.jsxs)(`button`,{onClick:()=>c(e),style:{padding:`6px 14px`,borderRadius:6,border:`1px solid`,fontSize:13,cursor:`pointer`,background:n===e?`rgba(59,130,246,0.2)`:`transparent`,borderColor:n===e?`#3b82f6`:`rgba(59,130,246,0.2)`,color:n===e?`#3b82f6`:`#94a3b8`},children:[e,` (`,e===`全部`?a.length:a.filter(t=>t.category===e).length,`)`]},e))}),(0,i.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:8},children:u.map(n=>{let r=e===`${n.method}-${n.path}`;return(0,i.jsxs)(`div`,{style:{background:`rgba(15,23,42,0.6)`,border:`1px solid rgba(59,130,246,0.12)`,borderRadius:10,overflow:`hidden`,cursor:`pointer`},onClick:()=>t(r?null:`${n.method}-${n.path}`),children:[(0,i.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:12,padding:`14px 18px`},children:[(0,i.jsx)(`span`,{style:{background:s[n.method],color:o[n.method],padding:`3px 10px`,borderRadius:5,fontSize:12,fontWeight:700,fontFamily:`monospace`,minWidth:60,textAlign:`center`},children:n.method}),(0,i.jsx)(`code`,{style:{color:`#e2e8f0`,fontSize:14,fontFamily:`monospace`,flex:1},children:n.path}),(0,i.jsx)(`span`,{style:{color:`#94a3b8`,fontSize:13},children:n.title}),(0,i.jsx)(`span`,{style:{color:`#475569`,fontSize:12},children:r?`▲`:`▼`})]}),r&&(0,i.jsxs)(`div`,{style:{padding:`0 18px 18px`,borderTop:`1px solid rgba(59,130,246,0.1)`},children:[(0,i.jsx)(`p`,{style:{color:`#94a3b8`,fontSize:13,margin:`14px 0`},children:n.description}),n.params&&n.params.length>0&&(0,i.jsxs)(`div`,{style:{marginBottom:16},children:[(0,i.jsx)(`h4`,{style:{color:`#e2e8f0`,fontSize:13,marginBottom:8},children:`参数`}),(0,i.jsx)(`div`,{style:{background:`rgba(30,41,59,0.5)`,borderRadius:8,overflow:`hidden`},children:(0,i.jsxs)(`table`,{style:{width:`100%`,borderCollapse:`collapse`,fontSize:13},children:[(0,i.jsx)(`thead`,{children:(0,i.jsxs)(`tr`,{style:{background:`rgba(59,130,246,0.08)`},children:[(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`8px 12px`,color:`#64748b`,fontWeight:500},children:`名称`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`8px 12px`,color:`#64748b`,fontWeight:500},children:`类型`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`8px 12px`,color:`#64748b`,fontWeight:500},children:`必填`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`8px 12px`,color:`#64748b`,fontWeight:500},children:`说明`})]})}),(0,i.jsx)(`tbody`,{children:n.params.map(e=>(0,i.jsxs)(`tr`,{style:{borderTop:`1px solid rgba(59,130,246,0.08)`},children:[(0,i.jsx)(`td`,{style:{padding:`8px 12px`,color:`#e2e8f0`,fontFamily:`monospace`},children:e.name}),(0,i.jsx)(`td`,{style:{padding:`8px 12px`,color:`#8b5cf6`},children:e.type}),(0,i.jsx)(`td`,{style:{padding:`8px 12px`},children:e.required?(0,i.jsx)(`span`,{style:{color:`#ef4444`,fontSize:11},children:`必填`}):(0,i.jsx)(`span`,{style:{color:`#475569`},children:`可选`})}),(0,i.jsx)(`td`,{style:{padding:`8px 12px`,color:`#94a3b8`},children:e.desc})]},e.name))})]})})]}),(0,i.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:n.requestExample?`1fr 1fr`:`1fr`,gap:12},children:[n.requestExample&&(0,i.jsxs)(`div`,{children:[(0,i.jsx)(`h4`,{style:{color:`#22c55e`,fontSize:12,marginBottom:6},children:`📝 请求示例`}),(0,i.jsx)(`pre`,{style:{background:`rgba(30,41,59,0.7)`,border:`1px solid rgba(34,197,94,0.15)`,borderRadius:8,padding:14,color:`#94a3b8`,fontSize:12,fontFamily:`monospace`,overflow:`auto`,margin:0},children:n.requestExample})]}),n.responseExample&&(0,i.jsxs)(`div`,{children:[(0,i.jsx)(`h4`,{style:{color:`#3b82f6`,fontSize:12,marginBottom:6},children:`📤 响应示例`}),(0,i.jsx)(`pre`,{style:{background:`rgba(30,41,59,0.7)`,border:`1px solid rgba(59,130,246,0.15)`,borderRadius:8,padding:14,color:`#94a3b8`,fontSize:12,fontFamily:`monospace`,overflow:`auto`,margin:0},children:n.responseExample})]})]}),(0,i.jsxs)(`div`,{style:{marginTop:12},children:[(0,i.jsx)(`h4`,{style:{color:`#f59e0b`,fontSize:12,marginBottom:6},children:`⚡ curl 测试`}),(0,i.jsx)(`pre`,{style:{background:`rgba(30,41,59,0.7)`,border:`1px solid rgba(245,158,11,0.15)`,borderRadius:8,padding:14,color:`#f59e0b`,fontSize:12,fontFamily:`monospace`,overflow:`auto`,margin:0},children:n.method===`GET`?`curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000${n.path}`:`curl -X ${n.method} -H "Authorization: Bearer <TOKEN>" \\\n  -H "Content-Type: application/json" \\\n  -d '${n.requestExample||`{}`}' \\\n  http://localhost:8000${n.path}`})]})]})]},`${n.method}-${n.path}`)})}),(0,i.jsxs)(`div`,{style:{marginTop:32,background:`rgba(15,23,42,0.6)`,border:`1px solid rgba(59,130,246,0.12)`,borderRadius:12,padding:20},children:[(0,i.jsx)(`h3`,{style:{color:`#e2e8f0`,fontSize:16,marginBottom:16},children:`❌ 错误码`}),(0,i.jsxs)(`table`,{style:{width:`100%`,borderCollapse:`collapse`,fontSize:13},children:[(0,i.jsx)(`thead`,{children:(0,i.jsxs)(`tr`,{style:{background:`rgba(59,130,246,0.08)`},children:[(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`10px 14px`,color:`#64748b`,fontWeight:500},children:`HTTP 状态码`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`10px 14px`,color:`#64748b`,fontWeight:500},children:`错误码`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`10px 14px`,color:`#64748b`,fontWeight:500},children:`说明`})]})}),(0,i.jsx)(`tbody`,{children:[[`400`,`INVALID_REQUEST`,`请求参数错误`],[`401`,`UNAUTHORIZED`,`未认证或 Token 无效`],[`403`,`FORBIDDEN`,`权限不足`],[`404`,`NOT_FOUND`,`资源不存在`],[`429`,`RATE_LIMITED`,`请求频率超限`],[`500`,`INTERNAL_ERROR`,`服务器内部错误`]].map(([e,t,n])=>(0,i.jsxs)(`tr`,{style:{borderTop:`1px solid rgba(59,130,246,0.08)`},children:[(0,i.jsx)(`td`,{style:{padding:`10px 14px`,color:`#e2e8f0`,fontFamily:`monospace`},children:e}),(0,i.jsx)(`td`,{style:{padding:`10px 14px`,color:`#8b5cf6`,fontFamily:`monospace`},children:t}),(0,i.jsx)(`td`,{style:{padding:`10px 14px`,color:`#94a3b8`},children:n})]},e))})]})]})]})}export{c as default};