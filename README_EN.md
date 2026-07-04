# Agentic AIOps

<div align="center">

🤖 **AI-native Operations Platform**

*Purpose-built for SRE, DevOps, and Cloud Native automation*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-5.3-orange.svg?style=flat-square)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)]()
[![K8s](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes&logoColor=white)]()
[![MCP](https://img.shields.io/badge/MCP-148%2B_Tools-FF6B35?style=flat-square)]()

English | [中文](README.md)

</div>

---

## Why Agentic AIOps?

Generic AI Agent frameworks are not built for operations.

**Agentic AIOps is purpose-built for:**

- 🐧 Linux/Windows — System diagnostics and troubleshooting
- ☸️ Kubernetes — Container orchestration management
- 🗄️ Database — MySQL, PostgreSQL, Redis, Oracle, DM8, TiDB, ClickHouse, OceanBase
- 📊 Monitoring — Prometheus, Grafana, SkyWalking, Loki analysis
- ☁️ Cloud — AWS, Alibaba Cloud, Huawei Cloud, Tencent Cloud, Azure, GCP
- 🔒 Security — Vulnerability scanning (Trivy, Falco), compliance (OPA, kube-bench)
- 💰 FinOps — Cost optimization (Kubecost, Cloud Cost Explorer)
- 🏗️ IaC — Terraform, Ansible, Helm
- 🔄 CI/CD & GitOps — Jenkins, GitLab CI, GitHub Actions, ArgoCD, FluxCD

---

## ✨ Features

- 🤖 **20+ Specialized Agents** — Linux, Docker, K8s, DB, Middleware, Network, Virtual, Windows, Monitor, Log, APM, SRE, Security, Incident, DevOps, GitOps, IaC, Cloud, Cost, ServiceMesh
- 🔄 **ReAct Reasoning** — Multi-step reasoning with tool calling
- 🔌 **148+ MCP Tools** — Covering 15 categories of ops scenarios
- 🧠 **Operational Memory** — Short-term, long-term, episodic, semantic memory
- 📚 **Knowledge RAG** — Runbook retrieval and knowledge base
- ⚡ **Event Bus** — Async event-driven architecture
- 🚦 **Workflow Engine** — 10 real-world enterprise workflows
- 👤 **Human Approval** — Critical operation gating
- 🌍 **18 Environment Topologies** — From bare-metal to hybrid cloud
- 📊 **Dashboard** — Real-time monitoring, alerts, cost analysis, security posture

---

## 📸 Demo

```bash
$ aiops diagnose --host 10.0.0.1 --symptom "high CPU"

[08:32:01] 🔍 OBSERVE    CPU 95%, Memory 87%
[08:32:02] 🧠 REASON     Analyzing processes
[08:32:03] 📋 PLAN       check_top → check_process → check_gc
[08:32:04] ⚡ ACTION     $ top -bn1 | head -20
[08:32:05] ✅ VERIFY     Java GC consuming 80% CPU
[08:32:06] 📝 LEARN      Recorded to knowledge base

Root Cause: Java Full GC
Fix: Increase JVM heap -Xmx4g → 8g
```

---

## ⚡ Quick Start

```bash
# Install
pip install agentic-aiops

# Configure
export AIOPS_AI_API_KEY=your-key

# Run
aiops diagnose --host 10.0.0.1 --symptom "high CPU"
```

### Docker

```bash
docker run -it agentic-aiops aiops diagnose --help
```

### Kubernetes

```bash
helm install aiops ./charts/agentic-aiops
```

---

## 📊 Support Matrix

### Platform & Runtime

| Platform | Container | Database | Middleware | Monitoring & Observability |
|----------|-----------|----------|------------|---------------------------|
| Linux (all distros) ✅ | Docker ✅ | MySQL ✅ | Nginx ✅ | Prometheus ✅ |
| Windows Server ✅ | Kubernetes ✅ | PostgreSQL ✅ | Apache Kafka ✅ | Grafana ✅ |
| Kylin ✅ | containerd ✅ | Redis ✅ | RabbitMQ ✅ | SkyWalking ✅ |
| UOS ✅ | Podman ✅ | Oracle ✅ | Tomcat ✅ | Jaeger ✅ |
| openEuler ✅ | K3s ✅ | DM8 ✅ | TongWeb ✅ | Loki ✅ |
| Ubuntu/CentOS/RHEL ✅ | Docker Compose ✅ | MongoDB ✅ | WildFly/JBoss ✅ | Alertmanager ✅ |
| Debian/SUSE ✅ | Docker Swarm ✅ | Elasticsearch ✅ | Caddy ✅ | OpenTelemetry ✅ |
| Alpine ✅ | Nomad ✅ | TiDB ✅ | Pulsar ✅ | Grafana Mimir ✅ |
| | | ClickHouse ✅ | NATS ✅ | Pyroscope ✅ |
| | | OceanBase ✅ | HAProxy ✅ | Tempo ✅ |
| | | KingbaseES ✅ | Traefik ✅ | |
| | | Cassandra ✅ | Consul ✅ | |
| | | DynamoDB ✅ | | |

### Security Scanning

| Tool | Purpose |
|------|---------|
| Trivy ✅ | Image/filesystem/repo vulnerability scanning |
| Falco ✅ | K8s runtime security monitoring |
| OPA/Gatekeeper ✅ | Policy-as-code evaluation |
| kube-bench ✅ | K8s CIS benchmark security check |
| Kubescape ✅ | K8s security compliance (NSA/CISA) |

### Secret Management

| Tool | Purpose |
|------|---------|
| HashiCorp Vault ✅ | Secrets/certificates/dynamic credentials |

### Cloud Platforms

| Cloud | Services |
|-------|----------|
| AWS ✅ | EC2, RDS, S3, CloudFront, Lambda, EKS, DynamoDB, Cost Explorer |
| Alibaba Cloud ✅ | ECS, RDS, Redis, SLB, OSS, CDN, ACK |
| Huawei Cloud ✅ | ECS, RDS, OBS, CCE, Huawei Cloud Stack |
| Tencent Cloud ✅ | CVM, COS, CLB, TKE |
| Azure ✅ | VM, SQL, Blob, AKS, Cost Management |
| GCP ✅ | Compute, Cloud SQL, GKE, Cost |
| OpenStack ✅ | Nova, Neutron, Cinder |

### IaC & CI/CD & GitOps

| Tool | Purpose |
|------|---------|
| Terraform ✅ | Infrastructure as Code (init/plan/apply/state) |
| Ansible ✅ | Configuration Management (adhoc/playbook/inventory) |
| Helm ✅ | K8s Package Manager (list/status/history/rollback) |
| ArgoCD ✅ | K8s GitOps Continuous Deployment |
| FluxCD ✅ | Lightweight GitOps |
| Jenkins ✅ | CI/CD Pipeline |
| GitLab CI ✅ | GitLab CI/CD Pipeline |
| GitHub Actions ✅ | GitHub Workflows |
| Harbor ✅ | Enterprise Container Registry |

---

## 🤖 Supported Agents (20+)

| Layer | Agent | Description | Tools |
|-------|-------|-------------|:-----:|
| 🧠 Core | Planner | Task planning & orchestration | 2 |
| 🧠 Core | Copilot | AI chat assistant | 2 |
| 🔧 Ops | Linux | System diagnostics | 8 |
| 🔧 Ops | Docker | Docker/containerd operations | 7 |
| 🔧 Ops | K8s | Kubernetes management | 11 |
| 🔧 Ops | DB | Database diagnostics | 7 |
| 🔧 Ops | Middleware | Middleware management | 7 |
| 🔧 Ops | Network | Network operations | 5 |
| 🔧 Ops | Virtual | VMware/KVM/OpenStack | 5 |
| 🔧 Ops | Windows | Windows Server ops | 4 |
| 📊 Observability | Monitor | Metrics & alerting | 5 |
| 📊 Observability | Log | Log analysis | 4 |
| 📊 Observability | APM | SkyWalking/Jaeger tracing | 4 |
| 📊 Observability | SRE | SLO & incident management | 3 |
| 🔒 Security | Security | Vulnerability scanning | 6 |
| 🔒 Security | Incident | Incident response | 2 |
| 🔄 DevOps | DevOps | CI/CD automation | 3 |
| 🔄 DevOps | GitOps | ArgoCD/FluxCD | 5 |
| 🔄 DevOps | IaC | Terraform/Ansible/Helm | 10 |
| ☁️ Cloud | Cloud | Multi-cloud management | 6 |
| ☁️ Cloud | Cost | FinOps & cost optimization | 4 |
| ☁️ Cloud | ServiceMesh | Service mesh management | 2 |

---

## 🌍 Environment Topologies (18)

| Topology | Example |
|----------|---------|
| Pure On-Prem (Physical) | Manufacturing MES, Hospital HIS |
| Pure On-Prem (Virtual) | VMware/KVM cluster |
| Pure Container | K3s, Docker Compose |
| Pure Cloud | Alibaba Cloud full-managed |
| Serverless | Function Compute + API Gateway |
| Hosted Private Cloud | Huawei Cloud Stack |
| Hybrid (Virtual+Cloud) | Local IDC + Cloud bursting |
| Hybrid (Physical+Cloud) | Factory + Huawei Cloud |
| Hybrid (Container+Cloud) | SAP + Tencent Cloud |
| Multi-Cloud | AWS + Alibaba + Azure |
| Cross-Border | PIPL + GDPR compliance |
| Edge + Cloud | Factory edge AI + Cloud training |
| Multi-Active | Securities same-city dual-active RPO=0 |
| DR Standby | Cross-region disaster recovery RTO<15min |
| Domestic Full-Stack | Kylin + DM8 + TongWeb |
| Smart Manufacturing | Edge production line + Cloud AI |
| Smart City | Three-tier: Edge + Local + Cloud |
| E-commerce | Alibaba Cloud full-managed + elastic |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

[MIT License](LICENSE)
