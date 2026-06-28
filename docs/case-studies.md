# Case Studies

Real-world operational scenarios handled by Agentic AIOps.

---

## Case 1: Pod CrashLoopBackOff

### Scenario

Production Kubernetes cluster, pod `payment-api` in `CrashLoopBackOff` state.

### Timeline

| Time | Action |
|------|--------|
| 08:00 | Prometheus alert: Pod restart count > 5 |
| 08:01 | Event Bus receives alert |
| 08:01 | Planner Agent creates plan |
| 08:02 | K8s Agent: `kubectl get pods` → CrashLoopBackOff |
| 08:02 | K8s Agent: `kubectl describe pod` → OOMKilled |
| 08:03 | K8s Agent: `kubectl get events` → Memory limit exceeded |
| 08:03 | Monitor Agent: Check node memory → Normal |
| 08:04 | Root cause: Pod memory limit too low (128Mi) |
| 08:04 | Fix suggestion: Increase to 512Mi |
| 08:05 | Approval requested |
| 08:06 | Approved by SRE |
| 08:06 | K8s Agent: `kubectl patch deployment` |
| 08:07 | Verification: Pod running, no restarts |
| 08:07 | Memory updated: OOM fix pattern recorded |

### Result

- **Root Cause**: Memory limit 128Mi too low
- **Fix**: Increase to 512Mi
- **Resolution Time**: 7 minutes
- **Manual Time**: ~15 minutes

---

## Case 2: Redis Connection Pool Exhausted

### Scenario

Application reporting `ConnectionPoolTimeout` errors.

### Timeline

| Time | Action |
|------|--------|
| 14:00 | Alert: Redis connection errors spike |
| 14:01 | Planner Agent creates plan |
| 14:01 | Log Agent: Analyze logs → ConnectionPoolTimeout |
| 14:02 | DB Agent: `redis-cli info clients` → 1000 connections |
| 14:02 | DB Agent: `redis-cli config get maxclients` → 10000 |
| 14:03 | Linux Agent: Check app config → pool_size=100 |
| 14:03 | Root cause: Pool exhausted under load |
| 14:04 | Fix: Increase pool_size to 500 |
| 14:05 | Application config updated |
| 14:06 | Verification: Connection errors resolved |

### Result

- **Root Cause**: Connection pool too small
- **Fix**: Increase pool_size from 100 to 500
- **Resolution Time**: 6 minutes

---

## Case 3: MySQL Slow Query

### Scenario

API response time increased from 100ms to 2s.

### Timeline

| Time | Action |
|------|--------|
| 10:00 | Alert: API p99 latency > 1s |
| 10:01 | Monitor Agent: Check Prometheus → Database latency |
| 10:02 | DB Agent: `SHOW PROCESSLIST` → Long running queries |
| 10:02 | DB Agent: `EXPLAIN SELECT ...` → Full table scan |
| 10:03 | DB Agent: Check indexes → Missing index on `user_id` |
| 10:04 | Root cause: Missing index causing full scan |
| 10:04 | Fix: `CREATE INDEX idx_user_id ON orders(user_id)` |
| 10:05 | Approval requested |
| 10:06 | Approved |
| 10:06 | Index created |
| 10:07 | Verification: Query time < 10ms |

### Result

- **Root Cause**: Missing index
- **Fix**: Create index on user_id
- **Resolution Time**: 7 minutes
- **Performance**: 200x improvement

---

## Case 4: Disk Space Full

### Scenario

Server `/var/log` partition 100% full.

### Timeline

| Time | Action |
|------|--------|
| 16:00 | Alert: Disk usage > 95% |
| 16:01 | Linux Agent: `df -h` → /var/log 100% |
| 16:01 | Linux Agent: `du -sh /var/log/*` → app.log 50GB |
| 16:02 | Linux Agent: `ls -lh /var/log/app.log` → 50GB |
| 16:02 | Root cause: Log rotation not working |
| 16:03 | Fix: Enable logrotate, archive old logs |
| 16:04 | Approval: Delete logs > 7 days |
| 16:05 | Approved |
| 16:05 | Logs archived, rotation fixed |
| 16:06 | Verification: Disk usage 45% |

### Result

- **Root Cause**: Log rotation disabled
- **Fix**: Enable logrotate, archive old logs
- **Resolution Time**: 6 minutes
- **Space Recovered**: 45GB

---

## Summary

| Case | Root Cause | Fix Time | Manual Time | Savings |
|------|------------|----------|-------------|---------|
| Pod CrashLoop | Memory limit | 7 min | 15 min | 53% |
| Redis Pool | Pool size | 6 min | 10 min | 40% |
| MySQL Slow | Missing index | 7 min | 20 min | 65% |
| Disk Full | Log rotation | 6 min | 12 min | 50% |
| **Average** | | **6.5 min** | **14.25 min** | **52%** |
