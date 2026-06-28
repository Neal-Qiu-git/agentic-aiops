# CPU High Diagnosis

Diagnose high CPU usage on a Linux server.

## Scenario

Server `10.0.0.1` has CPU usage > 90% for 5 minutes.

## Commands

```bash
# Basic diagnosis
aiops diagnose --host 10.0.0.1 --symptom "CPU 高"

# With specific threshold
aiops agent linux --host 10.0.0.1 --symptom "CPU > 90%"

# Using workflow
aiops workflow run cpu-diagnosis --host 10.0.0.1
```

## Expected Output

```
[08:32:01] 🔍 OBSERVE    CPU 95%, Load 8.2
[08:32:02] 🧠 REASON     High CPU detected
[08:32:03] 📋 PLAN       check_top → check_process → check_gc
[08:32:04] ⚡ ACTION     Executing commands...
[08:32:07] ✅ VERIFY     Java GC consuming 80% CPU
[08:32:08] 📝 LEARN      Recorded to knowledge base

Root Cause: Java Full GC
Fix: Increase JVM heap -Xmx4g → 8g
```

## Files

- `workflow.yaml` — Workflow definition
- `runbook.md` — Troubleshooting runbook
- `config.yaml` — Configuration example
