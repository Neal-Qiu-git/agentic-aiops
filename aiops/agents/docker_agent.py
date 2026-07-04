"""Docker Agent - 容器运维专家"""
from .base import BaseAgent, AgentResult


class DockerAgent(BaseAgent):
    """Docker Agent - 负责容器管理和 Docker 问题排查"""

    name = "docker"
    description = "Docker Agent - 容器运维专家"
    role = "容器运维专家"
    task_description = "处理 Docker 容器管理、镜像构建、Compose 编排、网络和存储管理"
    tools = [
        "docker_ps",
        "docker_logs",
        "docker_inspect",
        "docker_stats",
        "docker_compose",
        "docker_network",
        "docker_volume",
        "ssh_exec",
    ]
    max_steps = 12

    def run(self, task: str, context: dict = None) -> AgentResult:
        """执行 Docker 运维任务"""
        context = context or {}

        prompt = f"""作为 Docker 容器运维专家，请处理以下任务：

任务：{task}

你的专业领域：
1. 容器生命周期管理：创建、启动、停止、重启、删除容器
2. 镜像管理：构建、拉取、推送、清理镜像
3. Docker Compose：多容器应用编排、服务管理
4. 网络管理：容器网络配置、端口映射、DNS
5. 存储管理：数据卷、绑定挂载、存储驱动
6. 性能分析：容器资源使用、日志分析、故障排查
7. 安全检查：容器权限、镜像漏洞、配置审计

执行流程：
1. 分析任务需求，确定需要哪些 Docker 操作
2. 使用 docker_ps 查看当前容器状态
3. 根据需要使用 docker_logs/docker_inspect/docker_stats 获取详细信息
4. 执行具体操作（docker_compose/docker_network/docker_volume）
5. 验证操作结果，给出完整报告

注意：
- 生产环境操作前先确认
- 保留关键容器的日志和状态
- 给出可执行的具体命令
"""
        context["expertise"] = prompt
        return super().run(task, context)
