import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { agents, toolCategories } from '../data/agents';
import { demoAgentData, demoConnections, type AgentData } from '../api';

// ══════════════════════════════════════════
// 仪表盘 — 平台介绍 + 分页展示
// Tab: 平台概览 | 使用指南 | Agent网络 | 智能体&工具
// ══════════════════════════════════════════

type Tab = 'overview' | 'guide' | 'network' | 'agents';

const tabConfig: { key: Tab; label: string; icon: string }[] = [
  { key: 'overview', label: '平台概览', icon: '📊' },
  { key: 'guide', label: '使用指南', icon: '📖' },
  { key: 'network', label: 'Agent 网络', icon: '🕸️' },
  { key: 'agents', label: '智能体 & 工具', icon: '🤖' },
];

// ══════════════════════════════════════════
// Tab 1: 平台概览
// ══════════════════════════════════════════

function OverviewTab({ navigate }: { navigate: any }) {
  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      {/* Hero */}
      <div className="card" style={{
        padding: '32px 36px', marginBottom: 24,
        background: 'linear-gradient(135deg, rgba(59,130,246,0.08), rgba(139,92,246,0.08), rgba(6,182,212,0.06))',
        border: '1px solid rgba(59,130,246,0.15)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 20, marginBottom: 20 }}>
          <div style={{ fontSize: 48 }}>🤖</div>
          <div>
            <h1 style={{ fontSize: 28, fontWeight: 800, margin: 0, background: 'linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Agentic AIOps
            </h1>
            <p style={{ fontSize: 14, color: 'var(--text-secondary)', margin: '4px 0 0' }}>
              AI-Native Intelligent Operations Platform
            </p>
          </div>
        </div>
        <p style={{ fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.8, maxWidth: 800 }}>
          一个<strong style={{ color: 'var(--text-primary)' }}>AI 驱动的智能运维平台</strong>，通过 21 个专业 Agent 和 148+ MCP 工具，
          自动完成监控、告警、部署、安全、成本优化等运维工作。支持 Linux / Windows / K8s / Docker / 多云 / 混合云 / 信创全栈。
        </p>
      </div>

      {/* 核心能力 */}
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>🎯 核心能力</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 14 }}>
          {[
            { icon: '🔍', title: '环境发现', desc: '自动探测服务器硬件、OS、容器、中间件、数据库，智能推荐 Agent 组合', color: '#3b82f6' },
            { icon: '📊', title: '实时监控', desc: 'CPU / 内存 / 磁盘 / 网络，接入 Prometheus、Grafana、SkyWalking', color: '#10b981' },
            { icon: '🚨', title: '智能告警', desc: '分级告警（Critical / Warning / Info），自动关联根因，推送修复建议', color: '#ef4444' },
            { icon: '🚀', title: '自动部署', desc: 'K8s 滚动更新、灰度发布、一键回滚，支持 ArgoCD / Jenkins / Helm', color: '#8b5cf6' },
            { icon: '🔒', title: '安全合规', desc: '漏洞扫描（Trivy）、等保检查、配置审计、证书管理', color: '#ec4899' },
            { icon: '💰', title: '成本优化', desc: '多云费用分析、资源利用率、优化建议，支持 Kubecost / Infracost', color: '#f59e0b' },
          ].map(item => (
            <div key={item.title} className="card" style={{ padding: '18px 20px', borderLeft: '3px solid ' + item.color }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                <span style={{ fontSize: 24 }}>{item.icon}</span>
                <span style={{ fontSize: 14, fontWeight: 700, color: item.color }}>{item.title}</span>
              </div>
              <p style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>{item.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* 平台指标 */}
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>📈 平台规模</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 12 }}>
          {[
            { label: '智能体', value: '21+', icon: '🤖', color: '#3b82f6' },
            { label: 'MCP 工具', value: '148+', icon: '🔌', color: '#8b5cf6' },
            { label: '环境拓扑', value: '18 种', icon: '🏗️', color: '#06b6d4' },
            { label: 'Dashboard 页面', value: '16', icon: '📊', color: '#10b981' },
            { label: '支持平台', value: '全栈', icon: '🌐', color: '#f97316' },
            { label: '开源协议', value: 'MIT', icon: '📜', color: '#64748b' },
          ].map(item => (
            <div key={item.label} className="card" style={{ padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: 24, marginBottom: 6 }}>{item.icon}</div>
              <div style={{ fontSize: 22, fontWeight: 800, color: item.color }}>{item.value}</div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>{item.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* 快速入口 */}
      <div>
        <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>⚡ 快速入口</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 10 }}>
          {[
            { icon: '🔍', label: '环境发现', path: '/environments', color: '#3b82f6' },
            { icon: '📊', label: '实时监控', path: '/monitoring', color: '#10b981' },
            { icon: '🚨', label: '告警中心', path: '/alerts', color: '#ef4444' },
            { icon: '🚀', label: '部署管理', path: '/deployment', color: '#8b5cf6' },
            { icon: '💰', label: '成本分析', path: '/cost', color: '#f59e0b' },
            { icon: '🔒', label: '安全态势', path: '/security', color: '#ec4899' },
          ].map(item => (
            <button key={item.path} onClick={() => navigate(item.path)} style={{
              padding: '16px 12px', borderRadius: 10, border: '1px solid ' + item.color + '25',
              background: item.color + '08', cursor: 'pointer', textAlign: 'center',
            }}
              onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = item.color + '15'; }}
              onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = item.color + '08'; }}
            >
              <div style={{ fontSize: 24, marginBottom: 4 }}>{item.icon}</div>
              <div style={{ fontSize: 12, fontWeight: 600, color: item.color }}>{item.label}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════
// Tab 2: 使用指南
// ══════════════════════════════════════════

function GuideTab({ navigate }: { navigate: any }) {
  const [expandedStep, setExpandedStep] = useState<number | null>(0);

  const steps = [
    {
      num: 1, title: '安装', icon: '📦',
      desc: '安装 agentic-aiops 到本地',
      details: [
        { label: 'pip 安装', code: 'pip install agentic-aiops' },
        { label: '验证安装', code: 'aiops --version' },
        { label: '查看帮助', code: 'aiops --help' },
      ],
    },
    {
      num: 2, title: '环境探测', icon: '🔍',
      desc: '自动发现服务器环境，推荐 Agent 组合',
      details: [
        { label: '一键探测', code: 'aiops discover' },
        { label: '探测内容', code: 'OS / 硬件 / 云平台 / 容器 / K8s / 中间件 / 数据库 / 网络' },
        { label: '生成报告', code: 'aiops discover --output report.yaml' },
      ],
    },
    {
      num: 3, title: '配置数据源', icon: '🔌',
      desc: '连接 Prometheus、K8s、Grafana 等真实数据源',
      details: [
        { label: '配置文件', code: 'vim config.yaml' },
        { label: 'Prometheus', code: 'prometheus:\n  endpoint: http://prometheus:9090' },
        { label: 'Kubernetes', code: 'kubernetes:\n  kubeconfig: ~/.kube/config' },
      ],
    },
    {
      num: 4, title: '启动服务', icon: '🚀',
      desc: '一键启动 API Server + Dashboard',
      details: [
        { label: '启动命令', code: 'aiops serve' },
        { label: '访问地址', code: 'http://localhost:8000' },
        { label: 'API 文档', code: 'http://localhost:8000/api/v1/docs' },
      ],
    },
    {
      num: 5, title: '日常使用', icon: '⚡',
      desc: '通过 Dashboard 或 CLI 执行运维操作',
      details: [
        { label: '查看告警', code: 'aiops alerts list' },
        { label: '执行工作流', code: 'aiops workflow run "P0 故障响应"' },
        { label: '成本报告', code: 'aiops cost report --period monthly' },
      ],
    },
  ];

  const cliCommands = [
    { cmd: 'aiops discover', desc: '环境探测', category: '探测' },
    { cmd: 'aiops serve', desc: '启动服务', category: '服务' },
    { cmd: 'aiops status', desc: '查看状态', category: '服务' },
    { cmd: 'aiops agents list', desc: '列出智能体', category: '管理' },
    { cmd: 'aiops agents run <agent> "<task>"', desc: '执行任务', category: '管理' },
    { cmd: 'aiops alerts list', desc: '告警列表', category: '运维' },
    { cmd: 'aiops workflow list', desc: '工作流列表', category: '运维' },
    { cmd: 'aiops workflow run "<name>"', desc: '执行工作流', category: '运维' },
    { cmd: 'aiops cost report', desc: '成本报告', category: 'FinOps' },
    { cmd: 'aiops security scan', desc: '安全扫描', category: '安全' },
  ];

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      {/* 快速开始步骤 */}
      <div style={{ marginBottom: 28 }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>🚀 快速开始</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {steps.map(step => (
            <div key={step.num} className="card" style={{
              padding: '16px 20px', cursor: 'pointer',
              borderLeft: '3px solid ' + (expandedStep === step.num ? '#3b82f6' : 'var(--border)'),
              transition: 'all 0.2s',
            }} onClick={() => setExpandedStep(expandedStep === step.num ? null : step.num)}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{
                  width: 32, height: 32, borderRadius: '50%',
                  background: expandedStep === step.num ? 'linear-gradient(135deg, #3b82f6, #8b5cf6)' : 'rgba(255,255,255,0.05)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 14, fontWeight: 700, color: expandedStep === step.num ? '#fff' : 'var(--text-muted)',
                }}>
                  {step.num}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 14, fontWeight: 600 }}>{step.icon} {step.title}</div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>{step.desc}</div>
                </div>
                <span style={{ fontSize: 12, color: 'var(--text-muted)', transform: expandedStep === step.num ? 'rotate(180deg)' : 'rotate(0)', transition: '0.2s' }}>▼</span>
              </div>
              {expandedStep === step.num && (
                <div style={{ marginTop: 14, paddingTop: 14, borderTop: '1px solid var(--border)' }}>
                  {step.details.map((d, i) => (
                    <div key={i} style={{ marginBottom: 10 }}>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>{d.label}</div>
                      <pre style={{
                        margin: 0, padding: '8px 12px', borderRadius: 6,
                        background: 'rgba(0,0,0,0.3)', fontSize: 12, fontFamily: 'monospace',
                        color: '#10b981', lineHeight: 1.5, overflow: 'auto',
                      }}>{d.code}</pre>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* CLI 命令参考 */}
      <div style={{ marginBottom: 28 }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>⌨️ CLI 命令参考</h2>
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr', }}>
            {cliCommands.map((c, i) => (
              <div key={i} style={{
                display: 'flex', alignItems: 'center', gap: 16, padding: '10px 16px',
                borderBottom: i < cliCommands.length - 1 ? '1px solid var(--border)' : 'none',
                background: i % 2 === 0 ? 'rgba(255,255,255,0.01)' : 'transparent',
              }}>
                <span style={{
                  padding: '2px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600,
                  background: 'rgba(59,130,246,0.1)', color: '#3b82f6', minWidth: 50, textAlign: 'center',
                }}>{c.category}</span>
                <code style={{ fontSize: 12, color: '#10b981', fontFamily: 'monospace', flex: 1 }}>{c.cmd}</code>
                <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{c.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 支持的环境 */}
      <div>
        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>🌍 支持的环境拓扑 (18 种)</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10 }}>
          {[
            { icon: '🏢', label: '纯本地物理机', examples: '制造MES、医疗HIS' },
            { icon: '🖥️', label: '纯本地虚拟化', examples: 'VMware、KVM 集群' },
            { icon: '🐳', label: '纯本地容器', examples: 'K3s、Docker Compose' },
            { icon: '☁️', label: '纯公有云', examples: '阿里云、AWS 全托管' },
            { icon: 'λ', label: 'Serverless', examples: '函数计算 + API 网关' },
            { icon: '🏰', label: '托管私有云', examples: '华为云 Stack 政务云' },
            { icon: '🔗', label: '混合云', examples: '本地IDC + 云弹性扩展' },
            { icon: '🌐', label: '多云部署', examples: '阿里云 + AWS + Azure' },
            { icon: '🌍', label: '跨境部署', examples: 'PIPL + GDPR 合规' },
            { icon: '📡', label: '边缘+云', examples: '工厂边缘 AI + 云端训练' },
            { icon: '⚡', label: '多活架构', examples: '证券同城双活 RPO=0' },
            { icon: '🔄', label: '主备/灾备', examples: '异地灾备 RTO<15min' },
            { icon: '🇨🇳', label: '国产化全栈', examples: '麒麟+达梦+东方通' },
            { icon: '🏭', label: '智能制造', examples: '边缘产线 + 云端 AI' },
            { icon: '🏙️', label: '智慧城市', examples: '三层: 边缘+本地+云' },
            { icon: '🎮', label: '游戏双云', examples: '腾讯云(运行)+阿里云(官网)' },
            { icon: '🏥', label: '高校超算', examples: 'VMware + HPC 节点' },
            { icon: '🛒', label: '电商平台', examples: '阿里云全托管 + 弹性' },
          ].map(item => (
            <div key={item.label} style={{
              padding: '10px 14px', borderRadius: 8,
              background: 'rgba(255,255,255,0.02)', border: '1px solid var(--border)',
              display: 'flex', alignItems: 'center', gap: 10,
            }}>
              <span style={{ fontSize: 20 }}>{item.icon}</span>
              <div>
                <div style={{ fontSize: 12, fontWeight: 600 }}>{item.label}</div>
                <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>{item.examples}</div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 12, textAlign: 'center' }}>
          <button onClick={() => navigate('/environments')} style={{
            padding: '8px 20px', borderRadius: 8, border: '1px solid rgba(59,130,246,0.3)',
            background: 'rgba(59,130,246,0.08)', color: '#3b82f6', cursor: 'pointer', fontSize: 12, fontWeight: 600,
          }}>
            🏗️ 查看环境管理 →
          </button>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════
// Tab 3: Agent 网络
// ══════════════════════════════════════════

function NetworkTab() {
  // 简化的网络拓扑图（纯 CSS/SVG，不依赖 ReactFlow）
  const agentList = demoAgentData;
  const connections = demoConnections;

  // 网络拓扑说明
  const archLayers = [
    {
      name: '🧠 核心调度层',
      color: '#3b82f6',
      agents: ['planner', 'copilot'],
      desc: 'planner 负责任务编排和调度，copilot 提供 AI 对话交互',
    },
    {
      name: '🔧 基础运维层',
      color: '#10b981',
      agents: ['linux', 'docker', 'k8s', 'db', 'middleware', 'network', 'virtual', 'windows'],
      desc: '覆盖操作系统、容器、数据库、中间件、网络、虚拟化等基础组件',
    },
    {
      name: '📊 监控可观测层',
      color: '#8b5cf6',
      agents: ['monitor', 'log', 'apm', 'sre'],
      desc: '指标采集、日志分析、链路追踪、SLO 管理',
    },
    {
      name: '🔒 安全 & 运维层',
      color: '#f97316',
      agents: ['security', 'incident', 'devops', 'gitops', 'iac'],
      desc: '安全扫描、应急响应、CI/CD、基础设施即代码',
    },
    {
      name: '☁️ 云 & FinOps 层',
      color: '#ec4899',
      agents: ['cloud', 'cost', 'servicemesh'],
      desc: '多云管理、成本优化、服务网格',
    },
  ];

  const getAgentIcon = (name: string) => {
    const found = agentList.find(a => a.name === name);
    return found?.icon || '🤖';
  };

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      {/* 架构说明 */}
      <div className="card" style={{
        padding: '24px 28px', marginBottom: 20,
        background: 'linear-gradient(135deg, rgba(59,130,246,0.06), rgba(139,92,246,0.06))',
        border: '1px solid rgba(59,130,246,0.15)',
      }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>🕸️ Agent 网络架构</h2>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.7, margin: 0 }}>
          所有 Agent 通过 <strong style={{ color: 'var(--text-primary)' }}>planner（核心调度器）</strong> 统一编排。
          planner 根据任务类型自动分配给对应的 Agent，Agent 之间通过消息总线协作。
          每个 Agent 拥有专属的 MCP 工具集，可独立执行也可组合工作。
        </p>
      </div>

      {/* 分层架构图 */}
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>🏛️ 分层架构</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {archLayers.map((layer) => (
            <div key={layer.name} className="card" style={{
              padding: '16px 20px', borderLeft: '4px solid ' + layer.color,
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
                <span style={{ fontSize: 14, fontWeight: 700, color: layer.color }}>{layer.name}</span>
                <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{layer.agents.length} 个 Agent</span>
              </div>
              <p style={{ fontSize: 12, color: 'var(--text-secondary)', margin: '0 0 10px', lineHeight: 1.5 }}>{layer.desc}</p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {layer.agents.map(name => {
                  const a = agentList.find(ag => ag.name === name);
                  return (
                    <span key={name} style={{
                      display: 'inline-flex', alignItems: 'center', gap: 4,
                      padding: '4px 10px', borderRadius: 6,
                      background: layer.color + '10', border: '1px solid ' + layer.color + '25',
                      fontSize: 11, fontWeight: 500,
                    }}>
                      <span>{a?.icon || '🤖'}</span>
                      <span style={{ color: 'var(--text-primary)' }}>{name}</span>
                      <span style={{
                        width: 6, height: 6, borderRadius: '50%',
                        background: a?.status === 'active' ? '#10b981' : '#f59e0b',
                      }} />
                    </span>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 通信链路 */}
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>🔗 关键通信链路</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 8 }}>
          {connections.slice(0, 14).map((conn, i) => (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: 8,
              padding: '8px 12px', borderRadius: 6,
              background: 'rgba(255,255,255,0.02)', border: '1px solid var(--border)',
              fontSize: 12,
            }}>
              <span>{getAgentIcon(conn.source)}</span>
              <span style={{ fontWeight: 500 }}>{conn.source}</span>
              <span style={{ color: 'var(--text-muted)' }}>→</span>
              <span>{getAgentIcon(conn.target)}</span>
              <span style={{ fontWeight: 500 }}>{conn.target}</span>
              <span style={{
                marginLeft: 'auto', padding: '1px 6px', borderRadius: 4,
                fontSize: 10, background: 'rgba(59,130,246,0.1)', color: '#3b82f6',
              }}>{conn.label}</span>
            </div>
          ))}
        </div>
      </div>

      <div style={{ fontSize: 12, color: 'var(--text-muted)', textAlign: 'center', marginTop: 8 }}>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════
// Tab 4: 智能体 & 工具
// ══════════════════════════════════════════

function AgentsTab() {
  const agentData: AgentData[] = demoAgentData;
  const categories = toolCategories;
  const totalTools = categories.reduce((a, c) => a + c.count, 0);

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      {/* 概览 */}
      <div className="card" style={{
        padding: '24px 28px', marginBottom: 20,
        background: 'linear-gradient(135deg, rgba(139,92,246,0.06), rgba(59,130,246,0.06))',
        border: '1px solid rgba(139,92,246,0.15)',
      }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>🤖 智能体 & 工具体系</h2>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.7, margin: 0 }}>
          平台拥有 <strong style={{ color: 'var(--text-primary)' }}>{agentData.length} 个专业智能体</strong> 和
          <strong style={{ color: 'var(--text-primary)' }}> {totalTools} 个 MCP 工具</strong>，
          覆盖 {categories.length} 大类运维场景。每个智能体是一个独立的 AI Agent，
          拥有自己的工具集、知识库和决策逻辑，可独立工作也可被 planner 统一调度。
        </p>
      </div>

      {/* 工具分类 */}
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>🔌 工具覆盖 ({categories.length} 类 {totalTools} 个)</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 10 }}>
          {categories.map((cat, i) => (
            <div key={i} className="card" style={{ padding: 14 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                <span style={{ fontSize: 20 }}>{cat.icon}</span>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>{cat.name}</div>
                  <div style={{ fontSize: 18, fontWeight: 700, color: cat.color }}>{cat.count}</div>
                </div>
              </div>
              <div style={{ fontSize: 10, color: 'var(--text-muted)', lineHeight: 1.4 }}>
                {cat.tools.slice(0, 5).join(' · ')}{cat.tools.length > 5 ? ' ...' : ''}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 智能体列表 */}
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>🤖 智能体目录 ({agentData.length} 个)</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
          {agentData.map(agent => (
            <div key={agent.name} className="card" style={{ padding: 16 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
                <span style={{ fontSize: 28 }}>{agent.icon}</span>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 600 }}>{agent.name}</div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{agent.description}</div>
                </div>
              </div>
              <div style={{ display: 'flex', gap: 6, marginBottom: 8 }}>
                <span style={{
                  padding: '2px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600,
                  background: agent.status === 'active' ? 'rgba(16,185,129,0.12)' : 'rgba(245,158,11,0.12)',
                  color: agent.status === 'active' ? '#10b981' : '#f59e0b',
                }}>
                  {agent.status === 'active' ? '● 运行中' : '○ 空闲'}
                </span>
                <span style={{
                  padding: '2px 8px', borderRadius: 4, fontSize: 10,
                  background: 'rgba(59,130,246,0.1)', color: '#3b82f6',
                }}>{agent.category}</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
                <div style={{ textAlign: 'center', padding: 6, background: 'rgba(255,255,255,0.02)', borderRadius: 6 }}>
                  <div style={{ fontSize: 16, fontWeight: 700, color: '#3b82f6' }}>{agent.tasks}</div>
                  <div style={{ fontSize: 9, color: 'var(--text-muted)' }}>总任务</div>
                </div>
                <div style={{ textAlign: 'center', padding: 6, background: 'rgba(255,255,255,0.02)', borderRadius: 6 }}>
                  <div style={{ fontSize: 16, fontWeight: 700, color: '#10b981' }}>{agent.tools.length}</div>
                  <div style={{ fontSize: 9, color: 'var(--text-muted)' }}>工具数</div>
                </div>
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 3, marginTop: 8 }}>
                {agent.tools.map((t, j) => (
                  <span key={j} style={{
                    padding: '1px 5px', borderRadius: 3, fontSize: 9,
                    background: 'rgba(255,255,255,0.04)', color: 'var(--text-muted)',
                  }}>{t}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════
// 主页面
// ══════════════════════════════════════════

export default function DashboardPage() {
  const navigate = useNavigate();
  const [tab, setTab] = useState<Tab>('overview');

  return (
    <div className="animate-fade-in">
      {/* 顶部 Tab 栏 */}
      <div className="page-header">
        <div>
          <h1 className="page-title">📊 仪表盘</h1>
          <p className="page-subtitle">平台介绍 · 使用指南 · 架构说明</p>
        </div>
      </div>

      {/* Tab 导航 */}
      <div style={{
        display: 'flex', gap: 4, padding: 4, borderRadius: 12,
        background: 'rgba(255,255,255,0.03)', marginBottom: 24,
        border: '1px solid var(--border)',
      }}>
        {tabConfig.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)} style={{
            flex: 1, padding: '10px 16px', borderRadius: 8, border: 'none',
            cursor: 'pointer', fontSize: 13, fontWeight: 600, transition: 'all 0.2s',
            background: tab === t.key ? 'linear-gradient(135deg, #3b82f6, #8b5cf6)' : 'transparent',
            color: tab === t.key ? '#fff' : 'var(--text-secondary)',
          }}>
            {t.icon} {t.label}
          </button>
        ))}
      </div>

      {/* Tab 内容 */}
      {tab === 'overview' && <OverviewTab navigate={navigate} />}
      {tab === 'guide' && <GuideTab navigate={navigate} />}
      {tab === 'network' && <NetworkTab />}
      {tab === 'agents' && <AgentsTab />}
    </div>
  );
}
