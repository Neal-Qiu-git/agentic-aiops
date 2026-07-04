"""Agentic AIOps CLI - 安全版本"""
import sys
import logging
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.logging import RichHandler
from typing import Optional

from .core.config import Config, ServerConfig
from .core.engine import AIOpsEngine, create_engine
from .reporters.terminal import TerminalReporter
from .reporters.markdown import MarkdownReporter
from .reporters.json_report import JsonReporter

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=Console())],
)
logger = logging.getLogger(__name__)

console = Console()


def get_engine(host: Optional[str] = None, user: Optional[str] = None,
               port: int = 22, config_file: Optional[str] = None) -> AIOpsEngine:
    """获取 AIOps 引擎实例"""
    try:
        return create_engine(config_path=config_file, host=host, user=user or "root", port=port)
    except Exception as e:
        console.print(f"[red]引擎初始化失败: {e}[/]")
        sys.exit(1)


def handle_error(e: Exception, operation: str):
    """统一错误处理"""
    console.print(f"[red]{operation}失败: {e}[/]")
    logger.error(f"{operation}失败: {e}", exc_info=True)
    sys.exit(1)


@click.group()
@click.option("--config", "-c", "config_file", default=None, help="配置文件路径")
@click.option("--verbose", "-v", is_flag=True, help="启用详细日志")
@click.pass_context
def main(ctx, config_file: Optional[str], verbose: bool):
    """Agentic AIOps - 智能运维平台"""
    ctx.ensure_object(dict)
    ctx.obj["config_file"] = config_file

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.option("--format", "-f", "fmt", type=click.Choice(["terminal", "markdown", "json"]), default="terminal")
@click.option("--output", "-o", default=None, help="输出文件路径")
@click.pass_context
def check(ctx, host: Optional[str], user: str, port: int, fmt: str, output: Optional[str]):
    """健康巡检"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("health-check")
        if fmt == "terminal":
            TerminalReporter().print_health_check(result)
        elif fmt == "markdown":
            print(MarkdownReporter().generate_health_check(result, output))
        elif fmt == "json":
            print(JsonReporter().generate(result, output))
    except Exception as e:
        handle_error(e, "健康巡检")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.option("--symptom", "-s", default="", help="事件症状")
@click.pass_context
def triage(ctx, host: Optional[str], user: str, port: int, symptom: str):
    """事件分诊"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("incident-triage", symptom=symptom)
        TerminalReporter().print_triage(result)
    except Exception as e:
        handle_error(e, "事件分诊")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.option("--hours", default=24, help="分析时间范围（小时）")
@click.option("--format", "-f", "fmt", type=click.Choice(["terminal", "markdown", "json"]), default="terminal")
@click.option("--output", "-o", default=None, help="输出文件路径")
@click.pass_context
def logs(ctx, host: Optional[str], user: str, port: int, hours: int, fmt: str, output: Optional[str]):
    """日志诊断"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("log-diagnosis", hours=hours)
        stats = result.get("stats", {})
        console.print(f"总错误: {stats.get('total_errors', 0)} | 受影响文件: {stats.get('files_with_errors', 0)}")

        if fmt == "markdown":
            print(MarkdownReporter().generate_log_diagnosis(result, output))
        elif fmt == "json":
            print(JsonReporter().generate(result, output))
    except Exception as e:
        handle_error(e, "日志诊断")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.pass_context
def discover(ctx, host: Optional[str], user: str, port: int):
    """环境发现"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("env-discovery")
        inv = result.get("inventory", {})
        console.print(Panel(
            f"主机: {inv.get('hostname', '')} | OS: {inv.get('os', '')} | CPU: {inv.get('cpu_cores', 0)}核 | 内存: {inv.get('memory_gb', 0)}G",
            title="环境发现"
        ))
    except Exception as e:
        handle_error(e, "环境发现")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.option("--format", "-f", "fmt", type=click.Choice(["terminal", "markdown", "json"]), default="terminal")
@click.option("--output", "-o", default=None, help="输出文件路径")
@click.pass_context
def security(ctx, host: Optional[str], user: str, port: int, fmt: str, output: Optional[str]):
    """安全扫描"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("security-scan")
        if fmt == "terminal":
            TerminalReporter().print_security(result)
        elif fmt == "markdown":
            print(MarkdownReporter().generate_security(result, output))
        elif fmt == "json":
            print(JsonReporter().generate(result, output))
    except Exception as e:
        handle_error(e, "安全扫描")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.option("--interval", "-i", default=5, help="采样间隔（秒）")
@click.option("--count", "-n", default=1, help="采样次数")
@click.pass_context
def monitor(ctx, host: Optional[str], user: str, port: int, interval: int, count: int):
    """性能监控"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("perf-monitor", interval=interval, count=count)
        for s in result.get("snapshots", []):
            console.print(f"CPU: {s['cpu']}% | MEM: {s['mem']}%")
    except Exception as e:
        handle_error(e, "性能监控")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.pass_context
