"""自动修复模块"""

class AutoRemediationModule:
    name = "auto-remediation"
    RUNBOOKS = {
        "high-cpu":[{"cmd":"top -bn1 | head -20","desc":"查看CPU大户"}],
        "disk-full":[{"cmd":"du -sh /* 2>/dev/null | sort -rh | head","desc":"查大目录"}],
        "service-down":[{"cmd":"systemctl list-units --state=failed","desc":"查看失败服务"}],
    }
    def run(self, ctx):
        ssh, server, issue = ctx["ssh"], ctx["server"], ctx.get("issue","")
        if issue not in self.RUNBOOKS: return {"error":f"未知: {issue}","available":list(self.RUNBOOKS.keys())}
        results = []
        for step in self.RUNBOOKS[issue]:
            out, _, code = ssh.exec_command(server, step["cmd"], timeout=15)
            results.append({"step":step["desc"],"command":step["cmd"],"output":out.strip()[:500],"exit_code":code})
        return {"issue":issue,"diagnosis":results}
