# 服务宕机

## 诊断
```bash
systemctl status <service>
journalctl -u <service> -n 50
ss -tlnp | grep <port>
```

## 重启
```bash
systemctl restart <service>
```
