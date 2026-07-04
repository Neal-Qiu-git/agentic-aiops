# Memory Leak Diagnosis

Detect and diagnose memory leaks.

## Scenario

Server memory usage continuously increasing.

## Commands

```bash
# Basic diagnosis
aiops agent linux --symptom "内存泄漏"

# Specific process
aiops agent linux --host 10.0.0.1 --symptom "Java 内存泄漏"

# Using workflow
aiops workflow run memory-diagnosis --host 10.0.0.1
```

## Expected Output

```
[08:32:01] 🔍 OBSERVE    Memory usage 95%
[08:32:02] 🧠 REASON     Checking memory trends
[08:32:03] 📋 PLAN       free → ps → jmap
[08:32:04] ⚡ ACTION     free -m
[08:32:05] ⚡ ACTION     ps aux --sort=-%mem | head -10
[08:32:06] ⚡ ACTION     jmap -heap <pid>
[08:32:07] ✅ VERIFY     Old gen growing continuously
[08:32:08] 📝 LEARN      Recorded to knowledge base

Root Cause: Memory leak in application
Fix: Analyze heap dump, fix memory leak
```

## Files

- `workflow.yaml` — Workflow definition
- `runbook.md` — Troubleshooting runbook
