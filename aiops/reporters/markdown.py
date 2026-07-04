"""Markdown报告"""
import os
from datetime import datetime

class MarkdownReporter:
    def generate_health_check(self, data, output=None):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [f"# 健康巡检报告","","服务器: {0}".format(data.get('hostname','')),"状态: **{0}**".format(data.get('overall','')),"时间: "+now,""]
        sys_d = data.get("data",{}).get("system",{})
        lines += ["## 系统资源","","| 指标 | 值 |","|------|-----|",
            "| CPU | {0}% |".format(sys_d.get("cpu",{}).get("usage_percent",0)),
            "| 内存 | {0}% |".format(sys_d.get("memory",{}).get("used_percent",0)),""]
        content = "\n".join(lines)
        if output:
            with open(output, "w") as f: f.write(content)
        return content
    def generate_security(self, data, output=None):
        lines = ["# 安全扫描","评分: {0}/100".format(data.get('score',0)),"","| 级别 | 描述 |","|------|------|"]
        for f in data.get("findings",[]): lines.append("| {0} | {1} |".format(f['level'].upper(),f['message']))
        content = "\n".join(lines)
        if output:
            with open(output, "w") as f: f.write(content)
        return content
