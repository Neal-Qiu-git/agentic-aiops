# 审批系统 (Approval)

## 概述

审批系统支持高风险操作的人工确认，确保生产环境安全。

## 审批策略

| 策略 | 说明 |
|------|------|
| **Auto** | 低风险自动通过 |
| **Risk Score** | 基于风险评分决定 |
| **Manual** | 必须人工审批 |

## 危险操作

以下操作默认需要审批：

- 删除操作 (`rm -rf`, `delete`)
- 重启服务 (`restart`, `reboot`)
- 扩缩容 (`scale`, `resize`)
- 版本升级 (`upgrade`, `update`)
- 回滚操作 (`rollback`)
- 配置变更 (`config change`)

## 使用示例

### 查看待审批

```bash
aiops approval list
```

输出：
```
Pending Approvals
├── APR-001: restart mysql (High Risk)
├── APR-002: scale deployment (Medium Risk)
└── APR-003: delete log file (Low Risk)
```

### 审批操作

```bash
# 批准
aiops approval approve APR-001

# 拒绝
aiops approval reject APR-002 --reason "需要在维护窗口执行"

# 查看详情
aiops approval info APR-001
```

## Webhook 集成

### 飞书通知

```yaml
approval:
  webhook:
    type: feishu
    url: https://open.feishu.cn/open-apis/bot/v2/hook/xxx
```

### 钉钉通知

```yaml
approval:
  webhook:
    type: dingtalk
    url: https://oapi.dingtalk.com/robot/send?access_token=xxx
```

### Slack 通知

```yaml
approval:
  webhook:
    type: slack
    url: https://hooks.slack.com/services/xxx
```

### Email 通知

```yaml
approval:
  email:
    smtp: smtp.example.com
    to:
      - admin@example.com
      - ops@example.com
```

## 审批流程

```
Agent 准备执行危险操作
    │
    ▼
创建审批请求
    │
    ▼
发送通知 (飞书/钉钉/Slack/Email)
    │
    ▼
等待审批
    │
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼
批准                  拒绝
    │                   │
    ▼                   ▼
执行操作            记录拒绝原因
    │
    ▼
记录审计日志
```

## 风险等级

| 等级 | 说明 | 示例 |
|------|------|------|
| **Low** | 低风险 | 查看日志、查询信息 |
| **Medium** | 中风险 | 重启服务、修改配置 |
| **High** | 高风险 | 删除数据、扩缩容 |
| **Critical** | 极高风险 | 删除集群、格式化磁盘 |

## 配置

```yaml
approval:
  # 自动审批阈值
  auto_approve_threshold: low

  # 需要审批的操作
  require_approval_for:
    - restart
    - delete
    - scale
    - upgrade
    - rollback

  # 超时时间（秒）
  timeout: 300

  # 审批人
  reviewers:
    - admin
    - ops-lead
```
