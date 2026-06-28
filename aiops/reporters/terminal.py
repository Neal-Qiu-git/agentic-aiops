"""终端彩色输出"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class TerminalReporter:
    def __init__(self): self.console = Console()
    def print_health_check(self, data):
        overall = data.get("overall","UNKNOWN")
        color = {"HEALTHY":"green","DEGRADED":"yellow","CRITICAL":"red"}.get(overall,"white")
        self.console.print(Panel(f"健康巡检 - {data.get('hostname','')} [{color}]{overall}[/]", border_style=color))
        sys_d = data.get("data",{}).get("system",{})
        table = Table(title="系统资源"); table.add_column("指标",style="cyan"); table.add_column("值"); table.add_column("状态")
        cpu = sys_d.get("cpu",{}).get("usage_percent",0); mem = sys_d.get("memory",{}).get("used_percent",0)
        table.add_row("CPU",f"{cpu}%","🔴" if cpu>90 else "🟡" if cpu>70 else "🟢")
        table.add_row("内存",f"{mem}%","🔴" if mem>90 else "🟡" if mem>70 else "🟢")
        self.console.print(table)
        anomalies = data.get("anomalies",{}).get("anomalies",[])
        if anomalies:
            at = Table(title="异常"); at.add_column("级别"); at.add_column("描述")
            for a in anomalies: at.add_row(a["level"].upper(),a["message"])
            self.console.print(at)
    def print_triage(self, data):
        sev = data.get("severity","SEV4")
        c = {"SEV1":"red","SEV2":"red","SEV3":"yellow","SEV4":"green"}.get(sev,"white")
        self.console.print(Panel(f"事件分诊 [{c}]{sev}[/] {data.get('symptom','')}", border_style=c))
    def print_security(self, data):
        score = data.get("score",0); c = "green" if score>=80 else "yellow" if score>=60 else "red"
        self.console.print(Panel(f"安全评分 [{c}]{score}/100[/]", border_style=c))
        for f in data.get("findings",[]): self.console.print(f"  {f['level'].upper()}: {f['message']}")
