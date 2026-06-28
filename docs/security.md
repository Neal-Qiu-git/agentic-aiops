# 安全配置

## 概述

Agentic AIOps 内置多层安全机制，确保运维操作安全可控。

## 安全特性

### 1. 命令安全

#### 命令白名单

```yaml
security:
  allowed_commands:
    - kubectl
    - docker
    - systemctl
    - journalctl
    - ps
    - top
    - df
    - free
```

#### 命令黑名单

```yaml
security:
  blocked_commands:
    - rm -rf
    - mkfs
    - dd
    - shutdown
    - reboot
    - init 0
    - init 6
```

#### 危险路径

```yaml
security:
  blocked_paths:
    - /etc/shadow
    - /etc/passwd
    - /root/.ssh
    - /etc/sudoers
```

### 2. 认证管理

#### 环境变量

```bash
# 服务器密码
export AIOPS_SERVER_PRODUCTION_PASSWORD="xxx"

# API Key
export AIOPS_AI_API_KEY="xxx"
```

#### 密钥文件

```yaml
servers:
  - name: production
    host: 10.0.0.1
    key_file: ~/.ssh/id_rsa
```

### 3. 输入验证

- 命令注入检测
- 特殊字符过滤
- 路径遍历防护

### 4. 输出清理

- 敏感信息移除
- 密码/密钥隐藏
- 输出长度限制

### 5. 审计日志

```yaml
security:
  audit_logging: true
  audit_log_path: /var/log/aiops/audit.log
```

## 风险评估

### 风险等级

| 等级 | 说明 | 防护措施 |
|------|------|----------|
| **Low** | 低风险 | 记录日志 |
| **Medium** | 中风险 | 记录日志 + 告警 |
| **High** | 高风险 | 记录日志 + 告警 + 审批 |
| **Critical** | 极高风险 | 记录日志 + 告警 + 审批 + 人工确认 |

### 风险评分

```python
def calculate_risk_score(command: str) -> int:
    score = 0

    # 检查危险命令
    if contains_dangerous_command(command):
        score += 50

    # 检查敏感路径
    if accesses_sensitive_path(command):
        score += 30

    # 检查特殊字符
    if contains_special_chars(command):
        score += 20

    return min(score, 100)
```

## 最佳实践

### 1. 最小权限原则

```yaml
# 只授予必要的权限
security:
  allowed_commands:
    - ps
    - top
    - free
    - df
  blocked_commands:
    - rm
    - dd
    - mkfs
```

### 2. 审批流程

```yaml
approval:
  require_approval_for:
    - restart
    - delete
    - scale
    - upgrade
```

### 3. 定期审计

```bash
# 查看审计日志
aiops audit log --days 7

# 导出审计报告
aiops audit export --format csv
```

### 4. 密钥轮换

```bash
# 更新服务器密码
aiops config update-server-password --server production

# 更新 API Key
aiops config update-api-key --provider deepseek
```
