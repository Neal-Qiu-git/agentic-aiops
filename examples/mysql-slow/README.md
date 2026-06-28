# MySQL Slow Query Diagnosis

Diagnose MySQL slow queries.

## Scenario

API response time increased from 100ms to 2s.

## Commands

```bash
# Basic diagnosis
aiops agent db --type mysql --symptom "查询慢"

# Specific database
aiops agent db --type mysql --host 10.0.0.1 --database myapp --symptom "慢查询"

# Using workflow
aiops workflow run mysql-diagnosis --host 10.0.0.1
```

## Expected Output

```
[08:32:01] 🔍 OBSERVE    High query latency
[08:32:02] 🧠 REASON     Checking slow queries
[08:32:03] 📋 PLAN       processlist → slowlog → explain
[08:32:04] ⚡ ACTION     SHOW PROCESSLIST
[08:32:05] ⚡ ACTION     EXPLAIN SELECT ...
[08:32:06] ✅ VERIFY     Full table scan on orders table
[08:32:07] 📝 LEARN      Recorded to knowledge base

Root Cause: Missing index on user_id
Fix: CREATE INDEX idx_user_id ON orders(user_id)
```

## Files

- `workflow.yaml` — Workflow definition
- `runbook.md` — Troubleshooting runbook
