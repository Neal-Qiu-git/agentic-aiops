# Agentic AIOps API 文档

> **Base URL:** `http://localhost:8000/api/v1`
>
> **Content-Type:** `application/json`
>
> **认证方式:** Bearer Token / API Key

---

## 📋 目录

- [快速开始](#-快速开始)
- [认证](#-认证)
- [健康检查](#-健康检查)
- [诊断接口](#-诊断接口)
- [智能体接口](#-智能体接口)
- [工具接口](#-工具接口)
- [工作流接口](#-工作流接口)
- [知识库接口](#-知识库接口)
- [记忆系统接口](#-记忆系统接口)
- [审批接口](#-审批接口)
- [事件总线接口](#-事件总线接口)
- [错误码](#-错误码)

---

## 🚀 快速开始

### 启动服务

```bash
# 默认端口 8000
aiops api start

# 自定义端口
aiops api start --host 0.0.0.0 --port 9000
```

### 第一次调用

```bash
# 健康检查
curl http://localhost:8000/api/v1/health

# 查看版本
curl http://localhost:8000/api/v1/version

# 执行诊断
curl -X POST http://localhost:8000/api/v1/diagnose \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"host":"10.0.0.1","symptom":"CPU使用率过高"}'
```

### Python SDK 调用

```python
import requests

API = "http://localhost:8000/api/v1"
HEADERS = {"Authorization": "Bearer your-api-key"}

# 健康检查
r = requests.get(f"{API}/health", headers=HEADERS)
print(r.json())  # {"status": "healthy"}

# 执行诊断
r = requests.post(f"{API}/diagnose", headers=HEADERS, json={
    "host": "10.0.0.1",
    "symptom": "CPU使用率过高",
    "agent": "linux"
})
print(r.json())
```

---

## 🔐 认证

### API Key 认证（推荐）

在请求头中添加 `Authorization` 字段：

```bash
curl -H "Authorization: Bearer your-api-key" \
     http://localhost:8000/api/v1/diagnose
```

### 配置 API Key

编辑 `config.yaml`：

```yaml
api:
  enabled: true
  host: 0.0.0.0
  port: 8000
  auth:
    type: api_key
    keys:
      - name: admin
        key: your-admin-key
        permissions: ["read", "write", "execute"]
      - name: readonly
        key: your-readonly-key
        permissions: ["read"]
```

### 权限说明

| 权限 | 说明 |
|------|------|
| `read` | 读取 Agent、工具、工作流信息 |
| `write` | 创建/更新知识库、记忆 |
| `execute` | 执行诊断、工具、工作流 |

---

## 💓 健康检查

### GET /api/v1/health

检查 API 服务是否正常运行。

**无需认证。**

**响应示例：**

```json
{
  "status": "healthy",
  "timestamp": "2026-07-04T10:30:00Z",
  "version": "4.2.0",
  "uptime": 3600
}
```

### GET /api/v1/version

获取当前版本信息。

**响应示例：**

```json
{
  "version": "4.2.0",
  "python": "3.12.3",
  "platform": "linux"
}
```

---

## 🔍 诊断接口

### POST /api/v1/diagnose

执行一次完整的诊断任务，自动选择合适的 Agent 并运行 ReAct 循环。

**请求参数：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `host` | string | ✅ | 目标主机 IP 或域名 |
| `symptom` | string | ❌ | 症状描述，如 "CPU 高"、"服务超时" |
| `agent` | string | ❌ | 指定 Agent（不指定则自动选择） |
| `context` | object | ❌ | 额外上下文信息 |
| `timeout` | integer | ❌ | 超时时间（秒），默认 300 |

**请求示例：**

```bash
curl -X POST http://localhost:8000/api/v1/diagnose \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "10.0.0.1",
    "symptom": "CPU 使用率持续 95%，服务响应慢",
    "agent": "linux",
    "context": {
      "service": "nginx",
      "port": 80
    },
    "timeout": 120
  }'
```

**响应示例：**

```json
{
  "task_id": "task_abc123",
  "status": "completed",
  "host": "10.0.0.1",
  "symptom": "CPU 使用率持续 95%，服务响应慢",
  "result": {
    "root_cause": "Java 进程 Full GC 频繁，消耗 80% CPU",
    "suggestion": "增大 JVM 堆内存 -Xmx4g → 8g",
    "confidence": 0.94,
    "severity": "high",
    "category": "performance"
  },
  "steps": [
    {"step": 1, "action": "top -bn1 | head -20", "result": "Java PID 12345 占用 78% CPU"},
    {"step": 2, "action": "jstat -gc 12345", "result": "Full GC 次数: 42, 耗时: 35s"},
    {"step": 3, "action": "jmap -heap 12345", "result": "Heap Used 98%"}
  ],
  "duration_ms": 8500,
  "agent_used": "linux"
}
```

**状态说明：**

| status | 说明 |
|--------|------|
| `completed` | 诊断完成，已找到根因 |
| `partial` | 部分完成，置信度较低 |
| `failed` | 诊断失败 |
| `timeout` | 超时未完成 |

---

## 🤖 智能体接口

### GET /api/v1/agents

列出所有可用的智能体及其状态。

**响应示例：**

```json
{
  "agents": [
    {
      "name": "linux",
      "description": "Linux 系统运维",
      "status": "ready",
      "capabilities": ["system_diagnosis", "process_analysis", "performance_tuning"],
      "tools": ["ssh_exec", "top", "ps", "netstat"],
      "max_steps": 15,
      "model": "deepseek-chat"
    },
    {
      "name": "k8s",
      "description": "Kubernetes 运维",
      "status": "ready",
      "capabilities": ["pod_management", "service_debugging", "cluster_health"],
      "tools": ["k8s_get_pods", "k8s_get_nodes", "k8s_logs"],
      "max_steps": 15,
      "model": "deepseek-chat"
    },
    {
      "name": "db",
      "description": "数据库诊断",
      "status": "ready",
      "capabilities": ["slow_query", "connection_pool", "replication_check"],
      "tools": ["mysql_query", "redis_exec", "pg_query"],
      "max_steps": 12,
      "model": "deepseek-chat"
    },
    {
      "name": "log",
      "description": "日志分析",
      "status": "ready",
      "capabilities": ["log_search", "pattern_matching", "error_analysis"],
      "tools": ["grep_logs", "loki_query", "file_read"],
      "max_steps": 10,
      "model": "deepseek-chat"
    },
    {
      "name": "monitor",
      "description": "监控分析",
      "status": "ready",
      "capabilities": ["metric_analysis", "alert_investigation", "trend_prediction"],
      "tools": ["prometheus_query", "grafana_api"],
      "max_steps": 10,
      "model": "deepseek-chat"
    },
    {
      "name": "security",
      "description": "安全扫描",
      "status": "ready",
      "capabilities": ["vulnerability_scan", "config_audit", "intrusion_detection"],
      "tools": ["nmap_scan", "ssl_check", "file_permission"],
      "max_steps": 15,
      "model": "deepseek-chat"
    },
    {
      "name": "sre",
      "description": "SRE 运维",
      "status": "ready",
      "capabilities": ["sli_slo", "error_budget", "incident_response"],
      "tools": ["prometheus_query", "pagerduty_api"],
      "max_steps": 12,
      "model": "deepseek-chat"
    },
    {
      "name": "cost",
      "description": "成本优化",
      "status": "ready",
      "capabilities": ["resource_utilization", "rightsizing", "spend_analysis"],
      "tools": ["cloud_billing", "resource_inventory"],
      "max_steps": 10,
      "model": "deepseek-chat"
    },
    {
      "name": "incident",
      "description": "事件管理",
      "status": "ready",
      "capabilities": ["event_correlation", "escalation", "postmortem"],
      "tools": ["event_bus", "notification"],
      "max_steps": 12,
      "model": "deepseek-chat"
    },
    {
      "name": "devops",
      "description": "DevOps 运维",
      "status": "ready",
      "capabilities": ["ci_cd", "deployment", "rollback"],
      "tools": ["docker_exec", "helm_api", "git_ops"],
      "max_steps": 12,
      "model": "deepseek-chat"
    },
    {
      "name": "cmdb",
      "description": "配置管理",
      "status": "ready",
      "capabilities": ["asset_discovery", "dependency_analysis", "impact_assessment"],
      "tools": ["ssh_exec", "k8s_get_pods", "k8s_get_nodes"],
      "max_steps": 10,
      "model": "deepseek-chat"
    },
    {
      "name": "planner",
      "description": "任务规划",
      "status": "ready",
      "capabilities": ["task_decomposition", "dependency_planning", "resource_scheduling"],
      "tools": [],
      "max_steps": 8,
      "model": "deepseek-chat"
    }
  ]
}
```

### GET /api/v1/agents/{agent}

获取指定智能体的详细信息。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `agent` | string | 智能体名称 |

**响应示例：**

```json
{
  "name": "linux",
  "description": "Linux 系统运维",
  "status": "ready",
  "role": "Linux 系统运维专家",
  "task_description": "负责 Linux 服务器的系统诊断、性能分析、进程管理和故障排查",
  "tools": ["ssh_exec", "top", "ps", "netstat", "dmesg", "vmstat"],
  "max_steps": 15,
  "model": "deepseek-chat",
  "capabilities": [
    "CPU/内存/磁盘使用率分析",
    "进程异常检测",
    "网络连接诊断",
    "系统日志分析",
    "内核参数调优",
    "服务状态检查"
  ],
  "stats": {
    "total_tasks": 1247,
    "success_rate": 0.94,
    "avg_response_time_ms": 8500,
    "last_active": "2026-07-04T10:25:00Z"
  }
}
```

### POST /api/v1/agents/{agent}/run

运行指定智能体执行任务。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `agent` | string | 智能体名称 |

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `task` | string | ✅ | 任务描述 |
| `context` | object | ❌ | 上下文信息 |
| `timeout` | integer | ❌ | 超时（秒），默认 300 |

**请求示例：**

```bash
curl -X POST http://localhost:8000/api/v1/agents/linux/run \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "检查 10.0.0.1 的 CPU 和内存使用情况",
    "context": {"port": 22, "user": "root"},
    "timeout": 60
  }'
```

**响应示例：**

```json
{
  "task_id": "task_def456",
  "agent": "linux",
  "status": "completed",
  "result": {
    "answer": "CPU 使用率 23%，内存使用率 67%，系统运行正常",
    "steps": [
      {"step": 1, "action": "top -bn1", "result": "CPU idle: 77%"},
      {"step": 2, "action": "free -h", "result": "Mem: 16G total, 10.7G used"}
    ],
    "tool_calls": ["ssh_exec:top", "ssh_exec:free"],
    "success": true
  },
  "duration_ms": 5200
}
```

---

## 🔧 工具接口

### GET /api/v1/tools

列出所有可用工具。

**响应示例：**

```json
{
  "tools": [
    {
      "name": "ssh_exec",
      "description": "SSH 远程执行命令",
      "category": "system",
      "params": {
        "host": {"type": "string", "required": true},
        "command": {"type": "string", "required": true},
        "user": {"type": "string", "default": "root"},
        "port": {"type": "integer", "default": 22}
      }
    },
    {
      "name": "mysql_query",
      "description": "MySQL 查询",
      "category": "database",
      "params": {
        "host": {"type": "string", "required": true},
        "query": {"type": "string", "required": true},
        "database": {"type": "string", "required": true}
      }
    },
    {
      "name": "prometheus_query",
      "description": "Prometheus 指标查询",
      "category": "monitoring",
      "params": {
        "query": {"type": "string", "required": true},
        "start": {"type": "string", "required": false},
        "end": {"type": "string", "required": false}
      }
    }
  ]
}
```

**工具分类：**

| 分类 | 工具 | 说明 |
|------|------|------|
| `system` | ssh_exec, docker_exec | 系统命令执行 |
| `database` | mysql_query, redis_exec, pg_query | 数据库操作 |
| `monitoring` | prometheus_query, grafana_api | 监控查询 |
| `cloud` | aws_ec2, aliyun_ecs, tencent_cvm | 云资源管理 |
| `network` | http_request, dns_lookup, ping_check | 网络诊断 |
| `log` | grep_logs, loki_query | 日志检索 |

### POST /api/v1/tools/execute

执行指定工具。

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `tool` | string | ✅ | 工具名称 |
| `params` | object | ✅ | 工具参数 |

**请求示例：**

```bash
curl -X POST http://localhost:8000/api/v1/tools/execute \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "ssh_exec",
    "params": {
      "host": "10.0.0.1",
      "command": "df -h",
      "user": "root"
    }
  }'
```

**响应示例：**

```json
{
  "tool": "ssh_exec",
  "status": "success",
  "result": {
    "output": "Filesystem      Size  Used Avail Use% Mounted on\n/dev/vda1        40G   28G   10G  74% /",
    "exit_code": 0,
    "duration_ms": 1200
  }
}
```

---

## ⚡ 工作流接口

### GET /api/v1/workflows

列出所有可用工作流。

**响应示例：**

```json
{
  "workflows": [
    {
      "name": "cpu-high-diagnosis",
      "description": "CPU 高使用率诊断流程",
      "steps": 5,
      "status": "active",
      "triggers": ["manual", "alert"],
      "last_run": "2026-07-04T09:00:00Z"
    },
    {
      "name": "pod-crash-recovery",
      "description": "K8s Pod 崩溃自动恢复",
      "steps": 8,
      "status": "active",
      "triggers": ["alert", "webhook"],
      "last_run": "2026-07-04T08:30:00Z"
    },
    {
      "name": "incident-response",
      "description": "事件响应自动化流程",
      "steps": 12,
      "status": "active",
      "triggers": ["manual"],
      "last_run": "2026-07-03T15:00:00Z"
    }
  ]
}
```

### POST /api/v1/workflows/run

运行指定工作流。

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `workflow` | string | ✅ | 工作流名称 |
| `variables` | object | ❌ | 工作流变量 |
| `dry_run` | boolean | ❌ | 仅模拟运行，默认 false |

**请求示例：**

```bash
curl -X POST http://localhost:8000/api/v1/workflows/run \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow": "cpu-high-diagnosis",
    "variables": {
      "host": "10.0.0.1",
      "threshold": 90
    }
  }'
```

**响应示例：**

```json
{
  "run_id": "run_xyz789",
  "workflow": "cpu-high-diagnosis",
  "status": "started",
  "started_at": "2026-07-04T10:30:00Z",
  "estimated_duration_ms": 30000
}
```

### GET /api/v1/workflows/{run_id}/status

查询工作流执行状态。

**响应示例：**

```json
{
  "run_id": "run_xyz789",
  "workflow": "cpu-high-diagnosis",
  "status": "completed",
  "started_at": "2026-07-04T10:30:00Z",
  "completed_at": "2026-07-04T10:30:28Z",
  "duration_ms": 28000,
  "steps": [
    {"name": "收集系统信息", "status": "completed", "duration_ms": 2000},
    {"name": "分析 CPU 使用率", "status": "completed", "duration_ms": 5000},
    {"name": "检查进程列表", "status": "completed", "duration_ms": 3000},
    {"name": "诊断根因", "status": "completed", "duration_ms": 8000},
    {"name": "生成报告", "status": "completed", "duration_ms": 1000}
  ],
  "result": {
    "root_cause": "Java GC 频繁",
    "recommendation": "增大 JVM 堆内存"
  }
}
```

---

## 📚 知识库接口

### GET /api/v1/knowledge

列出知识库条目。

**查询参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `type` | string | `all` | 类型：runbook / incident / document |
| `limit` | integer | `20` | 每页数量 |
| `offset` | integer | `0` | 偏移量 |

**响应示例：**

```json
{
  "total": 156,
  "items": [
    {
      "id": "kb_001",
      "title": "Redis 连接超时处理",
      "type": "runbook",
      "tags": ["redis", "timeout", "connection"],
      "summary": "Redis 连接超时的标准排查流程：检查连接池、网络延迟、慢查询",
      "created_at": "2026-06-01T10:00:00Z",
      "updated_at": "2026-07-01T15:00:00Z"
    }
  ]
}
```

### POST /api/v1/knowledge/search

语义搜索知识库。

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✅ | 搜索关键词 |
| `type` | string | ❌ | 限定类型 |
| `limit` | integer | ❌ | 返回数量，默认 10 |
| `threshold` | float | ❌ | 相似度阈值，默认 0.7 |

**请求示例：**

```bash
curl -X POST http://localhost:8000/api/v1/knowledge/search \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Redis 连接池耗尽",
    "type": "runbook",
    "limit": 5
  }'
```

**响应示例：**

```json
{
  "query": "Redis 连接池耗尽",
  "total": 3,
  "results": [
    {
      "id": "kb_001",
      "title": "Redis 连接超时处理",
      "type": "runbook",
      "score": 0.92,
      "content": "## Redis 连接超时处理\n\n### 排查步骤\n1. 检查 maxclients 配置...",
      "tags": ["redis", "timeout", "connection"]
    },
    {
      "id": "kb_002",
      "title": "连接池配置最佳实践",
      "type": "document",
      "score": 0.85,
      "content": "## 连接池配置\n\n### 推荐配置\n- min_idle: 10\n- max_idle: 50...",
      "tags": ["pool", "config", "best-practice"]
    }
  ]
}
```

---

## 🧠 记忆系统接口

### GET /api/v1/memory/stats

获取记忆系统统计信息。

**响应示例：**

```json
{
  "total_memories": 1247,
  "by_type": {
    "working": 15,
    "short_term": 89,
    "long_term": 567,
    "semantic": 312,
    "episodic": 264
  },
  "storage_size_mb": 45.2,
  "last_cleanup": "2026-07-04T03:00:00Z"
}
```

### POST /api/v1/memory/search

搜索记忆。

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✅ | 搜索关键词 |
| `type` | string | ❌ | 限定记忆类型 |
| `limit` | integer | ❌ | 返回数量，默认 10 |

**请求示例：**

```bash
curl -X POST http://localhost:8000/api/v1/memory/search \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"query":"Redis 连接问题的修复经验","limit":5}'
```

**响应示例：**

```json
{
  "query": "Redis 连接问题的修复经验",
  "total": 3,
  "results": [
    {
      "id": "mem_abc",
      "type": "episodic",
      "content": "2026-06-15: Redis 连接超时，原因是 maxclients 设置过低，调整为 10000 后恢复",
      "score": 0.88,
      "created_at": "2026-06-15T14:30:00Z",
      "source": "incident_response"
    }
  ]
}
```

---

## ✅ 审批接口

### GET /api/v1/approvals

列出待审批请求。

**查询参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `status` | string | `pending` | 状态：pending / approved / rejected |
| `limit` | integer | `20` | 每页数量 |

**响应示例：**

```json
{
  "total": 2,
  "requests": [
    {
      "id": "apr_001",
      "type": "command",
      "title": "重启 Nginx 服务",
      "description": "Nginx 进程异常，需要重启",
      "command": "systemctl restart nginx",
      "risk_level": "low",
      "status": "pending",
      "requested_by": "linux_agent",
      "created_at": "2026-07-04T10:25:00Z"
    },
    {
      "id": "apr_002",
      "type": "command",
      "title": "删除临时文件",
      "description": "清理 /tmp 下超过 7 天的文件",
      "command": "find /tmp -mtime +7 -delete",
      "risk_level": "high",
      "status": "pending",
      "requested_by": "devops_agent",
      "created_at": "2026-07-04T10:28:00Z"
    }
  ]
}
```

### POST /api/v1/approvals/create

创建审批请求。

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `title` | string | ✅ | 审批标题 |
| `command` | string | ✅ | 待执行命令 |
| `description` | string | ❌ | 详细描述 |
| `risk_level` | string | ❌ | 风险等级：low / medium / high，默认 medium |

**请求示例：**

```bash
curl -X POST http://localhost:8000/api/v1/approvals/create \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "重启 Nginx 服务",
    "command": "systemctl restart nginx",
    "description": "Nginx 进程异常，需要重启恢复服务",
    "risk_level": "low"
  }'
```

**响应示例：**

```json
{
  "request_id": "apr_003",
  "status": "pending",
  "created_at": "2026-07-04T10:30:00Z"
}
```

### POST /api/v1/approvals/{id}/approve

批准请求。

```bash
curl -X POST http://localhost:8000/api/v1/approvals/apr_001/approve \
  -H "Authorization: Bearer your-api-key"
```

**响应：**

```json
{
  "request_id": "apr_001",
  "status": "approved",
  "approved_at": "2026-07-04T10:35:00Z",
  "executed": true
}
```

### POST /api/v1/approvals/{id}/reject

拒绝请求。

```bash
curl -X POST http://localhost:8000/api/v1/approvals/apr_002/reject \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"reason":"风险太高，需要人工确认"}'
```

**响应：**

```json
{
  "request_id": "apr_002",
  "status": "rejected",
  "reason": "风险太高，需要人工确认",
  "rejected_at": "2026-07-04T10:36:00Z"
}
```

---

## 📡 事件总线接口

### GET /api/v1/events

获取事件列表。

**查询参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `level` | string | `all` | 级别：info / warning / error / critical |
| `source` | string | `all` | 来源：agent / workflow / system |
| `limit` | integer | `50` | 返回数量 |
| `since` | string | — | 起始时间（ISO 8601） |

**响应示例：**

```json
{
  "total": 1247,
  "events": [
    {
      "id": "evt_001",
      "level": "error",
      "source": "agent:linux",
      "title": "CPU 使用率超阈值",
      "message": "10.0.0.1 CPU 使用率 95%，已触发诊断",
      "metadata": {"host": "10.0.0.1", "cpu_percent": 95},
      "timestamp": "2026-07-04T10:30:00Z"
    },
    {
      "id": "evt_002",
      "level": "info",
      "source": "workflow:cpu-high",
      "title": "诊断工作流完成",
      "message": "根因：Java GC 频繁",
      "metadata": {"workflow": "cpu-high-diagnosis"},
      "timestamp": "2026-07-04T10:30:28Z"
    }
  ]
}
```

### POST /api/v1/events/emit

发布事件到事件总线。

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `level` | string | ✅ | 事件级别 |
| `title` | string | ✅ | 事件标题 |
| `message` | string | ❌ | 详细信息 |
| `source` | string | ❌ | 事件来源 |
| `metadata` | object | ❌ | 元数据 |

**请求示例：**

```bash
curl -X POST http://localhost:8000/api/v1/events/emit \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "level": "warning",
    "title": "磁盘空间不足",
    "message": "/data 分区使用率 85%",
    "source": "monitor:prometheus",
    "metadata": {"host": "10.0.0.1", "disk_percent": 85, "mount": "/data"}
  }'
```

---

## ❌ 错误码

| HTTP 状态码 | 错误码 | 说明 |
|:-----------:|--------|------|
| 400 | `INVALID_REQUEST` | 请求参数错误 |
| 400 | `MISSING_FIELD` | 缺少必填字段 |
| 401 | `UNAUTHORIZED` | 未认证或 Token 无效 |
| 403 | `FORBIDDEN` | 权限不足 |
| 404 | `NOT_FOUND` | 资源不存在 |
| 429 | `RATE_LIMITED` | 请求频率超限 |
| 500 | `INTERNAL_ERROR` | 服务器内部错误 |
| 503 | `SERVICE_UNAVAILABLE` | 服务不可用 |

**错误响应格式：**

```json
{
  "error": {
    "code": "MISSING_FIELD",
    "message": "缺少必填参数: host",
    "details": {
      "field": "host",
      "expected": "string"
    }
  }
}
```

---

## ⏱️ 速率限制

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `requests_per_minute` | 60 | 每分钟最大请求数 |
| `burst` | 10 | 突发请求上限 |

**响应头：**

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1688470800
```

---

## 📎 附录：完整 API 端点一览

| 方法 | 路径 | 说明 | 认证 |
|:----:|------|------|:----:|
| GET | `/api/v1/health` | 健康检查 | ❌ |
| GET | `/api/v1/version` | 版本信息 | ❌ |
| POST | `/api/v1/diagnose` | 执行诊断 | ✅ |
| GET | `/api/v1/agents` | 列出智能体 | ✅ |
| GET | `/api/v1/agents/{agent}` | 智能体详情 | ✅ |
| POST | `/api/v1/agents/{agent}/run` | 运行智能体 | ✅ |
| GET | `/api/v1/tools` | 列出工具 | ✅ |
| POST | `/api/v1/tools/execute` | 执行工具 | ✅ |
| GET | `/api/v1/workflows` | 列出工作流 | ✅ |
| POST | `/api/v1/workflows/run` | 运行工作流 | ✅ |
| GET | `/api/v1/workflows/{id}/status` | 工作流状态 | ✅ |
| GET | `/api/v1/knowledge` | 列出知识库 | ✅ |
| POST | `/api/v1/knowledge/search` | 搜索知识库 | ✅ |
| GET | `/api/v1/memory/stats` | 记忆统计 | ✅ |
| POST | `/api/v1/memory/search` | 搜索记忆 | ✅ |
| GET | `/api/v1/approvals` | 列出审批 | ✅ |
| POST | `/api/v1/approvals/create` | 创建审批 | ✅ |
| POST | `/api/v1/approvals/{id}/approve` | 批准 | ✅ |
| POST | `/api/v1/approvals/{id}/reject` | 拒绝 | ✅ |
| GET | `/api/v1/events` | 事件列表 | ✅ |
| POST | `/api/v1/events/emit` | 发布事件 | ✅ |