def cost(ctx, host: Optional[str], user: str, port: int):
    """成本优化"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("cost-optimize")
        u = result.get("utilization", {})
        console.print(f"CPU: {u.get('cpu', 0)}% | 内存: {u.get('memory', 0)}%")
        for s in result.get("suggestions", []):
            console.print(f"  [{s['priority']}] {s['message']}")
    except Exception as e:
        handle_error(e, "成本优化")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.pass_context
def compliance(ctx, host: Optional[str], user: str, port: int):
    """合规检查"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("compliance")
        console.print(f"合规评分: {result.get('score', 0)}/100 ({result.get('passed', 0)}/{result.get('total', 0)} 通过)")
        for r in result.get("results", []):
            status = "✅" if r['passed'] else "❌"
            console.print(f"  {status} [{r['id']}] {r['title']}")
    except Exception as e:
        handle_error(e, "合规检查")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.option("--issue", "-i", required=True, type=click.Choice(["high-cpu", "disk-full", "service-down"]))
@click.option("--confirm", is_flag=True, help="确认执行修复")
@click.pass_context
def remediate(ctx, host: Optional[str], user: str, port: int, issue: str, confirm: bool):
    """自动修复"""
    if not confirm:
        console.print("[yellow]警告: 自动修复可能会修改系统状态[/]")
        if not click.confirm("是否继续?"):
            return

    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("auto-remediation", issue=issue, confirm=confirm)
        for d in result.get("diagnosis", []):
            console.print(f"  {d['step']}: {d['output'][:200]}")
    except Exception as e:
        handle_error(e, "自动修复")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.pass_context
def capacity(ctx, host: Optional[str], user: str, port: int):
    """容量规划"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("capacity-plan")
        for r in result.get("recommendations", []):
            console.print(f"  [{r['urgency']}] {r['message']}")
    except Exception as e:
        handle_error(e, "容量规划")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", help="服务器地址")
@click.option("--user", "-u", default="root", help="用户名")
@click.option("--port", "-p", default=22, help="SSH 端口")
@click.pass_context
def tools(ctx, host: Optional[str], user: str, port: int):
    """列出所有可用工具"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        tools_list = engine.tool_registry.list_tools()

        table = Table(title="可用工具")
        table.add_column("名称", style="cyan")
        table.add_column("描述", style="green")
        table.add_column("类别", style="yellow")
        table.add_column("需要 SSH", style="red")

        for tool in tools_list:
            table.add_row(
                tool["name"],
                tool["description"],
                tool["category"],
                "是" if tool["requires_ssh"] else "否",
            )

        console.print(table)
    except Exception as e:
        handle_error(e, "列出工具")
    finally:
        engine.close()


@main.command()
@click.option("--host", "-h", default="0.0.0.0", help="监听地址")
@click.option("--port", "-p", default=8000, help="监听端口")
@click.option("--no-browser", is_flag=True, help="不自动打开浏览器")
def serve(host, port, no_browser):
    """启动 Web Dashboard（API + 前端一体化）"""
    import os
    import webbrowser
    from threading import Timer
    from .api.server import run_server, WEB_DIR

    # 检查 Dashboard 文件是否存在
    if not os.path.isfile(os.path.join(WEB_DIR, "index.html")):
        console.print("[yellow]⚠ Dashboard 未构建，正在自动构建...[/]")
        dashboard_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard")
        if os.path.isdir(dashboard_dir):
            os.system(f"cd {dashboard_dir} && npm run build 2>&1")
            # 复制到 web 目录
            dist_dir = os.path.join(dashboard_dir, "dist")
            if os.path.isdir(dist_dir):
                os.system(f"cp -r {dist_dir}/* {WEB_DIR}/")
                console.print("[green]✓ Dashboard 构建完成[/]")
            else:
                console.print("[red]✗ Dashboard 构建失败[/]")
                return
        else:
            console.print("[red]✗ dashboard 目录不存在[/]")
            return

    # 启动服务器
    url = f"http://{'localhost' if host == '0.0.0.0' else host}:{port}"
    console.print(Panel(
        f"[bold green]🚀 Agentic AIOps Dashboard 已启动[/]\n\n"
        f"  🌐 访问地址: [link={url}]{url}[/link]\n"
        f"  📡 API 地址: [link={url}/api/v1/health]{url}/api/v1/health[/link]\n"
        f"  📊 监控页面: [link={url}/#/monitoring]{url}/#/monitoring[/link]\n"
        f"  🚀 部署页面: [link={url}/#/deployment]{url}/#/deployment[/link]\n\n"
        f"  按 Ctrl+C 停止服务",
        title="🤖 Agentic AIOps",
        border_style="blue"
    ))

    # 自动打开浏览器
    if not no_browser:
        Timer(1.5, lambda: webbrowser.open(url)).start()

    run_server(host=host, port=port)


@main.command()
@click.pass_context
def version(ctx):
    """显示版本信息"""
    from . import __version__
    console.print(f"Agentic AIOps v{__version__}")


if __name__ == "__main__":
    main()
