"""运维手册知识库"""
from .base import KnowledgeBase


class RunbookKB(KnowledgeBase):
    """运维手册知识库 - 存储常见问题的处理流程"""

    def __init__(self):
        super().__init__()
        self._load_defaults()

    def _load_defaults(self):
        """加载默认运维手册"""
        self.add({
            "id": "high-cpu",
            "title": "CPU 使用率过高",
            "symptoms": ["cpu high", "CPU高", "负载高", "load average"],
            "diagnosis": [
                "top -bn1 | head -20",
                "ps aux --sort=-%cpu | head -10",
                "pidstat -u 1 5",
                "vmstat 1 5",
            ],
            "root_causes": ["应用死循环", "GC频繁", "挖矿病毒", "配置不当"],
            "fixes": [
                "kill -9 <PID>  # 终止异常进程",
                "systemctl restart <service>  # 重启服务",
                "sync && echo 3 > /proc/sys/vm/drop_caches  # 清理缓存",
            ],
        })
        self.add({
            "id": "disk-full",
            "title": "磁盘空间不足",
            "symptoms": ["disk full", "磁盘满", "No space left", "ENOSPC"],
            "diagnosis": [
                "df -h",
                "du -sh /* | sort -rh | head -10",
                "find / -type f -size +100M | head -20",
            ],
            "root_causes": ["日志增长", "临时文件", "Docker镜像", "核心转储"],
            "fixes": [
                "find /var/log -name '*.gz' -mtime +30 -delete",
                "docker system prune -f",
                "journalctl --vacuum-time=7d",
            ],
        })
        self.add({
            "id": "oom-killed",
            "title": "OOM Killed",
            "symptoms": ["OOMKilled", "oom", "out of memory", "内存不足"],
            "diagnosis": [
                "dmesg | grep -i oom",
                "free -h",
                "ps aux --sort=-%mem | head -10",
                "cat /proc/meminfo | head -10",
            ],
            "root_causes": ["内存泄漏", "配置不当", "流量突增"],
            "fixes": [
                "调整应用内存限制",
                "增加物理内存",
                "优化应用内存使用",
            ],
        })
        self.add({
            "id": "pod-crashloop",
            "title": "Pod CrashLoopBackOff",
            "symptoms": ["CrashLoopBackOff", "pod crash", "pod重启"],
            "diagnosis": [
                "kubectl get pods -o wide",
                "kubectl describe pod <pod>",
                "kubectl logs <pod> --previous",
                "kubectl get events",
            ],
            "root_causes": ["应用启动失败", "配置错误", "依赖服务不可用", "资源不足"],
            "fixes": [
                "kubectl rollout restart deployment/<name>",
                "kubectl rollout undo deployment/<name>",
                "检查并修复配置",
            ],
        })
        self.add({
            "id": "ssh-bruteforce",
            "title": "SSH 暴力破解",
            "symptoms": ["Failed password", "SSH暴力破解", "登录失败"],
            "diagnosis": [
                "lastb | head -20",
                "grep 'Failed password' /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head",
            ],
            "root_causes": ["密码太弱", "端口暴露", "无fail2ban"],
            "fixes": [
                "apt install fail2ban && systemctl enable fail2ban",
                "使用密钥认证替代密码",
                "修改SSH端口",
            ],
        })

    def search(self, query, top_k=5):
        """基于关键词匹配搜索"""
        query_lower = query.lower()
        scored = []
        for entry in self._entries:
            score = 0
            # 匹配标题
            if any(kw in entry["title"].lower() for kw in query_lower.split()):
                score += 3
            # 匹配症状
            for symptom in entry.get("symptoms", []):
                if any(kw in symptom.lower() for kw in query_lower.split()):
                    score += 2
            # 匹配关键词
            for kw in query_lower.split():
                if kw in str(entry).lower():
                    score += 1
            if score > 0:
                scored.append((score, entry))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored[:top_k]]
