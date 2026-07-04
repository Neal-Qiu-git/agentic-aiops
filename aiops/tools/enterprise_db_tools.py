"""企业数据库工具 - Oracle / ClickHouse / TiDB / DM8 / OceanBase / KingbaseES

Oracle: 企业级数据库霸主
ClickHouse: 分析型数据库首选 (OLAP)
TiDB: 国产分布式 NewSQL
DM8 (达梦): 国产信创数据库第一
OceanBase: 蚂蚁分布式数据库
KingbaseES (人大金仓): 国产信创数据库
"""
import json
import logging
import subprocess
from .base import BaseTool, ToolResult, ToolCategory

logger = logging.getLogger(__name__)


def _db_cmd(cmd: str, timeout: int = 15) -> ToolResult:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ToolResult(success=(r.returncode == 0), output=r.stdout.strip()[:8000],
                          error=r.stderr.strip() if r.returncode != 0 else "")
    except Exception as e:
        return ToolResult(success=False, error=str(e))


class OracleTool(BaseTool):
    """Oracle 数据库管理"""
    name = "oracle_db"
    description = "Oracle 数据库查询和管理 (通过 sqlplus 或 oracledb)"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "query/status/sessions/tablespace/locks", "default": "status"},
        "sql": {"type": "string", "description": "SQL 语句"},
        "host": {"type": "string", "description": "连接地址"},
        "user": {"type": "string", "default": "system"},
        "password": {"type": "string"},
        "service": {"type": "string", "description": "Oracle Service Name"},
    }}

    def execute(self, action: str = "status", sql: str = "", host: str = "localhost",
                user: str = "system", password: str = "", service: str = "ORCL", **kwargs) -> ToolResult:
        if action == "status":
            sql = "SELECT instance_name, version, status FROM v$instance"
        elif action == "sessions":
            sql = "SELECT sid, serial#, username, status, machine FROM v$session WHERE ROWNUM <= 20"
        elif action == "tablespace":
            sql = "SELECT tablespace_name, round(sum(bytes)/1024/1024,2) AS mb FROM dba_data_files GROUP BY tablespace_name ORDER BY mb DESC"
        elif action == "locks":
            sql = "SELECT s.sid, s.serial#, s.username, o.object_name FROM v$locked_object l JOIN dba_objects o ON l.object_id=o.object_id JOIN v$session s ON l.session_id=s.sid"
        elif action == "query" and not sql:
            return ToolResult(success=False, error="query action 需要 sql 参数")
        # 使用 python-oracledb 或 sqlplus
        cmd = f"echo '{sql}' | sqlplus -S {user}/{password}@{host}/{service} 2>/dev/null"
        if not password:
            cmd = f"echo '{sql}' | sqlplus -S / as sysdba 2>/dev/null"
        return _db_cmd(cmd)


class ClickHouseTool(BaseTool):
    """ClickHouse 分析型数据库"""
    name = "clickhouse_db"
    description = "ClickHouse 查询和管理 (OLAP 分析)"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "query/status/tables/engines/processes", "default": "status"},
        "sql": {"type": "string"},
        "host": {"type": "string", "default": "localhost"},
        "port": {"type": "integer", "default": 8123},
    }}

    def execute(self, action: str = "status", sql: str = "", host: str = "localhost",
                port: int = 8123, **kwargs) -> ToolResult:
        url = f"http://{host}:{port}"
        if action == "status":
            sql = "SELECT version(), uptime(), event_time FROM system.metrics LIMIT 1"
        elif action == "tables":
            sql = "SELECT database, name, engine, formatReadableSize(total_bytes) AS size FROM system.tables ORDER BY total_bytes DESC LIMIT 20"
        elif action == "processes":
            sql = "SELECT query, elapsed, read_rows, memory_usage FROM system.processes"
        elif action == "engines":
            sql = "SELECT name FROM system.engines"
        elif action == "query" and not sql:
            return ToolResult(success=False, error="query action 需要 sql")
        return _db_cmd(f"curl -s '{url}/' --data '{sql}'")


