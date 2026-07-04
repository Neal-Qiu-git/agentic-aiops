# 记忆系统 (Memory)

## 概述

Memory 系统让 Agent 具备持续学习能力，能够记住历史经验并在未来复用。

## 记忆类型

### 1. Working Memory (工作记忆)

当前会话的上下文信息。

```python
# 自动管理
- 当前任务
- 对话历史
- 中间结果
```

### 2. Short-term Memory (短期记忆)

近期的对话和操作记录，有 TTL 限制。

```python
# 默认 TTL: 1小时
- 最近的诊断记录
- 最近的工具调用
- 最近的决策
```

### 3. Long-term Memory (长期记忆)

持久化存储的重要信息。

```python
# 永久存储
- 故障经验
- 修复方案
- 最佳实践
```

### 4. Semantic Memory (语义记忆)

基于向量检索的语义记忆。

```python
# 向量索引
- 故障模式
- 解决方案
- 相似案例
```

### 5. Episodic Memory (情景记忆)

具体的运维事件记录。

```python
# 事件记录
- 故障事件
- 操作记录
- 决策历史
```

## 使用示例

### 记录故障经验

```bash
# 自动记录
aiops agent linux --host 10.0.0.1 --symptom "CPU 高"

# 手动记录
aiops memory add --type fault --content "Redis 连接池耗尽"
```

### 搜索记忆

```bash
# 搜索类似故障
aiops memory search "Redis 连接问题"

# 按类型搜索
aiops memory search --type fault --keyword "OOM"
```

### 查看统计

```bash
aiops memory stats
```

输出：
```
Memory Statistics
├── Short-term: 45 entries
├── Long-term: 128 entries
├── Semantic: 56 entries
└── Episodic: 89 entries
```

## 记忆流程

```
Agent 执行任务
    │
    ▼
记录操作步骤
    │
    ▼
记录执行结果
    │
    ▼
记录成功/失败
    │
    ▼
更新语义索引
    │
    ▼
下次遇到类似问题
    │
    ▼
检索相关记忆
    │
    ▼
复用成功经验
```
