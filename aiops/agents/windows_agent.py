"""Windows Agent - Windows 系统运维专家"""
from .base import BaseAgent, AgentResult


class WindowsAgent(BaseAgent):
    """Windows Agent - 负责 Windows Server 运维"""

    name = "windows"
    description = "Windows Agent - Windows Server 运维"
    role = "Windows 运维专家"
    task_description = "处理 Windows Server 性能问题、IIS/AD/DNS/DHCP 管理、事件日志分析"
    tools = [
        "winrm_exec", "ssh_exec", "log_search", "http_get",
    ]
    max_steps = 12

    def run(self, task: str, context: dict = None) -> AgentResult:
        context = context or {}
        context["expertise"] = """你是 Windows Server 运维专家：
1. 系统管理: 服务、进程、计划任务、注册表
2. 性能分析: CPU/内存/磁盘/网络 (PerfMon/TaskManager)
3. IIS 管理: 网站/应用池/SSL/日志
4. Active Directory: 用户/组/组策略/GPO
5. DNS/DHCP: 域名解析/地址分配
6. 事件日志: 系统/应用/安全日志分析
7. PowerShell: 自动化脚本执行
8. Windows Update: 补丁管理

执行流程：
1. 通过 WinRM 连接目标 Windows 服务器
2. 执行 PowerShell 命令收集信息
3. 分析事件日志定位问题
4. 给出修复方案和验证步骤
"""
        return super().run(task, context)
