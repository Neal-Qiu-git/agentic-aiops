import { lazy, Suspense } from 'react';
import { HashRouter, Routes, Route, NavLink } from 'react-router-dom';

// 懒加载所有页面组件 — 首屏只加载 DashboardPage
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const EnvironmentPage = lazy(() => import('./pages/EnvironmentPage'));
const MonitoringPage = lazy(() => import('./pages/MonitoringPage'));
const SLOPage = lazy(() => import('./pages/SLOPage'));
const AlertPage = lazy(() => import('./pages/AlertPage'));
const DeploymentPage = lazy(() => import('./pages/DeploymentPage'));
const WorkflowsPage = lazy(() => import('./pages/WorkflowsPage'));
const EventsPage = lazy(() => import('./pages/EventsPage'));
const SecurityPage = lazy(() => import('./pages/SecurityPage'));
const CostPage = lazy(() => import('./pages/CostPage'));
const DataSourcePage = lazy(() => import('./pages/DataSourcePage'));
const AuditLogPage = lazy(() => import('./pages/AuditLogPage'));
const SettingsPage = lazy(() => import('./pages/SettingsPage'));
const ApiDocsPage = lazy(() => import('./pages/ApiDocsPage'));

function Loading() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#64748b' }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: 28, marginBottom: 8, animation: 'spin 1s linear infinite' }}>⚙️</div>
        <div style={{ fontSize: 13 }}>加载中...</div>
      </div>
    </div>
  );
}

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
              <NavLink to="/environments" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>🏗️</span><span>环境</span>
              </NavLink>
            </div>
            <div className="nav-section">
              <div className="nav-section-title">运维</div>
              <NavLink to="/monitoring" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>📊</span><span>实时监控</span>
              </NavLink>
              <NavLink to="/slo" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>🎯</span><span>SLO 仪表盘</span>
              </NavLink>
              <NavLink to="/alerts" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>🚨</span><span>告警中心</span>
              </NavLink>
              <NavLink to="/deployment" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>🚀</span><span>部署管理</span>
              </NavLink>
              <NavLink to="/workflows" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>⚡</span><span>工作流</span>
              </NavLink>
              <NavLink to="/events" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>📡</span><span>事件日志</span>
              </NavLink>
            </div>
            <div className="nav-section">
              <div className="nav-section-title">安全 & 成本</div>
              <NavLink to="/security" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>🔒</span><span>安全态势</span>
              </NavLink>
              <NavLink to="/cost" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>💰</span><span>成本分析</span>
              </NavLink>
            </div>
            <div className="nav-section">
              <div className="nav-section-title">配置</div>
              <NavLink to="/datasource" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>🔌</span><span>数据源</span>
              </NavLink>
              <NavLink to="/audit" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>📋</span><span>审计日志</span>
              </NavLink>
              <NavLink to="/settings" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
                <span>⚙️</span><span>系统设置</span>
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
            v5.3.0 · MIT License
          </div>
        </aside>
        <main className="main-content">
          <Suspense fallback={<Loading />}>
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/environments" element={<EnvironmentPage />} />
              <Route path="/monitoring" element={<MonitoringPage />} />
              <Route path="/slo" element={<SLOPage />} />
              <Route path="/alerts" element={<AlertPage />} />
              <Route path="/deployment" element={<DeploymentPage />} />
              <Route path="/workflows" element={<WorkflowsPage />} />
              <Route path="/events" element={<EventsPage />} />
              <Route path="/security" element={<SecurityPage />} />
              <Route path="/cost" element={<CostPage />} />
              <Route path="/datasource" element={<DataSourcePage />} />
              <Route path="/audit" element={<AuditLogPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/api-docs" element={<ApiDocsPage />} />
            </Routes>
          </Suspense>
        </main>
      </div>
    </HashRouter>
  );
}

export default App;
