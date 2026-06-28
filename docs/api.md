# API 文档

## 概述

Agentic AIOps 提供 RESTful API 接口，支持与其他系统集成。

## 启动 API 服务

```bash
aiops api start --host 0.0.0.0 --port 8000
```

## API 端点

### 诊断接口

#### POST /api/v1/diagnose

执行诊断任务。

**请求体：**

```json
{
  "host": "10.0.0.1",
  "symptom": "CPU 高",
  "agent": "linux"
}
```

**响应：**

```json
{
  "task_id": "task_abc123",
  "status": "completed",
  "result": {
    "root_cause": "Java 进程 GC 频繁",
    "suggestion": "增大 JVM 堆内存",
    "confidence": 0.85
  }
}
```

### Agent 接口

#### GET /api/v1/agents

列出所有 Agent。

**响应：**

```json
{
  "agents": [
    {
      "name": "linux",
      "description": "系统运维 Agent",
      "status": "ready"
    }
  ]
}
```

#### POST /api/v1/agents/{agent}/run

运行指定 Agent。

**请求体：**

```json
{
  "task": "检查 CPU 使用率",
  "context": {
    "host": "10.0.0.1"
  }
}
```

### 工具接口

#### GET /api/v1/tools

列出所有工具。

#### POST /api/v1/tools/{tool}/execute

执行指定工具。

**请求体：**

```json
{
  "params": {
    "command": "uptime",
    "host": "10.0.0.1"
  }
}
```

### 工作流接口

#### GET /api/v1/workflows

列出所有工作流。

#### POST /api/v1/workflows/{name}/run

运行指定工作流。

**请求体：**

```json
{
  "variables": {
    "host": "10.0.0.1"
  }
}
```

#### GET /api/v1/workflows/{id}/status

查询工作流执行状态。

### 知识库接口

#### GET /api/v1/knowledge

列出知识条目。

#### POST /api/v1/knowledge/search

搜索知识库。

**请求体：**

```json
{
  "query": "Redis 连接问题",
  "type": "runbook",
  "limit": 10
}
```

### 记忆接口

#### GET /api/v1/memory/stats

获取记忆统计。

#### POST /api/v1/memory/search

搜索记忆。

### 审批接口

#### GET /api/v1/approvals

列出待审批请求。

#### POST /api/v1/approvals/{id}/approve

批准请求。

#### POST /api/v1/approvals/{id}/reject

拒绝请求。

## 认证

### API Key 认证

```bash
curl -H "Authorization: Bearer your-api-key" \
     http://localhost:8000/api/v1/diagnose
```

### 配置

```yaml
api:
  enabled: true
  host: 0.0.0.0
  port: 8000
  auth:
    type: api_key
    keys:
      - name: admin
        key: your-api-key
        permissions: ["read", "write"]
```

## 错误处理

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Missing required parameter: host"
  }
}
```

## 速率限制

```yaml
api:
  rate_limit:
    requests_per_minute: 60
    burst: 10
```
