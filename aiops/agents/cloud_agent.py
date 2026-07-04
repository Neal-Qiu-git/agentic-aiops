"""Cloud Agent - 多云管理专家"""
from .base import BaseAgent, AgentResult


class CloudAgent(BaseAgent):
    """Cloud Agent - 负责多云平台运维管理"""

    name = "cloud"
    description = "Cloud Agent - 多云平台运维（AWS/Azure/阿里云/腾讯云/华为云）"
    role = "多云运维专家"
    task_description = "处理公有云/私有云资源管理、成本优化、安全合规、跨云迁移"
    tools = [
        "aws_cli", "azure_cli", "aliyun_cli", "tencent_cli", "huawei_cli",
        "ssh_exec", "http_get",
    ]
    max_steps = 15

    def run(self, task: str, context: dict = None) -> AgentResult:
        context = context or {}
        context["expertise"] = """你是多云运维专家，覆盖：
1. AWS: EC2/S3/RDS/Lambda/CloudWatch/IAM/VPC
2. Azure: VM/Blob/AKS/AD/NSG/Monitor
3. 阿里云: ECS/OSS/RDS/SLB/ACK/STS
4. 腾讯云: CVM/COS/CDB/CLB/TKE/CAM
5. 华为云: ECS/OBS/RDS/ELB/CCE/IAM

执行流程：
1. 识别任务涉及的云平台
2. 使用对应 CLI 工具查询/操作资源
3. 跨云对比分析，给出最优方案
4. 关注成本、安全、合规
"""
        return super().run(task, context)
