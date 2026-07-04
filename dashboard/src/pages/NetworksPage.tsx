import { useState, useEffect, useMemo } from 'react';
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
import { fetchApi, type AgentData, type AgentConnection, demoAgentData, demoConnections } from '../api';

interface AgentInfo {
  id: string; name: string; icon: string; status: string;
  color: string; tasks: number; successRate: number;
}

function AgentNode({ data }: { data: { agent: AgentInfo } }) {
  const { agent } = data;
  return (
    <div style={{
      background: '#1a1f35', border: `2px solid ${agent.status === 'active' ? agent.color : '#2a3050'}`,
      borderRadius: 12, padding: '12px 16px', textAlign: 'center', minWidth: 100,
      boxShadow: agent.status === 'active' ? `0 0 12px ${agent.color}30` : 'none',
    }}>
      <div style={{ fontSize: 24, marginBottom: 4 }}>{agent.icon}</div>
      <div style={{ fontSize: 12, fontWeight: 600, color: '#e2e8f0' }}>{agent.name}</div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4, marginTop: 4, fontSize: 10, color: '#94a3b8' }}>
        <span style={{ width: 6, height: 6, borderRadius: '50%', background: agent.status === 'active' ? '#10b981' : '#f59e0b' }} />
        {agent.status === 'active' ? '运行中' : '空闲'}
      </div>
      <div style={{ fontSize: 9, color: '#64748b', marginTop: 2 }}>{agent.tasks} 任务 · {agent.successRate}%</div>
    </div>
  );
}

const nodeTypes = { agentNode: AgentNode };

export default function NetworksPage() {
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [connections, setConnections] = useState<AgentConnection[]>([]);
  const [mode, setMode] = useState<'loading' | 'demo' | 'real'>('loading');

  useEffect(() => {
    Promise.all([
      fetchApi<AgentData[]>('/api/v1/agents', demoAgentData),
      fetchApi<AgentConnection[]>('/api/v1/network/connections', demoConnections),
    ]).then(([agentsR, connR]) => {
      setAgents(agentsR.data.map(a => ({
        id: a.name, name: a.name, icon: a.icon, status: a.status,
        color: '#3b82f6', tasks: a.tasks, successRate: 95,
      })));
      setConnections(connR.data);
      setMode('demo');
    });
  }, []);

  const { nodes: initialNodes, edges: initialEdges } = useMemo(() => {
    if (agents.length === 0) return { nodes: [], edges: [] };
    const centerX = 500, centerY = 300, radius = 250;
    const nodes: Node[] = [];
    const edges: Edge[] = [];

    const planner = agents.find(a => a.id === 'planner') || agents[0];
    nodes.push({ id: planner.id, type: 'agentNode', position: { x: centerX - 70, y: centerY - 40 }, data: { agent: planner } });

    const others = agents.filter(a => a.id !== planner.id);
    others.forEach((agent, i) => {
      const angle = (i / others.length) * 2 * Math.PI - Math.PI / 2;
      nodes.push({
        id: agent.id, type: 'agentNode',
        position: { x: centerX + radius * Math.cos(angle) - 70, y: centerY + radius * Math.sin(angle) - 40 },
        data: { agent },
      });
    });

    connections.forEach((conn, i) => {
      edges.push({
        id: `e-${i}`, source: conn.source, target: conn.target, label: conn.label,
        animated: conn.source === planner.id,
        style: { stroke: '#2a3050', strokeWidth: 2 },
        labelStyle: { fill: '#64748b', fontSize: 10 },
        labelBgStyle: { fill: '#1a1f35', fillOpacity: 0.8 },
      });
    });

    return { nodes, edges };
  }, [agents, connections]);

  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>🕸️ Agent 网络拓扑</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>多智能体协作关系 · 实时数据流</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <span style={{ padding: '4px 10px', borderRadius: 6, background: 'rgba(16,185,129,0.12)', color: '#10b981', fontSize: 11 }}>● {agents.filter(a => a.status === 'active').length} 活跃</span>
          <span style={{ padding: '4px 10px', borderRadius: 6, background: 'rgba(245,158,11,0.12)', color: '#f59e0b', fontSize: 11 }}>● {agents.filter(a => a.status !== 'active').length} 空闲</span>
        </div>
      </div>

      <div style={{ height: 500, background: '#0f1629', borderRadius: 12, border: '1px solid #2a3050', overflow: 'hidden' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          proOptions={{ hideAttribution: true }}
          style={{ background: '#0f1629' }}
        >
          <Background color="#1a2040" gap={20} />
          <Controls />
        </ReactFlow>
      </div>

      <div style={{ display: 'flex', gap: 24, marginTop: 16, fontSize: 12, color: '#64748b' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{ width: 12, height: 2, borderRadius: 1, background: '#2a3050' }} />
          <span>数据流</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{ width: 12, height: 2, borderRadius: 1, background: '#2a3050', borderTop: '2px dashed #3b82f6' }} />
          <span>调度指令</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#10b981' }} />
          <span>运行中</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#f59e0b' }} />
          <span>空闲</span>
        </div>
      </div>
    </div>
  );
}
