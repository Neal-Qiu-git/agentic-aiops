"""Agentic AIOps CLI"""
import sys, click
from rich.console import Console
from rich.panel import Panel
from .core.config import Config, ServerConfig
from .core.engine import AIOpsEngine
from .reporters.terminal import TerminalReporter
from .reporters.markdown import MarkdownReporter
from .reporters.json_report import JsonReporter

console = Console()

def get_engine(host=None, user=None, port=22, config_file=None):
    config = Config.load(config_file)
    server = ServerConfig(name="cli", host=host, port=port, user=user or "root") if host else (config.servers[0] if config.servers else None)
    if not server: console.print("[red]请指定 --host[/]"); sys.exit(1)
    return AIOpsEngine(config=config, server=server)

@click.group()
@click.option("--config", "-c", "config_file", default=None)
@click.pass_context
def main(ctx, config_file):
    """Agentic AIOps - 智能运维平台"""
    ctx.ensure_object(dict); ctx.obj["config_file"] = config_file

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root"); @click.option("--port", "-p", default=22)
@click.option("--format", "-f", "fmt", type=click.Choice(["terminal","markdown","json"]), default="terminal")
@click.option("--output", "-o", default=None); @click.pass_context
def check(ctx, host, user, port, fmt, output):
    """健康巡检"""
    engine = get_engine(host, user, port, ctx.obj["config_file"])
    try:
        result = engine.run_module("health-check")
        if fmt=="terminal": TerminalReporter().print_health_check(result)
        elif fmt=="markdown": print(MarkdownReporter().generate_health_check(result, output))
        elif fmt=="json": print(JsonReporter().generate(result, output))
    finally: engine.close()

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root")
@click.option("--symptom", "-s", default=""); @click.pass_context
def triage(ctx, host, user, symptom):
    """事件分诊"""
    engine = get_engine(host, user, config_file=ctx.obj["config_file"])
    try: TerminalReporter().print_triage(engine.run_module("incident-triage", symptom=symptom))
    finally: engine.close()

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root"); @click.option("--hours", default=24); @click.pass_context
def logs(ctx, host, user, hours):
    """日志诊断"""
    engine = get_engine(host, user, config_file=ctx.obj["config_file"])
    try:
        result = engine.run_module("log-diagnosis", hours=hours)
        stats = result.get("stats", {})
        console.print("总错误: {0} | 受影响文件: {1}".format(stats.get('total_errors',0), stats.get('files_with_errors',0)))
    finally: engine.close()

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root"); @click.pass_context
def discover(ctx, host, user):
    """环境发现"""
    engine = get_engine(host, user, config_file=ctx.obj["config_file"])
    try:
        result = engine.run_module("env-discovery")
        inv = result.get("inventory", {})
        console.print(Panel("主机: {0} | OS: {1} | CPU: {2}核 | 内存: {3}G".format(
            inv.get('hostname',''), inv.get('os',''), inv.get('cpu_cores',0), inv.get('memory_gb',0)), title="环境发现"))
    finally: engine.close()

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root")
@click.option("--format", "-f", "fmt", type=click.Choice(["terminal","markdown","json"]), default="terminal")
@click.option("--output", "-o", default=None); @click.pass_context
def security(ctx, host, user, fmt, output):
    """安全扫描"""
    engine = get_engine(host, user, config_file=ctx.obj["config_file"])
    try:
        result = engine.run_module("security-scan")
        if fmt=="terminal": TerminalReporter().print_security(result)
        elif fmt=="markdown": print(MarkdownReporter().generate_security(result, output))
        elif fmt=="json": print(JsonReporter().generate(result, output))
    finally: engine.close()

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root")
@click.option("--interval", "-i", default=5); @click.option("--count", "-n", default=1); @click.pass_context
def monitor(ctx, host, user, interval, count):
    """性能监控"""
    engine = get_engine(host, user, config_file=ctx.obj["config_file"])
    try:
        result = engine.run_module("perf-monitor", interval=interval, count=count)
        for s in result.get("snapshots", []): console.print("CPU: {0}% | MEM: {1}%".format(s['cpu'], s['mem']))
    finally: engine.close()

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root"); @click.pass_context
def cost(ctx, host, user):
    """成本优化"""
    engine = get_engine(host, user, config_file=ctx.obj["config_file"])
    try:
        result = engine.run_module("cost-optimize")
        u = result.get("utilization", {})
        console.print("CPU: {0}% | 内存: {1}%".format(u.get('cpu',0), u.get('memory',0)))
        for s in result.get("suggestions", []): console.print("  [{0}] {1}".format(s['priority'], s['message']))
    finally: engine.close()

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root"); @click.pass_context
def compliance(ctx, host, user):
    """合规检查"""
    engine = get_engine(host, user, config_file=ctx.obj["config_file"])
    try:
        result = engine.run_module("compliance")
        console.print("合规评分: {0}/100 ({1}/{2} 通过)".format(result.get('score',0), result.get('passed',0), result.get('total',0)))
        for r in result.get("results", []): console.print("  {0} [{1}] {2}".format("✅" if r['passed'] else "❌", r['id'], r['title']))
    finally: engine.close()

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root")
@click.option("--issue", "-i", required=True, type=click.Choice(["high-cpu","disk-full","service-down"])); @click.pass_context
def remediate(ctx, host, user, issue):
    """自动修复"""
    engine = get_engine(host, user, config_file=ctx.obj["config_file"])
    try:
        result = engine.run_module("auto-remediation", issue=issue)
        for d in result.get("diagnosis", []): console.print("  {0}: {1}".format(d['step'], d['output'][:200]))
    finally: engine.close()

@main.command()
@click.option("--host", "-h"); @click.option("--user", "-u", default="root"); @click.pass_context
def capacity(ctx, host, user):
    """容量规划"""
    engine = get_engine(host, user, config_file=ctx.obj["config_file"])
    try:
        result = engine.run_module("capacity-plan")
        for r in result.get("recommendations", []): console.print("  [{0}] {1}".format(r['urgency'], r['message']))
    finally: engine.close()

if __name__ == "__main__": main()
