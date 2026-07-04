"""Virtual Agent - 虚拟化运维专家"""
from .base import BaseAgent, AgentResult


class VirtualAgent(BaseAgent):
    """Virtual Agent - 负责虚拟化平台管理"""

    name = "virtual"
    description = "Virtual Agent - 虚拟化运维（VMware/KVM/Xen/Hyper-V）"
    role = "虚拟化运维专家"
    task_description = "处理 VMware vSphere/KVM/Xen/Hyper-V 虚拟机管理、资源调度、快照备份"
    tools = [
        "ssh_exec", "http_get", "log_search",
    ]
    max_steps = 12

    def run(self, task: str, context: dict = None) -> AgentResult:
        context = context or {}
        context["expertise"] = """你是虚拟化运维专家：
1. VMware: vSphere/vCenter/ESXi 虚拟机管理
2. KVM/QEMU: libvirt 虚拟机生命周期管理
3. Xen: XenServer/XCP-ng 虚拟化
4. Hyper-V: Windows 虚拟化平台
5. Proxmox: 开源虚拟化平台
6. 资源管理: CPU/内存/存储/网络资源分配
7. 快照管理: 创建/恢复/删除快照
8. 迁移: 在线迁移/冷迁移/P2V/V2V
9. 高可用: HA/DRS/故障切换
10. 模板管理: 模板创建/克隆/部署

执行流程：
1. 连接虚拟化管理平台（API/CLI）
2. 查询虚拟机状态和资源使用
3. 执行管理操作（启停/迁移/快照）
4. 优化资源分配和性能
5. 验证操作结果
"""
        return super().run(task, context)
