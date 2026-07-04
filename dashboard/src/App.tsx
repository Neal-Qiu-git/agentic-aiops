import { HashRouter, Routes, Route, NavLink } from 'react-router-dom';
import NetworksPage from './pages/NetworksPage';
import DashboardPage from './pages/DashboardPage';
import WorkflowsPage from './pages/WorkflowsPage';
import EventsPage from './pages/EventsPage';
import AgentsPage from './pages/AgentsPage';
import ApiDocsPage from './pages/ApiDocsPage';

function App() {
  return (
    <HashRouter>
      <div className="app-layout">
        <aside className="sidebar">
          <div className="sidebar-header">
            <h1>🤖 Agentic AIOps</h1>
            <p>AI-native Operations Platform</p>
          </div>
          <nav className="sidebar-nav">
            <div className="nav-section">
              <div className="nav-section-title">概览</div>
              <NavLink to="/" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`} end>
                <span>📊</span><span>仪表盘</span>
              </NavLink>
              <NavLink to="/networks" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>🕸️</span><span>Agent 网络</span>
              </NavLink>
              <NavLink to="/agents" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>🤖</span><span>智能体管理</span>
              </NavLink>
            </div>
            <div className="nav-section">
              <div className="nav-section-title">运维</div>
              <NavLink to="/workflows" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>⚡</span><span>工作流</span>
              </NavLink>
              <NavLink to="/events" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>📡</span><span>事件日志</span>
              </NavLink>
            </div>
            <div className="nav-section">
              <div className="nav-section-title">开发</div>
              <NavLink to="/api-docs" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>📖</span><span>API 文档</span>
              </NavLink>
            </div>
            <div className="nav-section">
              <div className="nav-section-title">系统</div>
              <a className="nav-link" href="https://gitee.com/neal4752/agentic-aiops" target="_blank" rel="noreferrer">
                <span>🐙</span><span>Gitee</span>
              </a>
              <a className="nav-link" href="https://github.com/Neal-Qiu-git/agentic-aiops" target="_blank" rel="noreferrer">
                <span>🐱</span><span>GitHub</span>
              </a>
            </div>
          </nav>
          <div style={{padding: '12px', borderTop: '1px solid rgba(59,130,246,0.15)', fontSize: '11px', color: '#475569', textAlign: 'center'}}>
            v4.2.0 · MIT License
          </div>
        </aside>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/networks" element={<NetworksPage />} />
            <Route path="/agents" element={<AgentsPage />} />
            <Route path="/workflows" element={<WorkflowsPage />} />
            <Route path="/events" element={<EventsPage />} />
            <Route path="/api-docs" element={<ApiDocsPage />} />
          </Routes>
        </main>
      </div>
    </HashRouter>
  );
}

export default App;
