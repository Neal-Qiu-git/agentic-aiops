"""云原生数据库 + 云成本扩展

DynamoDB: AWS 原生 NoSQL (Serverless)
GCP Cost: Google Cloud 成本分析
"""
import subprocess, json
from .base import BaseTool, ToolResult, ToolCategory


def _run(cmd: str, t: int = 20) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=t)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:5000], error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class DynamoDBTool(BaseTool):
    """AWS DynamoDB"""
    name = "dynamodb"
    description = "AWS DynamoDB NoSQL 数据库管理"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "tables/describe/scan/stats", "default": "tables"},
        "table": {"type": "string"},
        "region": {"type": "string", "default": "us-east-1"},
    }}

    def execute(self, action: str = "tables", table: str = "", region: str = "us-east-1", **kw) -> ToolResult:
        if action == "tables":
            return _run(f"aws dynamodb list-tables --region {region} --output json")
        if action == "describe" and table:
            return _run(f"aws dynamodb describe-table --table-name {table} --region {region} --output json")
        if action == "stats" and table:
            r = _run(f"aws dynamodb describe-table --table-name {table} --region {region} --output json")
            if r.success:
                try:
                    d = json.loads(r.output)["Table"]
                    r.output = f"Rows: {d.get('ItemCount',0)}, Size: {d.get('TableSizeBytes',0)/1024:.1f}KB"
                except Exception:
                    pass
            return r
        return _run(f"aws dynamodb list-tables --region {region} --output json")


class GCPCost(BaseTool):
    """GCP 成本分析"""
    name = "gcp_cost"
    description = "Google Cloud 成本和使用情况分析"
    category = ToolCategory.FINOPS
    parameters = {"type": "object", "properties": {
        "project": {"type": "string", "description": "GCP 项目 ID"},
    }}

    def execute(self, project: str = "", **kw) -> ToolResult:
        return _run("gcloud billing accounts list --format=json 2>/dev/null || echo 'gcloud billing not configured'")
