"""合规检查模块"""

class ComplianceModule:
    name = "compliance"
    CHECKS = [
        {"id":"CIS-3.1","title":"SYN Cookie","cmd":"sysctl net.ipv4.tcp_syncookies 2>/dev/null | awk -F= '{print $2}'","expect":"1"},
        {"id":"CIS-3.2","title":"IP Forward","cmd":"sysctl net.ipv4.ip_forward 2>/dev/null | awk -F= '{print $2}'","expect":"0"},
    ]
    def run(self, ctx):
        ssh, server = ctx["ssh"], ctx["server"]
        results = []
        for c in self.CHECKS:
            out, _, _ = ssh.exec_command(server, c["cmd"], timeout=10)
            r = out.strip(); results.append({"id":c["id"],"title":c["title"],"result":r,"passed":r==c["expect"]})
        pc = sum(1 for r in results if r["passed"])
        return {"results":results,"passed":pc,"total":len(results),"score":round(pc/len(results)*100) if results else 0}
