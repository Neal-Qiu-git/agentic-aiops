"""环境发现工具 - 自动探测系统环境、推荐 Agent 组合"""
import json
import os
import platform
import re
import shutil
import subprocess
from typing import Any


def _run(cmd: str, timeout: int = 5) -> str:
    """安全执行命令"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


# ══════════════════════════════════════════════════════════
# 1. 操作系统探测
# ══════════════════════════════════════════════════════════

def detect_os() -> dict:
    """探测操作系统信息"""
    system = platform.system()
    info = {
        "os_type": system.lower(),
        "os_name": "",
        "os_version": "",
        "kernel": platform.release(),
        "arch": platform.machine(),
        "hostname": platform.node(),
    }

    if system == "Linux":
        # 发行版
        name = _run("cat /etc/os-release 2>/dev/null | grep ^NAME= | cut -d'\"' -f2")
        version = _run("cat /etc/os-release 2>/dev/null | grep ^VERSION_ID= | cut -d'\"' -f2")
        info["os_name"] = name or _run("lsb_release -si 2>/dev/null") or "Linux"
        info["os_version"] = version or _run("lsb_release -sr 2>/dev/null") or ""

        # 国产操作系统检测
        if "kylin" in name.lower() or "kylin" in _run("cat /etc/os-release 2>/dev/null").lower():
            info["os_name"] = "银河麒麟 " + (info["os_version"] or "")
            info["domestic_os"] = True
        elif "uos" in name.lower() or "uniontech" in _run("cat /etc/os-release 2>/dev/null").lower():
            info["os_name"] = "统信UOS " + (info["os_version"] or "")
            info["domestic_os"] = True
        elif "openEuler" in name:
            info["os_name"] = "openEuler " + info["os_version"]
            info["domestic_os"] = True
        elif "centos" in name.lower():
            info["os_name"] = "CentOS " + info["os_version"]

    elif system == "Windows":
        info["os_name"] = f"Windows {platform.version()}"
        info["os_version"] = platform.version()

    return info


# ══════════════════════════════════════════════════════════
# 2. 硬件探测
# ══════════════════════════════════════════════════════════

def detect_hardware() -> dict:
    """探测硬件信息"""
    info = {
        "cpu_cores": os.cpu_count() or 0,
        "arch": platform.machine(),
    }

    # 内存
    mem = _run("free -m 2>/dev/null | awk '/Mem:/{print $2}'")
    info["memory_mb"] = int(mem) if mem.isdigit() else 0
    info["memory_gb"] = round(info["memory_mb"] / 1024, 1)

    # 磁盘
    disk = _run("df -BG / 2>/dev/null | awk 'NR==2{print $2}'")
    info["disk_gb"] = int(disk.replace("G", "")) if disk.replace("G", "").isdigit() else 0

    # 负载
    load = _run("cat /proc/loadavg 2>/dev/null | awk '{print $1}'")
    info["load_1m"] = float(load) if load else 0

    # 是否虚拟机
    info["is_virtual"] = False
    info["virtual_type"] = ""
    virt = _run("systemd-detect-virt 2>/dev/null")
    if virt and virt != "none":
        info["is_virtual"] = True
        info["virtual_type"] = virt
    elif _run("grep -q 'hypervisor' /proc/cpuinfo 2>/dev/null && echo yes") == "yes":
        info["is_virtual"] = True
        info["virtual_type"] = "kvm"
    elif _run("dmidecode -s system-product-name 2>/dev/null"):
        product = _run("dmidecode -s system-product-name 2>/dev/null")
        if "vmware" in product.lower() or "virtualbox" in product.lower():
            info["is_virtual"] = True
            info["virtual_type"] = product.lower().replace("vmware ", "")

    return info


# ══════════════════════════════════════════════════════════
# 3. 云平台探测
# ══════════════════════════════════════════════════════════

def detect_cloud() -> dict:
    """探测云平台 (通过 metadata API)"""
    info = {"is_cloud": False, "provider": "", "region": "", "instance_type": "", "instance_id": ""}

    cloud_checks = [
        # 阿里云
        {"url": "http://100.100.100.200/latest/meta-data/instance-id",
         "provider": "aliyun",
         "region_url": "http://100.100.100.200/latest/meta-data/region-id",
         "type_url": "http://100.100.100.200/latest/meta-data/instance/instance-type"},
        # 华为云
        {"url": "http://169.254.169.254/latest/meta-data/instance-id",
         "provider": "huawei",
         "region_url": "http://169.254.169.254/latest/meta-data/availability-zone",
         "type_url": "http://169.254.169.254/latest/meta-data/flavor"},
        # AWS
        {"url": "http://169.254.169.254/latest/meta-data/instance-id",
         "provider": "aws",
         "region_url": "http://169.254.169.254/latest/meta-data/placement/region",
         "type_url": "http://169.254.169.254/latest/meta-data/instance-type"},
        # 腾讯云
        {"url": "http://metadata.tencentyun.com/latest/meta-data/instance-id",
         "provider": "tencent",
         "region_url": "http://metadata.tencentyun.com/latest/meta-data/placement/region",
         "type_url": "http://metadata.tencentyun.com/latest/meta-data/instance-type"},
    ]

    for check in cloud_checks:
        try:
            result = _run(f"curl -s --connect-timeout 2 {check['url']}", timeout=3)
            if result and not "error" in result.lower() and "localhost" not in result:
                info["is_cloud"] = True
                info["provider"] = check["provider"]
                info["instance_id"] = result
                info["region"] = _run(f"curl -s --connect-timeout 2 {check['region_url']}", timeout=3)
                info["instance_type"] = _run(f"curl -s --connect-timeout 2 {check['type_url']}", timeout=3)
                break
        except Exception:
            continue

    return info


# ══════════════════════════════════════════════════════════
# 4. 容器/K8s 探测
# ══════════════════════════════════════════════════════════

def detect_containers() -> dict:
    """探测容器运行时"""
    info = {"docker": False, "docker_version": "", "docker_running": False,
            "containerd": False, "podman": False, "k3s": False}

    # Docker
    if shutil.which("docker"):
        info["docker"] = True
        info["docker_version"] = _run("docker version --format '{{.Server.Version}}' 2>/dev/null")
        info["docker_running"] = _run("docker info --format '{{.ServerVersion}}' 2>/dev/null") != ""

    # containerd
    if shutil.which("ctr") or os.path.exists("/run/containerd/containerd.sock"):
        info["containerd"] = True

    # Podman
    if shutil.which("podman"):
        info["podman"] = True

    # K3s
    if os.path.exists("/etc/rancher/k3s/k3s.yaml") or shutil.which("k3s"):
        info["k3s"] = True

    return info


def detect_kubernetes() -> dict:
    """探测 Kubernetes"""
    info = {"available": False, "version": "", "nodes": 0, "namespaces": 0,
            "pods": 0, "services": 0, "deployments": 0, "provider": ""}

    if not shutil.which("kubectl"):
        return info

    # 检查 kubectl 是否能连接
    version = _run("kubectl version --short 2>/dev/null | head -1")
    if not version:
        return info

    info["available"] = True
    info["version"] = version

    # 节点数
    nodes = _run("kubectl get nodes --no-headers 2>/dev/null | wc -l")
    info["nodes"] = int(nodes) if nodes.isdigit() else 0

    # 命名空间
    ns = _run("kubectl get ns --no-headers 2>/dev/null | wc -l")
    info["namespaces"] = int(ns) if ns.isdigit() else 0

    # Pods
    pods = _run("kubectl get pods --all-namespaces --no-headers 2>/dev/null | wc -l")
    info["pods"] = int(pods) if pods.isdigit() else 0

    # 云厂商 K8s 检测
    provider_hints = {
        "alicloud": "aliyun", "aws": "aws", "gce": "gcp",
        "azure": "azure", "huawei": "huawei", "tencent": "tencent",
    }
    node_info = _run("kubectl get nodes -o json 2>/dev/null | head -100")
    for hint, provider in provider_hints.items():
        if hint in node_info.lower():
            info["provider"] = provider
            break

    return info


# ══════════════════════════════════════════════════════════
# 5. 中间件探测
# ══════════════════════════════════════════════════════════

def detect_middleware() -> list[dict]:
    """探测运行中的中间件"""
    middlewares = []

    checks = [
        {"name": "Nginx", "cmd": "nginx -v 2>&1 | head -1", "port_cmd": "ss -tlnp 2>/dev/null | grep ':80\\|:443' | head -1", "process": "nginx"},
        {"name": "Redis", "cmd": "redis-cli --version 2>/dev/null", "port_cmd": "ss -tlnp 2>/dev/null | grep ':6379' | head -1", "process": "redis"},
        {"name": "MySQL", "cmd": "mysql --version 2>/dev/null", "port_cmd": "ss -tlnp 2>/dev/null | grep ':3306' | head -1", "process": "mysql"},
        {"name": "PostgreSQL", "cmd": "psql --version 2>/dev/null", "port_cmd": "ss -tlnp 2>/dev/null | grep ':5432' | head -1", "process": "postgres"},
        {"name": "MongoDB", "cmd": "mongod --version 2>/dev/null | head -1", "port_cmd": "ss -tlnp 2>/dev/null | grep ':27017' | head -1", "process": "mongod"},
        {"name": "RabbitMQ", "cmd": "rabbitmqctl status 2>/dev/null | grep RabbitMQ | head -1 || rabbitmq-server --version 2>/dev/null", "port_cmd": "ss -tlnp 2>/dev/null | grep ':5672\\|:15672' | head -1", "process": "rabbitmq"},
        {"name": "Kafka", "cmd": "kafka-server-start.sh --version 2>/dev/null || /opt/kafka/bin/kafka-server-start.sh --version 2>/dev/null", "port_cmd": "ss -tlnp 2>/dev/null | grep ':9092' | head -1", "process": "kafka"},
        {"name": "Elasticsearch", "cmd": "curl -s http://localhost:9200 2>/dev/null | grep cluster_name", "port_cmd": "ss -tlnp 2>/dev/null | grep ':9200' | head -1", "process": "elastic"},
        {"name": "Tomcat", "cmd": "catalina.sh version 2>/dev/null | head -1 || /opt/tomcat/bin/catalina.sh version 2>/dev/null | head -1", "port_cmd": "ss -tlnp 2>/dev/null | grep ':8080' | head -1", "process": "java.*tomcat"},
        {"name": "TongWeb", "cmd": "find /opt /data -name 'version.xml' 2>/dev/null | grep -i tongweb | head -1", "port_cmd": "ss -tlnp 2>/dev/null | grep ':9060\\|:8088' | head -1", "process": "tongweb"},
    ]

    for check in checks:
        version = _run(check["cmd"], timeout=5)
        if version:
            running = _run(check["port_cmd"]) != ""
            middlewares.append({
                "name": check["name"],
                "version": version[:80],
                "running": running,
            })

    # systemd 服务检测补充
    for svc in ["nginx", "redis", "mysql", "postgresql", "mongod", "rabbitmq-server", "kafka"]:
        if not any(m["name"].lower().startswith(svc.split("-")[0]) for m in middlewares):
            status = _run(f"systemctl is-active {svc} 2>/dev/null")
            if status == "active":
                middlewares.append({"name": svc, "version": "", "running": True})

    return middlewares


# ══════════════════════════════════════════════════════════
# 6. 数据库探测
# ══════════════════════════════════════════════════════════

def detect_databases() -> list[dict]:
    """探测数据库"""
    dbs = []
    checks = [
        {"name": "MySQL", "cmd": "mysql --version 2>/dev/null", "port": 3306},
        {"name": "PostgreSQL", "cmd": "psql --version 2>/dev/null", "port": 5432},
        {"name": "Redis", "cmd": "redis-cli --version 2>/dev/null", "port": 6379},
        {"name": "MongoDB", "cmd": "mongod --version 2>/dev/null | head -1", "port": 27017},
        {"name": "达梦DM8", "cmd": "dmserver --version 2>/dev/null || find /opt/dm* -name 'dmserver' 2>/dev/null | head -1", "port": 5236},
        {"name": "OceanBase", "cmd": "obclient --version 2>/dev/null", "port": 2881},
        {"name": "TiDB", "cmd": "tidb-server --version 2>/dev/null", "port": 4000},
    ]

    for check in checks:
        version = _run(check["cmd"], timeout=5)
        if version:
            port_open = _run(f"ss -tlnp 2>/dev/null | grep ':{check['port']}' | head -1") != ""
            dbs.append({"name": check["name"], "version": version[:80], "port": check["port"], "running": port_open})

    return dbs


# ══════════════════════════════════════════════════════════
# 7. 网络探测
# ══════════════════════════════════════════════════════════

def detect_network() -> dict:
    """探测网络信息"""
    info = {"interfaces": [], "public_ip": "", "private_ip": "", "dns": []}

    # IP 地址
    info["private_ip"] = _run("hostname -I 2>/dev/null | awk '{print $1}'")
    info["public_ip"] = _run("curl -s --connect-timeout 3 http://ifconfig.me 2>/dev/null")

    # DNS
    info["dns"] = _run("cat /etc/resolv.conf 2>/dev/null | grep nameserver | awk '{print $2}'").split("\n")[:3]

    # 网络接口
    interfaces = _run("ip -o link show 2>/dev/null | awk -F': ' '{print $2}'").split("\n")
    for iface in interfaces[:5]:
        if iface and iface != "lo":
            ip = _run(f"ip addr show {iface} 2>/dev/null | grep 'inet ' | awk '{{print $2}}' | head -1")
            info["interfaces"].append({"name": iface, "ip": ip})

    return info


# ══════════════════════════════════════════════════════════
# 8. 应用/服务探测
# ══════════════════════════════════════════════════════════

def detect_services() -> dict:
    """探测运行中的服务"""
    info = {"systemd_count": 0, "docker_containers": 0, "k8s_pods": 0,
            "listening_ports": [], "top_processes": []}

    # systemd 服务数
    active = _run("systemctl list-units --type=service --state=active --no-legend 2>/dev/null | wc -l")
    info["systemd_count"] = int(active) if active.isdigit() else 0

    # Docker 容器数
    containers = _run("docker ps -q 2>/dev/null | wc -l")
    info["docker_containers"] = int(containers) if containers.isdigit() else 0

    # 监听端口
    ports = _run("ss -tlnp 2>/dev/null | tail -n +2 | awk '{print $4}' | sed 's/.*://' | sort -un | head -20")
    info["listening_ports"] = [int(p) for p in ports.split("\n") if p.isdigit()]

    # 高资源进程
    top = _run("ps aux --sort=-%mem 2>/dev/null | head -6 | tail -5 | awk '{printf \"%s %.1f%%mem %.1f%%cpu\\n\", $11, $4, $3}'")
    info["top_processes"] = top.split("\n") if top else []

    return info


# ══════════════════════════════════════════════════════════
# 9. 部署方式探测
# ══════════════════════════════════════════════════════════

def detect_deployment() -> dict:
    """探测部署方式"""
    info = {"docker_compose": False, "k8s_deployment": False, "systemd_services": 0,
            "ansible": False, "terraform": False, "helm": False, "gitops": False}

    # Docker Compose
    if shutil.which("docker-compose") or _run("docker compose version 2>/dev/null"):
        info["docker_compose"] = True

    # Ansible
    if shutil.which("ansible"):
        info["ansible"] = True

    # Terraform
    if shutil.which("terraform"):
        info["terraform"] = True

    # Helm
    if shutil.which("helm"):
        info["helm"] = True

    # GitOps (ArgoCD/Flux)
    if shutil.which("argocd"):
        info["gitops"] = True

    return info


# ══════════════════════════════════════════════════════════
# 10. 全量探测 + Agent 推荐
# ══════════════════════════════════════════════════════════

def full_discovery() -> dict:
    """执行全量环境探测"""
    os_info = detect_os()
    hw_info = detect_hardware()
    cloud_info = detect_cloud()
    container_info = detect_containers()
    k8s_info = detect_kubernetes()
    middleware_info = detect_middleware()
    db_info = detect_databases()
    network_info = detect_network()
    services_info = detect_services()
    deploy_info = detect_deployment()

    # 推荐 Agent 组合
    recommended_agents = _recommend_agents(
        os_info, hw_info, cloud_info, container_info, k8s_info,
        middleware_info, db_info, deploy_info,
        network_info, services_info
    )

    # 推荐环境拓扑
    topology = _infer_topology(os_info, cloud_info, container_info, k8s_info, hw_info)

    return {
        "os": os_info,
        "hardware": hw_info,
        "cloud": cloud_info,
        "containers": container_info,
        "kubernetes": k8s_info,
        "middleware": middleware_info,
        "databases": db_info,
        "network": network_info,
        "services": services_info,
        "deployment": deploy_info,
        "recommended_agents": recommended_agents,
        "inferred_topology": topology,
    }


def _recommend_agents(os_info, hw_info, cloud_info, container_info, k8s_info,
                      middleware_info, db_info, deploy_info, network_info=None, services_info=None) -> list[dict]:
    network_info = network_info or {}
    services_info = services_info or {}
    """根据探测结果推荐 Agent 组合"""
    agents = []

    # 基础设施 Agent (必选)
    agents.append({
        "name": "linux", "icon": "🐧", "reason": "系统基础监控与诊断",
        "priority": "high", "category": "基础",
    })

    if os_info.get("os_type") == "windows":
        agents.append({
            "name": "windows", "icon": "🪟", "reason": "Windows Server 运维",
            "priority": "high", "category": "基础",
        })

    # 云 Agent
    if cloud_info.get("is_cloud"):
        agents.append({
            "name": "cloud", "icon": "☁️",
            "reason": f"检测到 {cloud_info['provider']} 云平台",
            "priority": "high", "category": "基础设施",
        })

    # 虚拟化 Agent
    if hw_info.get("is_virtual"):
        agents.append({
            "name": "virtual", "icon": "🖥️",
            "reason": f"检测到虚拟化环境 ({hw_info.get('virtual_type', '')})",
            "priority": "medium", "category": "基础设施",
        })

    # 容器 Agent
    if container_info.get("docker"):
        agents.append({
            "name": "docker", "icon": "🐳", "reason": "检测到 Docker 运行时",
            "priority": "high", "category": "容器",
        })

    # K8s Agent
    if k8s_info.get("available"):
        agents.append({
            "name": "k8s", "icon": "☸️",
            "reason": f"检测到 Kubernetes {k8s_info.get('version', '')}",
            "priority": "high", "category": "容器",
        })

    # 数据库 Agent
    if db_info:
        db_names = [d["name"] for d in db_info]
        agents.append({
            "name": "db", "icon": "🗄️",
            "reason": f"检测到数据库: {', '.join(db_names)}",
            "priority": "high", "category": "数据",
        })

    # 中间件 Agent
    if middleware_info:
        mw_names = [m["name"] for m in middleware_info]
        agents.append({
            "name": "middleware", "icon": "📦",
            "reason": f"检测到中间件: {', '.join(mw_names)}",
            "priority": "high", "category": "中间件",
        })

    # 网络 Agent (有防火墙/多网卡时推荐)
    if len(network_info.get("interfaces", [])) > 1:
        agents.append({
            "name": "network", "icon": "🌐", "reason": "检测到多网络接口",
            "priority": "medium", "category": "网络",
        })

    # DevOps Agent (有 CI/CD 工具时)
    if deploy_info.get("docker_compose") or deploy_info.get("helm") or deploy_info.get("gitops"):
        tools = []
        if deploy_info.get("docker_compose"): tools.append("Docker Compose")
        if deploy_info.get("helm"): tools.append("Helm")
        if deploy_info.get("gitops"): tools.append("GitOps")
        agents.append({
            "name": "devops", "icon": "🚀",
            "reason": f"检测到部署工具: {', '.join(tools)}",
            "priority": "medium", "category": "DevOps",
        })

    # IaC Agent
    if deploy_info.get("terraform") or deploy_info.get("ansible"):
        tools = []
        if deploy_info.get("terraform"): tools.append("Terraform")
        if deploy_info.get("ansible"): tools.append("Ansible")
        agents.append({
            "name": "iac", "icon": "🏗️",
            "reason": f"检测到 IaC 工具: {', '.join(tools)}",
            "priority": "medium", "category": "DevOps",
        })

    # 安全 Agent (始终推荐)
    agents.append({
        "name": "security", "icon": "🔒", "reason": "安全扫描与合规检查",
        "priority": "medium", "category": "安全",
    })

    # 监控 Agent (始终推荐)
    agents.append({
        "name": "monitor", "icon": "📊", "reason": "系统监控与告警",
        "priority": "high", "category": "监控",
    })

    # SRE Agent (有 K8s 或多服务时推荐)
    if k8s_info.get("available") or services_info.get("systemd_count", 0) > 10:
        agents.append({
            "name": "sre", "icon": "🏥", "reason": "SLI/SLO 管理",
            "priority": "medium", "category": "运维",
        })

    # 事件 Agent (始终推荐)
    agents.append({
        "name": "incident", "icon": "🚨", "reason": "故障应急响应",
        "priority": "medium", "category": "运维",
    })

    # Planner (始终推荐)
    agents.append({
        "name": "planner", "icon": "📋", "reason": "任务编排调度",
        "priority": "high", "category": "核心",
    })

    # Copilot (始终推荐)
    agents.append({
        "name": "copilot", "icon": "🤖", "reason": "AI 对话助手",
        "priority": "medium", "category": "核心",
    })

    return agents


def _infer_topology(os_info, cloud_info, container_info, k8s_info, hw_info) -> dict:
    """根据探测结果推断环境拓扑"""
    is_cloud = cloud_info.get("is_cloud", False)
    is_virtual = hw_info.get("is_virtual", False)
    has_k8s = k8s_info.get("available", False)
    has_docker = container_info.get("docker", False)
    provider = cloud_info.get("provider", "")

    if is_cloud and not is_virtual:
        if has_k8s:
            return {"type": "pure_cloud", "label": "☁️ 纯云 (Kubernetes)", "confidence": 90}
        return {"type": "pure_cloud", "label": "☁️ 纯云部署", "confidence": 85}

    if is_cloud and is_virtual:
        if has_k8s:
            return {"type": "pure_cloud", "label": f"☁️ {provider} 云 (容器化)", "confidence": 80}
        return {"type": "pure_cloud", "label": f"☁️ {provider} 云 (VM)", "confidence": 75}

    if is_virtual and not is_cloud:
        if has_docker or has_k8s:
            return {"type": "pure_container", "label": "🐳 本地容器环境", "confidence": 70}
        return {"type": "pure_virtual", "label": "🖥️ 本地虚拟化", "confidence": 80}

    if not is_virtual and not is_cloud:
        if has_docker or has_k8s:
            return {"type": "pure_container", "label": "🐳 本地容器 (bare metal)", "confidence": 75}
        return {"type": "pure_on_prem", "label": "🏢 本地物理机", "confidence": 85}

    return {"type": "unknown", "label": "❓ 未识别", "confidence": 0}
