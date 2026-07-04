import { useState } from 'react';

interface SettingSection {
  id: string; title: string; icon: string; settings: Setting[];
}
interface Setting {
  key: string; label: string; type: 'text' | 'select' | 'toggle' | 'number';
  value: any; options?: string[]; description: string;
}

const initialSettings: SettingSection[] = [
  {
    id: 'general', title: '通用设置', icon: '⚙️',
    settings: [
      { key: 'platform_name', label: '平台名称', type: 'text', value: 'Agentic AIOps', description: '显示在侧边栏和页面标题' },
      { key: 'language', label: '语言', type: 'select', value: 'zh-CN', options: ['zh-CN', 'en-US'], description: '界面语言' },
      { key: 'timezone', label: '时区', type: 'select', value: 'Asia/Shanghai', options: ['Asia/Shanghai', 'UTC', 'America/New_York'], description: '时间显示时区' },
      { key: 'auto_refresh', label: '自动刷新', type: 'toggle', value: true, description: '页面数据自动刷新' },
      { key: 'refresh_interval', label: '刷新间隔(秒)', type: 'number', value: 15, description: '自动刷新间隔' },
    ],
  },
  {
    id: 'notification', title: '通知设置', icon: '🔔',
    settings: [
      { key: 'email_enabled', label: '邮件通知', type: 'toggle', value: true, description: '告警邮件通知' },
      { key: 'email_smtp', label: 'SMTP 服务器', type: 'text', value: 'smtp.company.com', description: '邮件服务器地址' },
      { key: 'webhook_enabled', label: 'Webhook 通知', type: 'toggle', value: true, description: '企业微信/钉钉/飞书通知' },
      { key: 'webhook_url', label: 'Webhook URL', type: 'text', value: 'https://qyapi.weixin.qq.com/webhook/send?key=xxx', description: '企业微信 Webhook 地址' },
      { key: 'alert_severity', label: '通知级别', type: 'select', value: 'warning', options: ['critical', 'warning', 'info'], description: '仅通知该级别及以上的告警' },
    ],
  },
  {
    id: 'security', title: '安全设置', icon: '🔒',
    settings: [
      { key: 'session_timeout', label: '会话超时(分钟)', type: 'number', value: 30, description: '登录后无操作超时时间' },
      { key: 'audit_log', label: '审计日志', type: 'toggle', value: true, description: '记录所有操作审计日志' },
      { key: 'ip_whitelist', label: 'IP 白名单', type: 'text', value: '10.0.0.0/8, 172.16.0.0/12', description: '允许访问的 IP 范围' },
      { key: 'mfa_enabled', label: '双因素认证', type: 'toggle', value: false, description: '登录时需要验证码' },
    ],
  },
  {
    id: 'api', title: 'API 设置', icon: '🔌',
    settings: [
      { key: 'api_rate_limit', label: 'API 限流(次/分钟)', type: 'number', value: 60, description: '每个 API Key 的请求限制' },
      { key: 'api_timeout', label: 'API 超时(秒)', type: 'number', value: 30, description: 'API 请求超时时间' },
      { key: 'cors_enabled', label: 'CORS', type: 'toggle', value: true, description: '允许跨域请求' },
    ],
  },
];

export default function SettingsPage() {
  const [sections, setSections] = useState(initialSettings);
  const [activeSection, setActiveSection] = useState('general');

  const updateSetting = (sectionId: string, key: string, value: any) => {
    setSections(prev => prev.map(s =>
      s.id === sectionId
        ? { ...s, settings: s.settings.map(st => st.key === key ? { ...st, value } : st) }
        : s
    ));
  };

  const currentSection = sections.find(s => s.id === activeSection);

  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>⚙️ 系统设置</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>平台配置 · 通知 · 安全 · API</p>
        </div>
        <button style={{ padding: '8px 20px', borderRadius: 8, border: 'none', background: '#3b82f6', color: 'white', cursor: 'pointer', fontSize: 13, fontWeight: 600 }}>
          💾 保存设置
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr', gap: 20 }}>
        {/* Sidebar */}
        <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 12 }}>
          {sections.map(s => (
            <button key={s.id} onClick={() => setActiveSection(s.id)} style={{ display: 'flex', alignItems: 'center', gap: 10, width: '100%', padding: '10px 12px', borderRadius: 8, border: 'none', cursor: 'pointer', background: activeSection === s.id ? 'rgba(59,130,246,0.15)' : 'transparent', color: activeSection === s.id ? '#3b82f6' : '#94a3b8', fontSize: 13, fontWeight: activeSection === s.id ? 600 : 400, textAlign: 'left', marginBottom: 4 }}>
              <span>{s.icon}</span>
              <span>{s.title}</span>
            </button>
          ))}
        </div>

        {/* Settings Content */}
        {currentSection && (
          <div style={{ background: '#1a1f35', border: '1px solid #2a3050', borderRadius: 12, padding: 24 }}>
            <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 20, display: 'flex', alignItems: 'center', gap: 8 }}>
              <span>{currentSection.icon}</span>
              <span>{currentSection.title}</span>
            </div>

            {currentSection.settings.map((setting, i) => (
              <div key={setting.key} style={{ padding: '16px 0', borderBottom: i < currentSection.settings.length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 13, fontWeight: 500, color: '#e2e8f0' }}>{setting.label}</div>
                    <div style={{ fontSize: 11, color: '#64748b', marginTop: 2 }}>{setting.description}</div>
                  </div>
                  <div style={{ width: 240 }}>
                    {setting.type === 'toggle' ? (
                      <button onClick={() => updateSetting(currentSection.id, setting.key, !setting.value)} style={{ width: 44, height: 24, borderRadius: 12, border: 'none', cursor: 'pointer', background: setting.value ? '#3b82f6' : '#374151', position: 'relative', transition: 'background 0.2s' }}>
                        <div style={{ width: 18, height: 18, borderRadius: '50%', background: 'white', position: 'absolute', top: 3, left: setting.value ? 23 : 3, transition: 'left 0.2s' }} />
                      </button>
                    ) : setting.type === 'select' ? (
                      <select value={setting.value} onChange={e => updateSetting(currentSection.id, setting.key, e.target.value)} style={{ width: '100%', padding: '8px 12px', borderRadius: 6, border: '1px solid #2a3050', background: '#0f1629', color: '#e2e8f0', fontSize: 12, cursor: 'pointer' }}>
                        {setting.options?.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                      </select>
                    ) : setting.type === 'number' ? (
                      <input type="number" value={setting.value} onChange={e => updateSetting(currentSection.id, setting.key, Number(e.target.value))} style={{ width: '100%', padding: '8px 12px', borderRadius: 6, border: '1px solid #2a3050', background: '#0f1629', color: '#e2e8f0', fontSize: 12 }} />
                    ) : (
                      <input type="text" value={setting.value} onChange={e => updateSetting(currentSection.id, setting.key, e.target.value)} style={{ width: '100%', padding: '8px 12px', borderRadius: 6, border: '1px solid #2a3050', background: '#0f1629', color: '#e2e8f0', fontSize: 12 }} />
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
