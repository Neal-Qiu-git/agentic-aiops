# MCP 工具市场

## 概述

MCP (Model Context Protocol) 工具市场提供插件化的工具管理，支持 20+ 工具。

## 工具分类

### 系统工具

| 工具 | 功能 | 安全级别 |
|------|------|----------|
| `ssh_exec` | SSH 远程执行 | 需要确认 |
| `system_check` | 系统状态检查 | 只读 |
| `process_list` | 进程列表 | 只读 |

### 容器工具

| 工具 | 功能 | 安全级别 |
|------|------|----------|
| `docker_ps` | 容器列表 | 只读 |
| `docker_logs` | 容器日志 | 只读 |
| `docker_stats` | 资源统计 | 只读 |
| `kubectl` | K8s 命令 | 部分需要确认 |
| `k8s_get_pods` | Pod 列表 | 只读 |
| `k8s_get_events` | 事件列表 | 只读 |

### 数据库工具

| 工具 | 功能 | 安全级别 |
|------|------|----------|
| `mysql_query` | MySQL 查询 | 只读 |
| `redis_query` | Redis 命令 | 只读 |
| `postgresql_query` | PostgreSQL 查询 | 只读 |
| `mongodb_query` | MongoDB 查询 | 只读 |
| `elasticsearch_query` | ES 查询 | 只读 |
| `kafka_query` | Kafka 管理 | 只读 |

### 云平台工具

| 工具 | 功能 | 安全级别 |
|------|------|----------|
| `aws_cli` | AWS CLI | 需要确认 |
| `aliyun_cli` | 阿里云 CLI | 需要确认 |
| `tencent_cli` | 腾讯云 CLI | 需要确认 |
| `terraform` | 基础设施管理 | 需要确认 |
| `ansible` | 自动化工具 | 需要确认 |
| `helm` | K8s 包管理 | 需要确认 |

## 使用示例

### 列出所有工具

```bash
aiops tools list
```

### 查看工具详情

```bash
aiops tools info ssh_exec
```

### 执行工具

```bash
# SSH 执行
aiops tools run ssh_exec --host 10.0.0.1 --command "uptime"

# K8s 查询
aiops tools run k8s_get_pods --namespace default

# Redis 查询
aiops tools run redis_query --command "info memory"
```

## 插件开发

### 创建自定义工具

```python
from aiops.tools import BaseTool, ToolResult

class MyCustomTool(BaseTool):
    name = "my_tool"
    description = "自定义工具"
    category = "custom"

    parameters = {
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
        },
        "required": ["param1"],
    }

    def execute(self, param1: str, **kwargs) -> ToolResult:
        # 实现逻辑
        return ToolResult(success=True, output="result")
```

### 注册工具

```python
from aiops.mcp import get_marketplace

marketplace = get_marketplace()
marketplace.register_tool(MyCustomTool())
```

## 插件市场

### 安装插件

```bash
aiops plugin install docker-tools
aiops plugin install redis-tools
aiops plugin install aws-tools
```

### 查看已安装插件

```bash
aiops plugin list
```

### 卸载插件

```bash
aiops plugin uninstall docker-tools
```
