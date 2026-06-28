# 知识库 (Knowledge)

## 概述

Knowledge 系统管理运维知识，支持 RAG 检索增强生成。

## 知识来源

| 来源 | 说明 | 用途 |
|------|------|------|
| **Runbook** | 运维剧本 | 标准化操作流程 |
| **Official Docs** | 官方文档 | 技术参考 |
| **GitHub Issues** | 社区问题 | 常见问题解答 |
| **StackOverflow** | 技术问答 | 最佳实践 |
| **Internal Wiki** | 内部文档 | 企业知识 |
| **CMDB** | 配置管理 | 资产信息 |

## 使用示例

### 添加知识

```bash
# 添加 Runbook
aiops knowledge add --type runbook --name "redis-connection" --file redis-connection.md

# 添加故障案例
aiops knowledge add --type case --content "Redis 连接池耗尽导致服务不可用"
```

### 搜索知识

```bash
# 关键词搜索
aiops knowledge search "Redis 连接问题"

# RAG 检索
aiops knowledge rag "为什么 Redis 连接失败"
```

### 查看知识库

```bash
aiops knowledge list --type runbook
aiops knowledge list --type case
```

## RAG 流程

```
用户问题
    │
    ▼
向量化查询
    │
    ▼
检索相关文档
    │
    ▼
上下文增强
    │
    ▼
LLM 生成答案
    │
    ▼
返回结果
```

## Runbook 格式

```markdown
# Redis 连接失败排查

## 症状
- 服务无法连接 Redis
- 连接超时错误

## 可能原因
1. Redis 服务未启动
2. 连接池耗尽
3. 网络问题
4. 防火墙阻断

## 排查步骤

### 1. 检查 Redis 状态
```bash
redis-cli ping
```

### 2. 检查连接数
```bash
redis-cli info clients
```

### 3. 检查网络
```bash
telnet redis-host 6379
```

## 解决方案
根据排查结果采取相应措施
```
