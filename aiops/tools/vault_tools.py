"""HashiCorp Vault 工具 - 密钥/证书/动态凭证管理

Vault 是密钥管理事实标准，CNCF 项目。
支持: KV/Transit/PKI/数据库动态凭证/SSH CA/AWS Auth
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _vault_cmd(cmd: str, timeout: int = 15) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class VaultStatus(BaseTool):
    """Vault 集群状态"""
    name = "vault_status"
    description = "获取 Vault 集群状态 (sealed/leader/version)"
    category = ToolCategory.VAULT
    parameters = {"type": "object", "properties": {}}

    def execute(self, **kwargs) -> ToolResult:
        return _vault_cmd("vault status -format=json 2>/dev/null || echo 'Vault CLI not found'")


class VaultKVRead(BaseTool):
    """读取 KV 密钥"""
    name = "vault_kv_read"
    description = "从 Vault KV 引擎读取密钥值"
    category = ToolCategory.VAULT
    parameters = {"type": "object", "properties": {
        "path": {"type": "string", "description": "密钥路径 (如 secret/data/myapp)"},
        "version": {"type": "integer", "description": "版本号"},
    }, "required": ["path"]}

    def execute(self, path: str, version: int = 0, **kwargs) -> ToolResult:
        cmd = f"vault kv get -format=json {path}"
        if version:
            cmd += f" -version={version}"
        return _vault_cmd(cmd)


class VaultKVWrite(BaseTool):
    """写入 KV 密钥"""
    name = "vault_kv_write"
    description = "向 Vault KV 引擎写入密钥"
    category = ToolCategory.VAULT
    is_destructive = True
    requires_confirmation = True
    parameters = {"type": "object", "properties": {
        "path": {"type": "string"},
        "data": {"type": "string", "description": "JSON 格式 key=value"},
    }, "required": ["path", "data"]}

    def execute(self, path: str, data: str, **kwargs) -> ToolResult:
        return _vault_cmd(f"vault kv put {path} {data}")


class VaultLeaseList(BaseTool):
    """列出活跃租约"""
    name = "vault_lease_list"
    description = "列出 Vault 中所有活跃的租约 (动态凭证)"
    category = ToolCategory.VAULT
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/revoke", "default": "list"},
        "lease_id": {"type": "string"},
    }}

    def execute(self, action: str = "list", lease_id: str = "", **kwargs) -> ToolResult:
        if action == "revoke" and lease_id:
            return _vault_cmd(f"vault lease revoke {lease_id}")
        return _vault_cmd("vault list sys/leases/lookup/ 2>/dev/null || vault lease list 2>/dev/null")


class VaultPolicyList(BaseTool):
    """Vault 策略管理"""
    name = "vault_policies"
    description = "列出/查看 Vault 策略"
    category = ToolCategory.VAULT
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/read", "default": "list"},
        "policy": {"type": "string", "description": "策略名称"},
    }}

    def execute(self, action: str = "list", policy: str = "", **kwargs) -> ToolResult:
        if action == "read" and policy:
            return _vault_cmd(f"vault policy read {policy}")
        return _vault_cmd("vault policy list")


class VaultSecretEngines(BaseTool):
    """Vault 密钥引擎"""
    name = "vault_secrets"
    description = "列出已启用的密钥引擎 (KV/Transit/PKI/数据库等)"
    category = ToolCategory.VAULT
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "list/tune", "default": "list"},
        "path": {"type": "string", "description": "引擎路径"},
    }}

    def execute(self, action: str = "list", path: str = "", **kwargs) -> ToolResult:
        if action == "tune" and path:
            return _vault_cmd(f"vault read sys/mounts/{path}/tune")
        return _vault_cmd("vault secrets list -format=json")
