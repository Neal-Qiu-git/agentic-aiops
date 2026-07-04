# Pod CrashLoopBackOff Diagnosis

Diagnose Kubernetes Pod CrashLoopBackOff issues.

## Scenario

Pod `payment-api` in `CrashLoopBackOff` state.

## Commands

```bash
# Basic diagnosis
aiops agent k8s --symptom "Pod CrashLoopBackOff"

# Specific pod
aiops agent k8s --action diagnose --pod payment-api --namespace production

# Using workflow
aiops workflow run pod-troubleshoot --pod payment-api
```

## Expected Output

```
[08:32:01] 🔍 OBSERVE    Pod CrashLoopBackOff
[08:32:02] 🧠 REASON     Checking pod status and events
[08:32:03] 📋 PLAN       get_pods → get_events → describe → logs
[08:32:04] ⚡ ACTION     kubectl get pods -n production
[08:32:05] ⚡ ACTION     kubectl describe pod payment-api
[08:32:06] ⚡ ACTION     kubectl logs payment-api --tail=100
[08:32:07] ✅ VERIFY     OOMKilled: memory limit exceeded
[08:32:08] 📝 LEARN      Recorded to knowledge base

Root Cause: Memory limit too low (128Mi)
Fix: kubectl patch deployment payment-api -p '{"spec":{"template":{"spec":{"containers":[{"name":"api","resources":{"limits":{"memory":"512Mi"}}}]}}}}'
```

## Files

- `workflow.yaml` — Workflow definition
- `runbook.md` — Troubleshooting runbook
