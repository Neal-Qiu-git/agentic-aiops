import{i as e,s as t,t as n}from"./index-InlQoSr6.js";var r=t(e(),1),i=n(),a=[{method:`GET`,path:`/api/v1/health`,title:`健康检查`,category:`基础`,description:`检查 API 服务是否正常运行，无需认证`,responseExample:`{
  "status": "healthy",
  "version": "5.3.0"
}`},{method:`GET`,path:`/api/v1/version`,title:`版本信息`,category:`基础`,description:`获取当前系统版本和运行环境信息`,responseExample:`{
  "version": "5.3.0",
  "python": "3.12.3",
  "tools": 157,
  "agents": 21
}`},{method:`POST`,path:`/api/v1/diagnose`,title:`执行诊断`,category:`诊断`,description:`执行完整诊断任务，自动选择合适的 Agent 分析问题根因`,params:[{name:`host`,type:`string`,required:!0,desc:`目标主机 IP`},{name:`symptom`,type:`string`,required:!1,desc:`症状描述`},{name:`agent`,type:`string`,required:!1,desc:`指定 Agent（linux/k8s/db 等）`},{name:`timeout`,type:`integer`,required:!1,desc:`超时秒数，默认 60`}],requestExample:`{
  "host": "10.0.0.1",
  "symptom": "CPU 持续高于 90%",
  "agent": "linux"
}`,responseExample:`{
  "status": "completed",
  "root_cause": "Java Full GC 频繁",
  "confidence": 0.94,
  "suggestion": "增大 JVM 堆内存至 4G"
}`},{method:`GET`,path:`/api/v1/agents`,title:`列出智能体`,category:`智能体`,description:`列出所有 21 个可用智能体及其运行状态`,responseExample:`{
  "agents": [
    {"name": "linux", "status": "ready"},
    {"name": "kubernetes", "status": "ready"},
    {"name": "database", "status": "ready"}
  ],
  "total": 21
}`},{method:`GET`,path:`/api/v1/agents/{agent}`,title:`智能体详情`,category:`智能体`,description:`获取指定智能体的详细信息，包括工具列表和执行统计`,responseExample:`{
  "name": "linux",
  "status": "ready",
  "tools": ["ssh_exec", "system_info", "process_list"],
  "stats": {"total_tasks": 1247, "success_rate": 0.94}
}`},{method:`POST`,path:`/api/v1/agents/{agent}/run`,title:`运行智能体`,category:`智能体`,description:`运行指定智能体执行诊断或运维任务`,params:[{name:`task`,type:`string`,required:!0,desc:`任务描述`},{name:`context`,type:`object`,required:!1,desc:`上下文信息`},{name:`timeout`,type:`integer`,required:!1,desc:`超时秒数`}],requestExample:`{
  "task": "检查 CPU 使用情况并分析 top 进程",
  "timeout": 60
}`,responseExample:`{
  "status": "completed",
  "result": {"answer": "CPU 23%，top 进程为 java(12%)"}
}`},{method:`GET`,path:`/api/v1/tools`,title:`列出工具`,category:`工具`,description:`列出所有 157 个可用 MCP 工具，支持按类别筛选`,responseExample:`{
  "tools": [
    {"name": "ssh_exec", "category": "system"},
    {"name": "mysql_query", "category": "database"},
    {"name": "prometheus_query", "category": "monitoring"}
  ],
  "total": 157
}`},{method:`POST`,path:`/api/v1/tools/execute`,title:`执行工具`,category:`工具`,description:`直接执行指定工具，返回执行结果`,params:[{name:`tool`,type:`string`,required:!0,desc:`工具名称`},{name:`params`,type:`object`,required:!0,desc:`工具参数`}],requestExample:`{
  "tool": "ssh_exec",
  "params": {"host": "10.0.0.1", "command": "df -h"}
}`,responseExample:`{
  "tool": "ssh_exec",
  "result": {"output": "Filesystem  Size  Used", "exit_code": 0}
}`},{method:`POST`,path:`/api/v1/workflow/run`,title:`运行工作流`,category:`工作流`,description:`运行指定的自动化工作流，支持 10 条预置企业工作流`,params:[{name:`workflow`,type:`string`,required:!0,desc:`工作流名称`},{name:`variables`,type:`object`,required:!1,desc:`工作流变量`}],requestExample:`{
  "workflow": "cpu-high-diagnosis",
  "variables": {"host": "10.0.0.1"}
}`,responseExample:`{
  "run_id": "run_xyz789",
  "status": "started"
}`},{method:`GET`,path:`/api/v1/workflows`,title:`列出工作流`,category:`工作流`,description:`获取所有可用工作流列表及其执行状态`,responseExample:`{
  "workflows": [
    {"name": "cpu-high-diagnosis", "steps": 4},
    {"name": "deploy-canary", "steps": 6},
    {"name": "security-incident-response", "steps": 8}
  ]
}`},{method:`POST`,path:`/api/v1/approval/create`,title:`创建审批`,category:`审批`,description:`创建审批请求，用于高风险运维操作的审批流程`,params:[{name:`title`,type:`string`,required:!0,desc:`审批标题`},{name:`command`,type:`string`,required:!0,desc:`待执行命令`},{name:`risk_level`,type:`string`,required:!1,desc:`low/medium/high`}],requestExample:`{
  "title": "重启 Nginx",
  "command": "systemctl restart nginx",
  "risk_level": "low"
}`,responseExample:`{
  "request_id": "apr_003",
  "status": "pending"
}`},{method:`GET`,path:`/api/v1/monitoring/summary`,title:`监控概览`,category:`监控`,description:`获取监控系统整体概览，包括 Prometheus/Loki/SkyWalking 状态`,responseExample:`{
  "healthy_targets": 47,
  "total_targets": 52,
  "active_alerts": 3,
  "data_sources": ["prometheus", "loki", "skywalking"]
}`},{method:`GET`,path:`/api/v1/monitoring/metrics`,title:`监控指标`,category:`监控`,description:`获取实时系统指标（CPU/内存/磁盘/网络）`,responseExample:`{
  "cpu_usage": 45.2,
  "memory_usage": 68.7,
  "disk_usage": 52.1,
  "network_in": "125 MB/s",
  "network_out": "89 MB/s"
}`},{method:`GET`,path:`/api/v1/monitoring/alerts`,title:`监控告警`,category:`监控`,description:`获取当前活跃的监控告警列表`,responseExample:`{
  "alerts": [
    {"name": "HighCPU", "severity": "warning", "instance": "10.0.0.1"},
    {"name": "DiskFull", "severity": "critical", "instance": "10.0.0.3"}
  ]
}`},{method:`GET`,path:`/api/v1/monitoring/targets`,title:`监控目标`,category:`监控`,description:`获取所有监控目标（Exporter/Agent）的在线状态`,responseExample:`{
  "targets": [
    {"job": "node_exporter", "instance": "10.0.0.1:9100", "up": true},
    {"job": "mysql_exporter", "instance": "10.0.0.2:9104", "up": true}
  ]
}`},{method:`GET`,path:`/api/v1/deployment/summary`,title:`部署概览`,category:`部署`,description:`获取 Kubernetes 部署整体概览`,responseExample:`{
  "total_pods": 48,
  "running": 45,
  "pending": 2,
  "failed": 1,
  "namespaces": 6
}`},{method:`GET`,path:`/api/v1/deployment/nodes`,title:`集群节点`,category:`部署`,description:`获取 Kubernetes 集群节点状态`,responseExample:`{
  "nodes": [
    {"name": "node-1", "status": "Ready", "cpu": "4/8", "memory": "12/32Gi"},
    {"name": "node-2", "status": "Ready", "cpu": "3/8", "memory": "15/32Gi"}
  ]
}`},{method:`GET`,path:`/api/v1/deployment/pods`,title:`Pod 列表`,category:`部署`,description:`获取所有 Pod 的运行状态`,responseExample:`{
  "pods": [
    {"name": "nginx-abc123", "namespace": "default", "status": "Running", "restarts": 0},
    {"name": "redis-def456", "namespace": "middleware", "status": "Running", "restarts": 1}
  ]
}`},{method:`GET`,path:`/api/v1/deployment/deployments`,title:`Deployment 列表`,category:`部署`,description:`获取所有 Deployment 的副本状态`,responseExample:`{
  "deployments": [
    {"name": "nginx", "namespace": "default", "ready": "3/3", "updated": 3},
    {"name": "api-server", "namespace": "backend", "ready": "5/5", "updated": 5}
  ]
}`},{method:`GET`,path:`/api/v1/deployment/events`,title:`部署事件`,category:`部署`,description:`获取 Kubernetes 事件流（Warning/Error 优先）`,responseExample:`{
  "events": [
    {"type": "Warning", "reason": "BackOff", "message": "Back-off restarting failed container"},
    {"type": "Normal", "reason": "Pulled", "message": "Successfully pulled image"}
  ]
}`},{method:`GET`,path:`/api/v1/deployment/namespaces`,title:`命名空间`,category:`部署`,description:`获取所有 Kubernetes 命名空间`,responseExample:`{
  "namespaces": [
    {"name": "default", "status": "Active"},
    {"name": "kube-system", "status": "Active"},
    {"name": "monitoring", "status": "Active"}
  ]
}`},{method:`GET`,path:`/api/v1/deployment/services`,title:`Service 列表`,category:`部署`,description:`获取所有 Kubernetes Service`,responseExample:`{
  "services": [
    {"name": "nginx-svc", "type": "ClusterIP", "cluster_ip": "10.96.0.100", "ports": "80/TCP"},
    {"name": "api-svc", "type": "NodePort", "cluster_ip": "10.96.0.101", "ports": "8080:30080"}
  ]
}`},{method:`POST`,path:`/api/v1/deployment/scale`,title:`副本伸缩`,category:`部署`,description:`调整 Deployment 副本数量`,params:[{name:`deployment`,type:`string`,required:!0,desc:`Deployment 名称`},{name:`replicas`,type:`integer`,required:!0,desc:`目标副本数`},{name:`namespace`,type:`string`,required:!1,desc:`命名空间，默认 default`}],requestExample:`{
  "deployment": "nginx",
  "replicas": 5,
  "namespace": "default"
}`,responseExample:`{
  "status": "scaling",
  "from": 3,
  "to": 5
}`},{method:`GET`,path:`/api/v1/environments`,title:`环境列表`,category:`环境`,description:`获取所有已注册的运维环境（支持 18 种拓扑类型）`,responseExample:`{
  "environments": [
    {"id": "env-001", "name": "汽车制造 MES", "type": "混合云", "industry": "制造"},
    {"id": "env-002", "name": "医疗 HIS 系统", "type": "纯本地虚拟化", "industry": "医疗"}
  ],
  "total": 18
}`},{method:`GET`,path:`/api/v1/environments/summary`,title:`环境概览`,category:`环境`,description:`获取环境拓扑类型分布统计`,responseExample:`{
  "total": 18,
  "by_type": {"混合云": 4, "纯本地虚拟化": 3, "纯公有云": 3, "多云": 2},
  "by_industry": {"制造": 2, "医疗": 1, "金融": 2}
}`},{method:`GET`,path:`/api/v1/environments/topology`,title:`网络拓扑`,category:`环境`,description:`获取环境网络拓扑图数据`,responseExample:`{
  "nodes": [
    {"id": "dc-1", "label": "北京数据中心", "type": "datacenter"},
    {"id": "cloud-1", "label": "阿里云华东", "type": "cloud"}
  ],
  "edges": [
    {"source": "dc-1", "target": "cloud-1", "label": "VPN 1Gbps"}
  ]
}`},{method:`GET`,path:`/api/v1/environments/{id}`,title:`环境详情`,category:`环境`,description:`获取单个环境的完整信息`,responseExample:`{
  "id": "env-001",
  "name": "汽车制造 MES",
  "type": "混合云(容器+云)",
  "industry": "汽车制造",
  "nodes": [...],
  "cloud_accounts": [...]
}`},{method:`POST`,path:`/api/v1/discovery`,title:`环境发现`,category:`发现`,description:`自动探测目标环境，识别操作系统、容器、中间件、数据库等 10 大类`,params:[{name:`host`,type:`string`,required:!0,desc:`目标主机 IP`},{name:`port`,type:`integer`,required:!1,desc:`SSH 端口，默认 22`}],requestExample:`{
  "host": "10.0.0.1",
  "port": 22
}`,responseExample:`{
  "host": "10.0.0.1",
  "os": "Ubuntu 22.04",
  "containers": ["docker", "k8s-node"],
  "middleware": ["nginx", "redis"],
  "databases": ["mysql 8.0"],
  "recommended_topology": "混合云(容器+云)",
  "suggested_agents": ["linux", "kubernetes", "docker"]
}`},{method:`GET`,path:`/api/v1/slo`,title:`SLO 数据`,category:`SLO`,description:`获取服务等级目标（SLO）数据，包括可用性和延迟指标`,responseExample:`{
  "services": [
    {"name": "api-gateway", "availability": 99.97, "target": 99.95, "status": "on_track"},
    {"name": "order-service", "availability": 99.82, "target": 99.90, "status": "at_risk"}
  ]
}`},{method:`GET`,path:`/api/v1/events`,title:`事件列表`,category:`事件`,description:`获取事件总线中的事件流，支持按级别筛选`,responseExample:`{
  "events": [
    {"id": "evt-001", "level": "error", "title": "CPU 超阈值", "source": "agent:linux", "time": "2026-07-04T10:30:00Z"},
    {"id": "evt-002", "level": "warning", "title": "磁盘空间不足", "source": "tool:disk_usage"}
  ]
}`},{method:`GET`,path:`/api/v1/network/connections`,title:`网络连接`,category:`网络`,description:`获取环境间网络连接和链路状态`,responseExample:`{
  "connections": [
    {"from": "北京 DC", "to": "阿里云华东", "type": "VPN", "bandwidth": "1Gbps", "latency": "12ms"},
    {"from": "上海 DC", "to": "腾讯云华南", "type": "专线", "bandwidth": "10Gbps", "latency": "3ms"}
  ]
}`},{method:`GET`,path:`/api/v1/multicloud`,title:`多云概览`,category:`多云`,description:`获取多云环境下的账户、费用和资源概览`,responseExample:`{
  "accounts": [
    {"provider": "阿里云", "region": "华东", "monthly_cost": 12500, "resources": 48},
    {"provider": "腾讯云", "region": "华南", "monthly_cost": 8300, "resources": 32}
  ],
  "total_monthly_cost": 20800
}`},{method:`GET`,path:`/api/v1/audit`,title:`审计日志`,category:`审计`,description:`获取运维操作审计日志`,responseExample:`{
  "logs": [
    {"user": "admin", "action": "tool:ssh_exec", "target": "10.0.0.1", "time": "2026-07-04T10:15:00Z", "result": "success"},
    {"user": "ops", "action": "workflow:deploy-canary", "target": "k8s-cluster", "result": "success"}
  ]
}`},{method:`GET`,path:`/api/v1/cost/summary`,title:`成本概览`,category:`成本`,description:`获取各云厂商/环境的成本汇总和趋势`,responseExample:`{
  "total_monthly": 45200,
  "by_provider": {"阿里云": 18500, "华为云": 15200, "腾讯云": 11500},
  "trend": "down_5_percent"
}`},{method:`GET`,path:`/api/v1/security/summary`,title:`安全态势`,category:`安全`,description:`获取安全态势整体概览，包括漏洞和合规状态`,responseExample:`{
  "total_vulnerabilities": 23,
  "critical": 2, "high": 5, "medium": 11, "low": 5,
  "compliance_score": 87,
  "last_scan": "2026-07-04T08:00:00Z"
}`}],o={GET:`#22c55e`,POST:`#3b82f6`,PUT:`#f59e0b`,DELETE:`#ef4444`},s={GET:`rgba(34,197,94,0.15)`,POST:`rgba(59,130,246,0.15)`,PUT:`rgba(245,158,11,0.15)`,DELETE:`rgba(239,68,68,0.15)`};function c(){let[e,t]=(0,r.useState)(null),[n,c]=(0,r.useState)(`全部`),l=[`全部`,...Array.from(new Set(a.map(e=>e.category)))],u=n===`全部`?a:a.filter(e=>e.category===n);return(0,i.jsxs)(`div`,{children:[(0,i.jsxs)(`div`,{style:{display:`flex`,justifyContent:`space-between`,alignItems:`center`,marginBottom:24},children:[(0,i.jsxs)(`div`,{children:[(0,i.jsx)(`h2`,{style:{fontSize:24,fontWeight:700,marginBottom:4},children:`📖 API 文档`}),(0,i.jsxs)(`p`,{style:{fontSize:14,color:`#64748b`},children:[`REST API · Base URL: http://localhost:8000/api/v1 · Bearer Token 认证 · `,a.length,` 个端点`]})]}),(0,i.jsx)(`a`,{href:`https://gitee.com/neal4752/agentic-aiops/blob/main/docs/api.md`,target:`_blank`,rel:`noreferrer`,style:{padding:`8px 16px`,background:`rgba(59,130,246,0.15)`,border:`1px solid rgba(59,130,246,0.3)`,borderRadius:8,color:`#3b82f6`,fontSize:13,textDecoration:`none`},children:`📄 完整 Markdown 文档`})]}),(0,i.jsx)(`div`,{style:{display:`flex`,gap:8,marginBottom:20,flexWrap:`wrap`},children:l.map(e=>(0,i.jsxs)(`button`,{onClick:()=>c(e),style:{padding:`6px 14px`,borderRadius:6,border:`1px solid`,fontSize:13,cursor:`pointer`,background:n===e?`rgba(59,130,246,0.2)`:`transparent`,borderColor:n===e?`#3b82f6`:`rgba(59,130,246,0.2)`,color:n===e?`#3b82f6`:`#94a3b8`},children:[e,` (`,e===`全部`?a.length:a.filter(t=>t.category===e).length,`)`]},e))}),(0,i.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:8},children:u.map(n=>{let r=e===`${n.method}-${n.path}`;return(0,i.jsxs)(`div`,{style:{background:`rgba(15,23,42,0.6)`,border:`1px solid rgba(59,130,246,0.12)`,borderRadius:10,overflow:`hidden`,cursor:`pointer`},onClick:()=>t(r?null:`${n.method}-${n.path}`),children:[(0,i.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:12,padding:`14px 18px`},children:[(0,i.jsx)(`span`,{style:{background:s[n.method],color:o[n.method],padding:`3px 10px`,borderRadius:5,fontSize:12,fontWeight:700,fontFamily:`monospace`,minWidth:60,textAlign:`center`},children:n.method}),(0,i.jsx)(`code`,{style:{color:`#e2e8f0`,fontSize:14,fontFamily:`monospace`,flex:1},children:n.path}),(0,i.jsx)(`span`,{style:{color:`#94a3b8`,fontSize:13},children:n.title}),(0,i.jsx)(`span`,{style:{color:`#475569`,fontSize:12},children:r?`▲`:`▼`})]}),r&&(0,i.jsxs)(`div`,{style:{padding:`0 18px 18px`,borderTop:`1px solid rgba(59,130,246,0.1)`},children:[(0,i.jsx)(`p`,{style:{color:`#94a3b8`,fontSize:13,margin:`14px 0`},children:n.description}),n.params&&n.params.length>0&&(0,i.jsxs)(`div`,{style:{marginBottom:16},children:[(0,i.jsx)(`h4`,{style:{color:`#e2e8f0`,fontSize:13,marginBottom:8},children:`参数`}),(0,i.jsx)(`div`,{style:{background:`rgba(30,41,59,0.5)`,borderRadius:8,overflow:`hidden`},children:(0,i.jsxs)(`table`,{style:{width:`100%`,borderCollapse:`collapse`,fontSize:13},children:[(0,i.jsx)(`thead`,{children:(0,i.jsxs)(`tr`,{style:{background:`rgba(59,130,246,0.08)`},children:[(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`8px 12px`,color:`#64748b`,fontWeight:500},children:`名称`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`8px 12px`,color:`#64748b`,fontWeight:500},children:`类型`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`8px 12px`,color:`#64748b`,fontWeight:500},children:`必填`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`8px 12px`,color:`#64748b`,fontWeight:500},children:`说明`})]})}),(0,i.jsx)(`tbody`,{children:n.params.map(e=>(0,i.jsxs)(`tr`,{style:{borderTop:`1px solid rgba(59,130,246,0.08)`},children:[(0,i.jsx)(`td`,{style:{padding:`8px 12px`,color:`#e2e8f0`,fontFamily:`monospace`},children:e.name}),(0,i.jsx)(`td`,{style:{padding:`8px 12px`,color:`#8b5cf6`},children:e.type}),(0,i.jsx)(`td`,{style:{padding:`8px 12px`},children:e.required?(0,i.jsx)(`span`,{style:{color:`#ef4444`,fontSize:11},children:`必填`}):(0,i.jsx)(`span`,{style:{color:`#475569`},children:`可选`})}),(0,i.jsx)(`td`,{style:{padding:`8px 12px`,color:`#94a3b8`},children:e.desc})]},e.name))})]})})]}),(0,i.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:n.requestExample?`1fr 1fr`:`1fr`,gap:12},children:[n.requestExample&&(0,i.jsxs)(`div`,{children:[(0,i.jsx)(`h4`,{style:{color:`#22c55e`,fontSize:12,marginBottom:6},children:`📝 请求示例`}),(0,i.jsx)(`pre`,{style:{background:`rgba(30,41,59,0.7)`,border:`1px solid rgba(34,197,94,0.15)`,borderRadius:8,padding:14,color:`#94a3b8`,fontSize:12,fontFamily:`monospace`,overflow:`auto`,margin:0},children:n.requestExample})]}),n.responseExample&&(0,i.jsxs)(`div`,{children:[(0,i.jsx)(`h4`,{style:{color:`#3b82f6`,fontSize:12,marginBottom:6},children:`📤 响应示例`}),(0,i.jsx)(`pre`,{style:{background:`rgba(30,41,59,0.7)`,border:`1px solid rgba(59,130,246,0.15)`,borderRadius:8,padding:14,color:`#94a3b8`,fontSize:12,fontFamily:`monospace`,overflow:`auto`,margin:0},children:n.responseExample})]})]}),(0,i.jsxs)(`div`,{style:{marginTop:12},children:[(0,i.jsx)(`h4`,{style:{color:`#f59e0b`,fontSize:12,marginBottom:6},children:`⚡ curl 测试`}),(0,i.jsx)(`pre`,{style:{background:`rgba(30,41,59,0.7)`,border:`1px solid rgba(245,158,11,0.15)`,borderRadius:8,padding:14,color:`#f59e0b`,fontSize:12,fontFamily:`monospace`,overflow:`auto`,margin:0},children:n.method===`GET`?`curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000${n.path}`:`curl -X ${n.method} -H "Authorization: Bearer <TOKEN>" \\\n  -H "Content-Type: application/json" \\\n  -d '${n.requestExample||`{}`}' \\\n  http://localhost:8000${n.path}`})]})]})]},`${n.method}-${n.path}`)})}),(0,i.jsxs)(`div`,{style:{marginTop:32,background:`rgba(15,23,42,0.6)`,border:`1px solid rgba(59,130,246,0.12)`,borderRadius:12,padding:20},children:[(0,i.jsx)(`h3`,{style:{color:`#e2e8f0`,fontSize:16,marginBottom:16},children:`❌ 错误码`}),(0,i.jsxs)(`table`,{style:{width:`100%`,borderCollapse:`collapse`,fontSize:13},children:[(0,i.jsx)(`thead`,{children:(0,i.jsxs)(`tr`,{style:{background:`rgba(59,130,246,0.08)`},children:[(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`10px 14px`,color:`#64748b`,fontWeight:500},children:`HTTP 状态码`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`10px 14px`,color:`#64748b`,fontWeight:500},children:`错误码`}),(0,i.jsx)(`th`,{style:{textAlign:`left`,padding:`10px 14px`,color:`#64748b`,fontWeight:500},children:`说明`})]})}),(0,i.jsx)(`tbody`,{children:[[`400`,`INVALID_REQUEST`,`请求参数错误`],[`401`,`UNAUTHORIZED`,`未认证或 Token 无效`],[`403`,`FORBIDDEN`,`权限不足`],[`404`,`NOT_FOUND`,`资源不存在`],[`429`,`RATE_LIMITED`,`请求频率超限`],[`500`,`INTERNAL_ERROR`,`服务器内部错误`]].map(([e,t,n])=>(0,i.jsxs)(`tr`,{style:{borderTop:`1px solid rgba(59,130,246,0.08)`},children:[(0,i.jsx)(`td`,{style:{padding:`10px 14px`,color:`#e2e8f0`,fontFamily:`monospace`},children:e}),(0,i.jsx)(`td`,{style:{padding:`10px 14px`,color:`#8b5cf6`,fontFamily:`monospace`},children:t}),(0,i.jsx)(`td`,{style:{padding:`10px 14px`,color:`#94a3b8`},children:n})]},e))})]})]})]})}export{c as default};