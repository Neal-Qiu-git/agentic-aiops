"""安全扫描模块"""

class SecurityScanModule:
    name = "security-scan"
    def run(self, ctx):
        ssh, server = ctx["ssh"], ctx["server"]
        findings = []
        out, _, _ = ssh.exec_command(server, "cat /etc/ssh/sshd_config")
        cfg = out.lower()
        if "permitrootlogin yes" in cfg: findings.append({"check":"ssh","level":"critical","message":"SSH root登录","fix":"修改PermitRootLogin"})
        if "passwordauthentication yes" in cfg: findings.append({"check":"ssh","level":"warning","message":"SSH密码认证","fix":"用密钥"})
        out, _, _ = ssh.exec_command(server, "systemctl is-active fail2ban 2>/dev/null || echo inactive")
        if "inactive" in out.lower(): findings.append({"check":"fail2ban","level":"warning","message":"fail2ban未运行","fix":"apt install fail2ban"})
        out, _, _ = ssh.exec_command(server, "iptables -L -n 2>/dev/null | grep -c ACCEPT || echo 0")
        rules = int(out.strip()) if out.strip().isdigit() else 0
        if rules < 3: findings.append({"check":"firewall","level":"warning","message":"防火墙规则少","fix":"配置iptables"})
        crit = sum(1 for f in findings if f["level"]=="critical")
        warn = sum(1 for f in findings if f["level"]=="warning")
        return {"findings":findings,"critical":crit,"warning":warn,"score":max(0,100-crit*15-warn*5)}
