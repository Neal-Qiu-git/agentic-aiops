"""FinOps 工具 - 成本优化

Kubecost: K8s 成本可视化事实标准
OpenCost: CNCF 孵化项目，K8s 成本分配
云厂商成本 API: AWS Cost Explorer, 阿里云账单
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _finops_cmd(cmd: str, timeout: int = 30) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class KubecostAllocation(BaseTool):
    """Kubecost 资源分配"""
    name = "kubecost_allocation"
    description = "查询 K8s 命名空间/部署/Pod 的成本分配"
    category = ToolCategory.FINOPS
    parameters = {"type": "object", "properties": {
        "aggregate_by": {"type": "string", "description": "namespace/label/controller", "default": "namespace"},
        "window": {"type": "string", "description": "时间窗口 (如 1d, 7d, 30d)", "default": "1d"},
        "namespace": {"type": "string", "description": "过滤命名空间"},
    }}

    def execute(self, aggregate_by: str = "namespace", window: str = "1d",
                namespace: str = "", **kwargs) -> ToolResult:
        import os
        url = os.environ.get("KUBECOST_URL", "http://kubecost-cost-analyzer:9090")
        ns_filter = f"&namespace={namespace}" if namespace else ""
        cmd = (f"curl -s '{url}/model/allocation?aggregate={aggregate_by}"
               f"&window={window}{ns_filter}&accumulate=true'")
        return _finops_cmd(cmd)


class KubecostAssets(BaseTool):
    """Kubecost 资产 (节点/PV)"""
    name = "kubecost_assets"
    description = "查询 K8s 节点和持久卷的成本"
    category = ToolCategory.FINOPS
    parameters = {"type": "object", "properties": {
        "asset_type": {"type": "string", "description": "node/disk", "default": "node"},
        "window": {"type": "string", "default": "7d"},
    }}

    def execute(self, asset_type: str = "node", window: str = "7d", **kwargs) -> ToolResult:
        import os
        url = os.environ.get("KUBECOST_URL", "http://kubecost-cost-analyzer:9090")
        return _finops_cmd(f"curl -s '{url}/model/assets?type={asset_type}&window={window}'")


class AWSCostExplorer(BaseTool):
    """AWS 成本分析"""
    name = "aws_cost"
    description = "查询 AWS 成本和使用情况"
    category = ToolCategory.FINOPS
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "daily/monthly/service/reserved", "default": "monthly"},
        "period": {"type": "string", "description": "时间周期 (如 2024-01-01:2024-12-31)"},
    }}

    def execute(self, action: str = "monthly", period: str = "", **kwargs) -> ToolResult:
        import time
        if not period:
            now = time.strftime("%Y-%m-%d")
            period = f"2024-01-01:{now}"
        if action == "daily":
            cmd = f"aws ce get-cost-and-usage --time-period Start={period.split(':')[0]},End={period.split(':')[1]} " \
                  f"--granularity DAILY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE"
        elif action == "service":
            cmd = f"aws ce get-cost-and-usage --time-period Start={period.split(':')[0]},End={period.split(':')[1]} " \
                  f"--granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE"
        else:
            cmd = f"aws ce get-cost-and-usage --time-period Start={period.split(':')[0]},End={period.split(':')[1]} " \
                  f"--granularity MONTHLY --metrics UnblendedCost"
        return _finops_cmd(cmd)


class AzureCost(BaseTool):
    """Azure 成本分析"""
    name = "azure_cost"
    description = "查询 Azure 消费和成本"
    category = ToolCategory.FINOPS
    parameters = {"type": "object", "properties": {
        "period": {"type": "string", "description": "月份 (如 2024-01)"},
    }}

    def execute(self, period: str = "", **kwargs) -> ToolResult:
        if not period:
            import time
            period = time.strftime("%Y-%m")
        return _finops_cmd(f"az cost management query --type ActualCost --time-period {period} -o json")
