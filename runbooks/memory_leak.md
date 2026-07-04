# 内存泄漏

## 诊断
```bash
free -h
ps aux --sort=-%mem | head -10
```

## Java
```bash
jmap -dump:live,format=b,file=/tmp/heap.hprof <PID>
```

## 修复
```bash
systemctl restart <service>
```
