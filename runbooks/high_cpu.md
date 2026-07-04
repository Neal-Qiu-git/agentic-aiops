# CPU 使用率过高

## 诊断
```bash
top -bn1 | head -20
ps aux --sort=-%cpu | head -10
```

## 常见原因
- Java GC 频繁
- 死循环
- 挖矿病毒

## 修复
```bash
# 清理缓存
sync && echo 3 > /proc/sys/vm/drop_caches
# 重启服务
systemctl restart <service>
```