class TiDBTool(BaseTool):
    """TiDB 分布式数据库"""
    name = "tidb_db"
    description = "TiDB 分布式 NewSQL 数据库管理"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "query/status/cluster/slow_query", "default": "status"},
        "sql": {"type": "string"},
        "host": {"type": "string", "default": "localhost"},
        "port": {"type": "integer", "default": 4000},
    }}

    def execute(self, action: str = "status", sql: str = "", host: str = "localhost",
                port: int = 4000, **kwargs) -> ToolResult:
        if action == "status":
            sql = "SELECT VERSION()"
        elif action == "cluster":
            sql = "SELECT * FROM information_schema.tikv_region_status LIMIT 10"
        elif action == "slow_query":
            sql = "SELECT query, query_time, process_time FROM information_schema.slow_query ORDER BY query_time DESC LIMIT 10"
        elif action == "query" and not sql:
            return ToolResult(success=False, error="query action 需要 sql")
        return _db_cmd(f"mysql -h {host} -P {port} -u root -e '{sql}' 2>/dev/null")


class DM8Tool(BaseTool):
    """达梦 DM8 数据库"""
    name = "dm8_db"
    description = "达梦 DM8 国产信创数据库管理"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "query/status/ tablespaces/sessions", "default": "status"},
        "sql": {"type": "string"},
        "host": {"type": "string", "default": "localhost"},
        "port": {"type": "integer", "default": 5236},
        "user": {"type": "string", "default": "SYSDBA"},
        "password": {"type": "string", "default": "SYSDBA001"},
    }}

    def execute(self, action: str = "status", sql: str = "", host: str = "localhost",
                port: int = 5236, user: str = "SYSDBA", password: str = "SYSDBA001", **kwargs) -> ToolResult:
        if action == "status":
            sql = "SELECT * FROM V$VERSION"
        elif action == "tablespaces":
            sql = "SELECT TABLESPACE_NAME, STATUS, TOTAL_SIZE, FREE_SIZE FROM DBA_TABLESPACES"
        elif action == "sessions":
            sql = "SELECT * FROM V$SESSIONS WHERE ROWNUM <= 20"
        elif action == "query" and not sql:
            return ToolResult(success=False, error="query action 需要 sql")
        return _db_cmd(f"disql {user}/{password}@{host}::236 -- '{sql}' 2>/dev/null || echo 'DM8 disql not found'")


class OceanBaseTool(BaseTool):
    """OceanBase 分布式数据库"""
    name = "oceanbase_db"
    description = "OceanBase 蚂蚁分布式数据库管理"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "query/status/cluster/tenants", "default": "status"},
        "sql": {"type": "string"},
        "host": {"type": "string", "default": "localhost"},
        "port": {"type": "integer", "default": 2881},
    }}

    def execute(self, action: str = "status", sql: str = "", host: str = "localhost",
                port: int = 2881, **kwargs) -> ToolResult:
        if action == "status":
            sql = "SELECT * FROM oceanbase.GV$OB_VERSION"
        elif action == "cluster":
            sql = "SELECT * FROM oceanbase.DBA_OB_UNITS"
        elif action == "tenants":
            sql = "SELECT tenant_id, tenant_name, status FROM oceanbase.DBA_OB_TENANTS"
        elif action == "query" and not sql:
            return ToolResult(success=False, error="query action 需要 sql")
        return _db_cmd(f"mysql -h {host} -P {port} -u root -e '{sql}' 2>/dev/null")


class KingbaseESTool(BaseTool):
    """人大金仓 KingbaseES"""
    name = "kingbase_db"
    description = "KingbaseES 国产信创数据库管理"
    category = ToolCategory.DATABASE
    parameters = {"type": "object", "properties": {
        "action": {"type": "string", "description": "query/status/tables", "default": "status"},
        "sql": {"type": "string"},
        "host": {"type": "string", "default": "localhost"},
        "port": {"type": "integer", "default": 54321},
        "user": {"type": "string", "default": "system"},
    }}

    def execute(self, action: str = "status", sql: str = "", host: str = "localhost",
                port: int = 54321, user: str = "system", **kwargs) -> ToolResult:
        if action == "status":
            sql = "SELECT version()"
        elif action == "tables":
            sql = "SELECT schemaname, tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema') LIMIT 20"
        elif action == "query" and not sql:
            return ToolResult(success=False, error="query action 需要 sql")
        return _db_cmd(f"ksql -h {host} -p {port} -U {user} -c '{sql}' 2>/dev/null || echo 'KingbaseES ksql not found'")
