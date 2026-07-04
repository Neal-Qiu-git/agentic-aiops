# 磁盘空间不足

## 诊断
```bash
df -h
du -sh /* | sort -rh | head -10
```

## 清理
```bash
find /var/log -name '*.gz' -mtime +30 -delete
docker system prune -f
journalctl --vacuum-time=7d
```
