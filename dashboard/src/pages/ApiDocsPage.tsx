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
    responseExample: '{\n  "status": "healthy",\n  "version": "5.3.0"\n}'
  },
  {
    method: 'GET', path: '/api/v1/version', title: '版本信息', category: '基础',
    description: '获取当前系统版本和运行环境信息',
    responseExample: '{\n  "version": "5.3.0",\n  "python": "3.12.3",\n  "tools": 157,\n  "agents": 21\n}'
  },
  {
    method: 'POST', path: '/api/v1/diagnose', title: '执行诊断', category: '诊断',
    description: '执行完整诊断任务，自动选择合适的 Agent 分析问题根因',
    params: [
      { name: 'host', type: 'string', required: true, desc: '目标主机 IP' },
      { name: 'symptom', type: 'string', required: false, desc: '症状描述' },
      { name: 'agent', type: 'string', required: false, desc: '指定 Agent（linux/k8s/db 等）' },
      { name: 'timeout', type: 'integer', required: false, desc: '超时秒数，默认 60' },
    ],
    requestExample: '{\n  "host": "10.0.0.1",\n  "symptom": "CPU 持续高于 90%",\n  "agent": "linux"\n}',
    responseExample: '{\n  "status": "completed",\n  "root_cause": "Java Full GC 频繁",\n  "confidence": 0.94,\n  "suggestion": "增大 JVM 堆内存至 4G"\n}'
  },
  {
    method: 'GET', path: '/api/v1/agents', title: '列出智能体', category: '智能体',
    description: '列出所有 21 个可用智能体及其运行状态',
    responseExample: '{\n  "agents": [\n    {"name": "linux", "status": "ready"},\n    {"name": "kubernetes", "status": "ready"},\n    {"name": "database", "status": "ready"}\n  ],\n  "total": 21\n}'
  },
  {
    method: 'GET', path: '/api/v1/agents/{agent}', title: '智能体详情', category: '智能体',
    description: '获取指定智能体的详细信息，包括工具列表和执行统计',
    responseExample: '{\n  "name": "linux",\n  "status": "ready",\n  "tools": ["ssh_exec", "system_info", "process_list"],\n  "stats": {"total_tasks": 1247, "success_rate": 0.94}\n}'
  },
  {
    method: 'POST', path: '/api/v1/agents/{agent}/run', title: '运行智能体', category: '智能体',
    description: '运行指定智能体执行诊断或运维任务',
    params: [
      { name: 'task', type: 'string', required: true, desc: '任务描述' },
      { name: 'context', type: 'object', required: false, desc: '上下文信息' },
      { name: 'timeout', type: 'integer', required: false, desc: '超时秒数' },
    ],
    requestExample: '{\n  "task": "检查 CPU 使用情况并分析 top 进程",\n  "timeout": 60\n}',
    responseExample: '{\n  "status": "completed",\n  "result": {"answer": "CPU 23%，top 进程为 java(12%)"}\n}'
  },
  {
    method: 'GET', path: '/api/v1/tools', title: '列出工具', category: '工具',
    description: '列出所有 157 个可用 MCP 工具，支持按类别筛选',
    responseExample: '{\n  "tools": [\n    {"name": "ssh_exec", "category": "system"},\n    {"name": "mysql_query", "category": "database"},\n    {"name": "prometheus_query", "category": "monitoring"}\n  ],\n  "total": 157\n}'
  },
  {
    method: 'POST', path: '/api/v1/tools/execute', title: '执行工具', category: '工具',
    description: '直接执行指定工具，返回执行结果',
    params: [
      { name: 'tool', type: 'string', required: true, desc: '工具名称' },
      { name: 'params', type: 'object', required: true, desc: '工具参数' },
    ],
    requestExample: '{\n  "tool": "ssh_exec",\n  "params": {"host": "10.0.0.1", "command": "df -h"}\n}',
    responseExample: '{\n  "tool": "ssh_exec",\n  "result": {"output": "Filesystem  Size  Used", "exit_code": 0}\n}'
  },
  {
    method: 'POST', path: '/api/v1/workflow/run', title: '运行工作流', category: '工作流',
    description: '运行指定的自动化工作流，支持 10 条预置企业工作流',
    params: [
      { name: 'workflow', type: 'string', required: true, desc: '工作流名称' },
      { name: 'variables', type: 'object', required: false, desc: '工作流变量' },
    ],
    requestExample: '{\n  "workflow": "cpu-high-diagnosis",\n  "variables": {"host": "10.0.0.1"}\n}',
    responseExample: '{\n  "run_id": "run_xyz789",\n  "status": "started"\n}'
  },
  {
    method: 'GET', path: '/api/v1/workflows', title: '列出工作流', category: '工作流',
    description: '获取所有可用工作流列表及其执行状态',
    responseExample: '{\n  "workflows": [\n    {"name": "cpu-high-diagnosis", "steps": 4},\n    {"name": "deploy-canary", "steps": 6},\n    {"name": "security-incident-response", "steps": 8}\n  ]\n}'
  },
  {
    method: 'POST', path: '/api/v1/approval/create', title: '创建审批', category: '审批',
    description: '创建审批请求，用于高风险运维操作的审批流程',
    params: [
      { name: 'title', type: 'string', required: true, desc: '审批标题' },
      { name: 'command', type: 'string', required: true, desc: '待执行命令' },
      { name: 'risk_level', type: 'string', required: false, desc: 'low/medium/high' },
    ],
    requestExample: '{\n  "title": "重启 Nginx",\n  "command": "systemctl restart nginx",\n  "risk_level": "low"\n}',
    responseExample: '{\n  "request_id": "apr_003",\n  "status": "pending"\n}'
  },
  {
    method: 'GET', path: '/api/v1/monitoring/summary', title: '监控概览', category: '监控',
    description: '获取监控系统整体概览，包括 Prometheus/Loki/SkyWalking 状态',
    responseExample: '{\n  "healthy_targets": 47,\n  "total_targets": 52,\n  "active_alerts": 3,\n  "data_sources": ["prometheus", "loki", "skywalking"]\n}'
  },
  {
    method: 'GET', path: '/api/v1/monitoring/metrics', title: '监控指标', category: '监控',
    description: '获取实时系统指标（CPU/内存/磁盘/网络）',
    responseExample: '{\n  "cpu_usage": 45.2,\n  "memory_usage": 68.7,\n  "disk_usage": 52.1,\n  "network_in": "125 MB/s",\n  "network_out": "89 MB/s"\n}'
  },
  {
    method: 'GET', path: '/api/v1/monitoring/alerts', title: '监控告警', category: '监控',
    description: '获取当前活跃的监控告警列表',
    responseExample: '{\n  "alerts": [\n    {"name": "HighCPU", "severity": "warning", "instance": "10.0.0.1"},\n    {"name": "DiskFull", "severity": "critical", "instance": "10.0.0.3"}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/monitoring/targets', title: '监控目标', category: '监控',
    description: '获取所有监控目标（Exporter/Agent）的在线状态',
    responseExample: '{\n  "targets": [\n    {"job": "node_exporter", "instance": "10.0.0.1:9100", "up": true},\n    {"job": "mysql_exporter", "instance": "10.0.0.2:9104", "up": true}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/deployment/summary', title: '部署概览', category: '部署',
    description: '获取 Kubernetes 部署整体概览',
    responseExample: '{\n  "total_pods": 48,\n  "running": 45,\n  "pending": 2,\n  "failed": 1,\n  "namespaces": 6\n}'
  },
  {
    method: 'GET', path: '/api/v1/deployment/nodes', title: '集群节点', category: '部署',
    description: '获取 Kubernetes 集群节点状态',
    responseExample: '{\n  "nodes": [\n    {"name": "node-1", "status": "Ready", "cpu": "4/8", "memory": "12/32Gi"},\n    {"name": "node-2", "status": "Ready", "cpu": "3/8", "memory": "15/32Gi"}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/deployment/pods', title: 'Pod 列表', category: '部署',
    description: '获取所有 Pod 的运行状态',
    responseExample: '{\n  "pods": [\n    {"name": "nginx-abc123", "namespace": "default", "status": "Running", "restarts": 0},\n    {"name": "redis-def456", "namespace": "middleware", "status": "Running", "restarts": 1}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/deployment/deployments', title: 'Deployment 列表', category: '部署',
    description: '获取所有 Deployment 的副本状态',
    responseExample: '{\n  "deployments": [\n    {"name": "nginx", "namespace": "default", "ready": "3/3", "updated": 3},\n    {"name": "api-server", "namespace": "backend", "ready": "5/5", "updated": 5}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/deployment/events', title: '部署事件', category: '部署',
    description: '获取 Kubernetes 事件流（Warning/Error 优先）',
    responseExample: '{\n  "events": [\n    {"type": "Warning", "reason": "BackOff", "message": "Back-off restarting failed container"},\n    {"type": "Normal", "reason": "Pulled", "message": "Successfully pulled image"}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/deployment/namespaces', title: '命名空间', category: '部署',
    description: '获取所有 Kubernetes 命名空间',
    responseExample: '{\n  "namespaces": [\n    {"name": "default", "status": "Active"},\n    {"name": "kube-system", "status": "Active"},\n    {"name": "monitoring", "status": "Active"}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/deployment/services', title: 'Service 列表', category: '部署',
    description: '获取所有 Kubernetes Service',
    responseExample: '{\n  "services": [\n    {"name": "nginx-svc", "type": "ClusterIP", "cluster_ip": "10.96.0.100", "ports": "80/TCP"},\n    {"name": "api-svc", "type": "NodePort", "cluster_ip": "10.96.0.101", "ports": "8080:30080"}\n  ]\n}'
  },
  {
    method: 'POST', path: '/api/v1/deployment/scale', title: '副本伸缩', category: '部署',
    description: '调整 Deployment 副本数量',
    params: [
      { name: 'deployment', type: 'string', required: true, desc: 'Deployment 名称' },
      { name: 'replicas', type: 'integer', required: true, desc: '目标副本数' },
      { name: 'namespace', type: 'string', required: false, desc: '命名空间，默认 default' },
    ],
    requestExample: '{\n  "deployment": "nginx",\n  "replicas": 5,\n  "namespace": "default"\n}',
    responseExample: '{\n  "status": "scaling",\n  "from": 3,\n  "to": 5\n}'
  },
  {
    method: 'GET', path: '/api/v1/environments', title: '环境列表', category: '环境',
    description: '获取所有已注册的运维环境（支持 18 种拓扑类型）',
    responseExample: '{\n  "environments": [\n    {"id": "env-001", "name": "汽车制造 MES", "type": "混合云", "industry": "制造"},\n    {"id": "env-002", "name": "医疗 HIS 系统", "type": "纯本地虚拟化", "industry": "医疗"}\n  ],\n  "total": 18\n}'
  },
  {
    method: 'GET', path: '/api/v1/environments/summary', title: '环境概览', category: '环境',
    description: '获取环境拓扑类型分布统计',
    responseExample: '{\n  "total": 18,\n  "by_type": {"混合云": 4, "纯本地虚拟化": 3, "纯公有云": 3, "多云": 2},\n  "by_industry": {"制造": 2, "医疗": 1, "金融": 2}\n}'
  },
  {
    method: 'GET', path: '/api/v1/environments/topology', title: '网络拓扑', category: '环境',
    description: '获取环境网络拓扑图数据',
    responseExample: '{\n  "nodes": [\n    {"id": "dc-1", "label": "北京数据中心", "type": "datacenter"},\n    {"id": "cloud-1", "label": "阿里云华东", "type": "cloud"}\n  ],\n  "edges": [\n    {"source": "dc-1", "target": "cloud-1", "label": "VPN 1Gbps"}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/environments/{id}', title: '环境详情', category: '环境',
    description: '获取单个环境的完整信息',
    responseExample: '{\n  "id": "env-001",\n  "name": "汽车制造 MES",\n  "type": "混合云(容器+云)",\n  "industry": "汽车制造",\n  "nodes": [...],\n  "cloud_accounts": [...]\n}'
  },
  {
    method: 'POST', path: '/api/v1/discovery', title: '环境发现', category: '发现',
    description: '自动探测目标环境，识别操作系统、容器、中间件、数据库等 10 大类',
    params: [
      { name: 'host', type: 'string', required: true, desc: '目标主机 IP' },
      { name: 'port', type: 'integer', required: false, desc: 'SSH 端口，默认 22' },
    ],
    requestExample: '{\n  "host": "10.0.0.1",\n  "port": 22\n}',
    responseExample: '{\n  "host": "10.0.0.1",\n  "os": "Ubuntu 22.04",\n  "containers": ["docker", "k8s-node"],\n  "middleware": ["nginx", "redis"],\n  "databases": ["mysql 8.0"],\n  "recommended_topology": "混合云(容器+云)",\n  "suggested_agents": ["linux", "kubernetes", "docker"]\n}'
  },
  {
    method: 'GET', path: '/api/v1/slo', title: 'SLO 数据', category: 'SLO',
    description: '获取服务等级目标（SLO）数据，包括可用性和延迟指标',
    responseExample: '{\n  "services": [\n    {"name": "api-gateway", "availability": 99.97, "target": 99.95, "status": "on_track"},\n    {"name": "order-service", "availability": 99.82, "target": 99.90, "status": "at_risk"}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/events', title: '事件列表', category: '事件',
    description: '获取事件总线中的事件流，支持按级别筛选',
    responseExample: '{\n  "events": [\n    {"id": "evt-001", "level": "error", "title": "CPU 超阈值", "source": "agent:linux", "time": "2026-07-04T10:30:00Z"},\n    {"id": "evt-002", "level": "warning", "title": "磁盘空间不足", "source": "tool:disk_usage"}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/network/connections', title: '网络连接', category: '网络',
    description: '获取环境间网络连接和链路状态',
    responseExample: '{\n  "connections": [\n    {"from": "北京 DC", "to": "阿里云华东", "type": "VPN", "bandwidth": "1Gbps", "latency": "12ms"},\n    {"from": "上海 DC", "to": "腾讯云华南", "type": "专线", "bandwidth": "10Gbps", "latency": "3ms"}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/multicloud', title: '多云概览', category: '多云',
    description: '获取多云环境下的账户、费用和资源概览',
    responseExample: '{\n  "accounts": [\n    {"provider": "阿里云", "region": "华东", "monthly_cost": 12500, "resources": 48},\n    {"provider": "腾讯云", "region": "华南", "monthly_cost": 8300, "resources": 32}\n  ],\n  "total_monthly_cost": 20800\n}'
  },
  {
    method: 'GET', path: '/api/v1/audit', title: '审计日志', category: '审计',
    description: '获取运维操作审计日志',
    responseExample: '{\n  "logs": [\n    {"user": "admin", "action": "tool:ssh_exec", "target": "10.0.0.1", "time": "2026-07-04T10:15:00Z", "result": "success"},\n    {"user": "ops", "action": "workflow:deploy-canary", "target": "k8s-cluster", "result": "success"}\n  ]\n}'
  },
  {
    method: 'GET', path: '/api/v1/cost/summary', title: '成本概览', category: '成本',
    description: '获取各云厂商/环境的成本汇总和趋势',
    responseExample: '{\n  "total_monthly": 45200,\n  "by_provider": {"阿里云": 18500, "华为云": 15200, "腾讯云": 11500},\n  "trend": "down_5_percent"\n}'
  },
  {
    method: 'GET', path: '/api/v1/security/summary', title: '安全态势', category: '安全',
    description: '获取安全态势整体概览，包括漏洞和合规状态',
    responseExample: '{\n  "total_vulnerabilities": 23,\n  "critical": 2, "high": 5, "medium": 11, "low": 5,\n  "compliance_score": 87,\n  "last_scan": "2026-07-04T08:00:00Z"\n}'
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
          <p style={{fontSize:14,color:'#64748b'}}>REST API · Base URL: http://localhost:8000/api/v1 · Bearer Token 认证 · {endpoints.length} 个端点</p>
        </div>
        <a href="https://gitee.com/neal4752/agentic-aiops/blob/main/docs/api.md"
           target="_blank" rel="noreferrer"
           style={{padding:'8px 16px',background:'rgba(59,130,246,0.15)',border:'1px solid rgba(59,130,246,0.3)',borderRadius:8,color:'#3b82f6',fontSize:13,textDecoration:'none'}}>
          📄 完整 Markdown 文档
        </a>
      </div>

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

      <div style={{display:'flex',flexDirection:'column',gap:8}}>
        {filtered.map(ep => {
          const isOpen = expanded === `${ep.method}-${ep.path}`;
          return (
            <div key={`${ep.method}-${ep.path}`}
              style={{background:'rgba(15,23,42,0.6)',border:'1px solid rgba(59,130,246,0.12)',borderRadius:10,overflow:'hidden',cursor:'pointer'}}
              onClick={() => setExpanded(isOpen ? null : `${ep.method}-${ep.path}`)}>
              <div style={{display:'flex',alignItems:'center',gap:12,padding:'14px 18px'}}>
                <span style={{background:methodBg[ep.method],color:methodColors[ep.method],padding:'3px 10px',borderRadius:5,fontSize:12,fontWeight:700,fontFamily:'monospace',minWidth:60,textAlign:'center'}}>
                  {ep.method}
                </span>
                <code style={{color:'#e2e8f0',fontSize:14,fontFamily:'monospace',flex:1}}>{ep.path}</code>
                <span style={{color:'#94a3b8',fontSize:13}}>{ep.title}</span>
                <span style={{color:'#475569',fontSize:12}}>{isOpen ? '▲' : '▼'}</span>
              </div>

              {isOpen && (
                <div style={{padding:'0 18px 18px',borderTop:'1px solid rgba(59,130,246,0.1)'}}>
                  <p style={{color:'#94a3b8',fontSize:13,margin:'14px 0'}}>{ep.description}</p>

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
