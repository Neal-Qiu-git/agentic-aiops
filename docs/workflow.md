# Workflow 引擎

## 概述

Workflow Engine 支持使用 YAML 编排运维流程，实现可复用、可视化的运维自动化。

## YAML 格式

```yaml
name: cpu-diagnosis
description: CPU 高诊断流程

steps:
  - name: check_cpu
    action: ssh_exec
    command: "top -bn1 | head -20"
    timeout: 10

  - name: check_process
    action: ssh_exec
    command: "ps aux --sort=-%cpu | head -10"
    depends_on: check_cpu

  - name: analyze
    action: ai_analyze
    input: "{{check_cpu.output}} {{check_process.output}}"
    depends_on: [check_cpu, check_process]

  - name: notify
    action: send_notification
    message: "{{analyze.result}}"
    condition: "analyze.severity == 'high'"
    depends_on: analyze
```

## 步骤类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **action** | 执行动作 | ssh_exec, k8s_get_pods |
| **condition** | 条件判断 | if/else 逻辑 |
| **parallel** | 并行执行 | 同时检查多个服务 |
| **loop** | 循环执行 | 批量处理 |
| **human** | 人工审批 | 等待确认 |
| **subworkflow** | 子工作流 | 调用其他流程 |

## 使用示例

### 执行工作流

```bash
# 执行预定义工作流
aiops workflow run cpu-diagnosis --host 10.0.0.1

# 执行自定义工作流
aiops workflow run -f my-workflow.yaml
```

### 管理工作流

```bash
# 列出所有工作流
aiops workflow list

# 查看工作流详情
aiops workflow info cpu-diagnosis

# 查看执行历史
aiops workflow history cpu-diagnosis
```

## 内置工作流

| 工作流 | 说明 |
|--------|------|
| cpu-diagnosis | CPU 高诊断 |
| memory-leak | 内存泄漏诊断 |
| disk-full | 磁盘满诊断 |
| pod-troubleshoot | K8s Pod 故障排查 |
| redis-diagnose | Redis 连接诊断 |
| mysql-slow-query | MySQL 慢查询分析 |

## 自定义工作流

### 模板

```yaml
name: my-workflow
description: 自定义工作流

# 全局配置
config:
  timeout: 300
  retry: 3

# 变量定义
variables:
  service_name: "my-service"
  threshold: 80

# 步骤定义
steps:
  - name: step1
    action: ssh_exec
    command: "systemctl status {{service_name}}"
```

### 条件逻辑

```yaml
steps:
  - name: check
    action: ssh_exec
    command: "free -m | grep Mem | awk '{print $3/$2 * 100}'"

  - name: high_memory
    action: ssh_exec
    command: "echo 'Memory high'"
    condition: "check.output > {{threshold}}"

  - name: normal
    action: ssh_exec
    command: "echo 'Memory normal'"
    condition: "check.output <= {{threshold}}"
```

### 并行执行

```yaml
steps:
  - name: parallel_check
    parallel:
      - name: check_cpu
        action: ssh_exec
        command: "top -bn1 | grep 'Cpu(s)'"
      - name: check_memory
        action: ssh_exec
        command: "free -m"
      - name: check_disk
        action: ssh_exec
        command: "df -h"
```
