import { useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { agents, connections } from '../data/agents';

// Custom Agent Node
function AgentNode({ data }: { data: { agent: typeof agents[0] } }) {
  const { agent } = data;
  return (
    <div className={`agent-node ${agent.status === 'active' ? 'active' : ''}`}>
      <div className="agent-icon">{agent.icon}</div>
      <div className="agent-name">{agent.name}</div>
      <div className="agent-status">
        <span style={{
          display:'inline-block',width:6,height:6,borderRadius:'50%',
          background: agent.status==='active'?'var(--accent-green)':agent.status==='idle'?'var(--accent-yellow)':'var(--accent-red)',
          marginRight:4
        }}/>
        {agent.status === 'active' ? '运行中' : agent.status === 'idle' ? '空闲' : '异常'}
      </div>
      <div style={{fontSize:10,color:'var(--text-muted)',marginTop:4}}>
        {agent.tasks} 任务 · {agent.successRate}%
      </div>
    </div>
  );
}

const nodeTypes = { agentNode: AgentNode };

// Layout positions - circular arrangement around planner
function layoutAgents() {
  const centerX = 500;
  const centerY = 300;
  const radius = 250;
  const nodes: Node[] = [];
  const edges: Edge[] = [];

  // Planner at center
  const planner = agents.find(a => a.id === 'planner')!;
  nodes.push({
    id: 'planner',
    type: 'agentNode',
    position: { x: centerX - 70, y: centerY - 40 },
    data: { agent: planner },
  });

  // Other agents in circle
  const others = agents.filter(a => a.id !== 'planner');
  others.forEach((agent, i) => {
    const angle = (i / others.length) * 2 * Math.PI - Math.PI / 2;
    const x = centerX + radius * Math.cos(angle) - 70;
    const y = centerY + radius * Math.sin(angle) - 40;
    nodes.push({
      id: agent.id,
      type: 'agentNode',
      position: { x, y },
      data: { agent },
    });
  });

  // Edges from connections
  connections.forEach((conn, i) => {
    edges.push({
      id: `e-${i}`,
      source: conn.source,
      target: conn.target,
      label: conn.label,
      animated: conn.source === 'planner',
      style: { stroke: '#2a3050', strokeWidth: 2 },
      labelStyle: { fill: '#64748b', fontSize: 10 },
      labelBgStyle: { fill: '#1a1f35', fillOpacity: 0.8 },
    });
  });

  return { nodes, edges };
}

export default function NetworksPage() {
  const { nodes: initialNodes, edges: initialEdges } = useMemo(() => layoutAgents(), []);
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">🕸️ Agent 网络拓扑</h1>
          <p className="page-subtitle">多智能体协作关系 · 实时数据流</p>
        </div>
        <div style={{display:'flex',gap:8}}>
          <span className="badge badge-green">● {agents.filter(a=>a.status==='active').length} 活跃</span>
          <span className="badge badge-yellow">● {agents.filter(a=>a.status==='idle').length} 空闲</span>
        </div>
      </div>

      <div className="network-container">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          proOptions={{ hideAttribution: true }}
          style={{background: 'var(--bg-primary)'}}
        >
          <Background color="#1a2040" gap={20} />
          <Controls />
        </ReactFlow>
      </div>

      {/* Legend */}
      <div style={{display:'flex',gap:24,marginTop:16,fontSize:12,color:'var(--text-muted)'}}>
        <div style={{display:'flex',alignItems:'center',gap:6}}>
          <div style={{width:12,height:2,borderRadius:1,background:'var(--border)'}}/>
          <span>数据流</span>
        </div>
        <div style={{display:'flex',alignItems:'center',gap:6}}>
          <div style={{width:12,height:2,borderRadius:1,background:'var(--border)',borderTop:'2px dashed var(--accent-blue)'}}/>
          <span>调度指令</span>
        </div>
        <div style={{display:'flex',alignItems:'center',gap:6}}>
          <div style={{width:8,height:8,borderRadius:'50%',background:'var(--accent-green)'}}/>
          <span>运行中</span>
        </div>
        <div style={{display:'flex',alignItems:'center',gap:6}}>
          <div style={{width:8,height:8,borderRadius:'50%',background:'var(--accent-yellow)'}}/>
          <span>空闲</span>
        </div>
      </div>
    </div>
  );
}
