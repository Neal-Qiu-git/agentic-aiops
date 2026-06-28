# Disk Full Diagnosis

Diagnose disk space issues.

## Scenario

Server `/var/log` partition 100% full.

## Commands

```bash
# Basic diagnosis
aiops agent linux --symptom "磁盘满"

# Specific path
aiops agent linux --host 10.0.0.1 --symptom "/var/log 磁盘满"

# Using workflow
aiops workflow run disk-diagnosis --host 10.0.0.1
```

## Expected Output

```
[08:32:01] 🔍 OBSERVE    Disk usage 100%
[08:32:02] 🧠 REASON     Finding large files
[08:32:03] 📋 PLAN       df → du → find
[08:32:04] ⚡ ACTION     df -h /var/log
[08:32:05] ⚡ ACTION     du -sh /var/log/*
[08:32:06] ✅ VERIFY     app.log is 50GB
[08:32:07] 📝 LEARN      Recorded to knowledge base

Root Cause: Log rotation disabled
Fix: Enable logrotate, archive old logs
```

## Files

- `workflow.yaml` — Workflow definition
- `runbook.md` — Troubleshooting runbook
