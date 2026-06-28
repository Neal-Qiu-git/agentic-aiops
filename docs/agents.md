# Agent 指南

## Agent 列表

| Agent | 职责 | 能力 |
|-------|------|------|
| **Planner Agent** | 总控协调 | 任务分解、Agent调度、结果聚合 |
| **Linux Agent** | 系统运维 | CPU/内存/磁盘/网络/进程诊断 |
| **K8s Agent** | 容器运维 | Pod/Deployment/Service/Node 管理 |
| **DB Agent** | 数据库运维 | MySQL/Redis/PostgreSQL/MongoDB 诊断 |
| **Log Agent** | 日志分析 | 日志搜索、错误追踪、链路分析 |
| **Monitor Agent** | 监控分析 | Prometheus/Grafana 指标分析 |
| **Security Agent** | 安全运维 | 漏洞扫描、合规检查、入侵检测 |
| **DevOps Agent** | DevOps | CI/CD、发布管理、版本控制 |
| **SRE Agent** | SRE | SLI/SLO/SLA/Error Budget 管理 |
| **Incident Agent** | 故障管理 | 故障响应、Timeline、RCA 报告 |
| **Cost Agent** | 成本优化 | 云资源分析、闲置资源、优化建议 |
| **CMDB Agent** | 配置管理 | 资产发现、依赖关系、影响分析 |

---

## Agent 架构

### BaseAgent

所有 Agent 继承自 BaseAgent，实现 ReAct 循环：

```python
class BaseAgent(ABC):
    def run(self, task: str, context: Dict) -> AgentResult:
        # 1. Reason - 推理分析
        thought = self.think(task, context)

        # 2. Plan - 制定计划
        plan = self.plan(thought)

        # 3. Act - 执行动作
        for step in plan.steps:
            result = self.execute(step)
            context.update(result)

        # 4. Verify - 验证结果
        verification = self.verify(context)

        # 5. Learn - 学习总结
        self.learn(task, verification)

        return AgentResult(answer=verification.summary)
```

---

## Linux Agent

### 职责
系统层面的故障诊断和性能分析

### 能力
- CPU 使用率分析
- 内存泄漏检测
- 磁盘空间诊断
- 网络连接分析
- 进程管理
- 服务状态检查

### 使用示例

```bash
# CPU 诊断
aiops agent linux --host 10.0.0.1 --symptom "CPU 高"

# 内存诊断
aiops agent linux --host 10.0.0.1 --symptom "内存不足"

# 磁盘诊断
aiops agent linux --host 10.0.0.1 --symptom "磁盘满"
```

---

## K8s Agent

### 职责
Kubernetes 集群和工作负载管理

### 能力
- Pod 诊断（CrashLoopBackOff, OOMKilled, ImagePullBackOff）
- Deployment 管理（扩缩容、回滚）
- Service 排查
- Node 状态分析
- Namespace 管理

### 使用示例

```bash
# Pod 诊断
aiops agent k8s --symptom "Pod CrashLoopBackOff"

# Node 诊断
aiops agent k8s --symptom "Node NotReady"

# 查看 Pod 列表
aiops agent k8s --action get-pods --namespace default
```

---

## DB Agent

### 职责
数据库性能诊断和优化

### 能力
- MySQL 慢查询分析
- Redis 连接诊断
- PostgreSQL 性能优化
- MongoDB 集合分析
- Elasticsearch 索引优化

### 使用示例

```bash
# MySQL 慢查询
aiops agent db --type mysql --symptom "查询慢"

# Redis 连接问题
aiops agent db --type redis --symptom "连接超时"

# PostgreSQL 诊断
aiops agent db --type postgresql --symptom "性能差"
```

---

## Log Agent

### 职责
日志分析和错误追踪

### 能力
- 日志搜索和过滤
- 错误模式识别
- 链路追踪
- 日志聚合分析

### 使用示例

```bash
# 搜索错误日志
aiops agent log --host 10.0.0.1 --file /var/log/app.log --pattern "ERROR"

# 分析最近错误
aiops agent log --host 10.0.0.1 --hours 24 --level error
```

---

## SRE Agent

### 职责
SLO/SLI/SLA 管理和 Error Budget 追踪

### 能力
- SLI 定义和监控
- SLO 目标管理
- Error Budget 计算
- Burn Rate 告警
- 可用性报告

### 使用示例

```bash
# 查看 SLO 状态
aiops agent sre --action check-slo --service payment-api

# 计算 Error Budget
aiops agent sre --action error-budget --service order-api

# 生成可用性报告
aiops agent sre --action report --period 30d
```

---

## Incident Agent

### 职责
故障事件响应和管理

### 能力
- 故障检测和分类
- 响应团队通知
- Timeline 生成
- RCA 报告
- 故障复盘

### 使用示例

```bash
# 创建故障事件
aiops agent incident create --severity P1 --service payment

# 添加 Timeline 事件
aiops agent incident timeline --id INC-001 --event "开始修复"

# 生成 RCA 报告
aiops agent incident rca --id INC-001
```

---

## Cost Agent

### 职责
云资源成本优化

### 能力
- 闲置资源检测
- 资源使用率分析
- 成本优化建议
- Reserved Instance 推荐
- Spot Instance 策略

### 使用示例

```bash
# 分析 AWS 成本
aiops agent cost --provider aws --region us-east-1

# 检测闲置资源
aiops agent cost --action idle-resources --provider aliyun

# 生成优化报告
aiops agent cost --action optimize-report
```

---

## Multi-Agent 协同

### 任务分解

Planner Agent 会自动将复杂任务分解给多个 Agent：

```
用户: Pod CrashLoopBackOff

Planner Agent 分解:
├── K8s Agent: 查看 Pod 状态和事件
├── Log Agent: 分析 Pod 日志
├── Monitor Agent: 查看 Node 指标
└── Linux Agent: 检查 Node 系统状态
```

### 结果聚合

各 Agent 执行完成后，Planner Agent 聚合结果：

```
K8s Agent: OOMKilled
Log Agent: 内存使用超过限制
Monitor Agent: Node 内存正常
Linux Agent: Node 系统正常

结论: Pod 内存限制过小，建议增大
```
