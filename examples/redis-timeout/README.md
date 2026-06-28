# Redis Connection Timeout Diagnosis

Diagnose Redis connection issues.

## Scenario

Application reporting `ConnectionPoolTimeout` errors.

## Commands

```bash
# Basic diagnosis
aiops agent db --type redis --symptom "连接超时"

# Specific server
aiops agent db --type redis --host 10.0.0.1 --symptom "ConnectionPoolTimeout"

# Using workflow
aiops workflow run redis-diagnosis --host 10.0.0.1
```

## Expected Output

```
[08:32:01] 🔍 OBSERVE    Redis connection errors
[08:32:02] 🧠 REASON     Checking connection pool
[08:32:03] 📋 PLAN       check_status → check_clients → check_config
[08:32:04] ⚡ ACTION     redis-cli info clients
[08:32:05] ⚡ ACTION     redis-cli config get maxclients
[08:32:06] ✅ VERIFY     Pool exhausted: 1000/1000 connections
[08:32:07] 📝 LEARN      Recorded to knowledge base

Root Cause: Connection pool too small
Fix: Increase pool_size from 100 to 500
```

## Files

- `workflow.yaml` — Workflow definition
- `runbook.md` — Troubleshooting runbook
