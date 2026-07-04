"""环境配置数据模型 - 覆盖所有企业真实拓扑"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Optional


class EnvironmentType(str, enum.Enum):
    """环境拓扑类型 - 覆盖现实中所有企业部署形态 (18种)"""
    # ── 纯本地 ──
    PURE_ON_PREM = "pure_on_prem"            # 纯本地物理机
    PURE_VIRTUAL = "pure_virtual"            # 纯本地虚拟化 (VMware/KVM)
    PURE_CONTAINER = "pure_container"        # 纯本地容器 (K3s/K8s on bare metal)
    MULTI_SITE_ONPREM = "multi_site_onprem"  # 多站点本地 (总行+分行)
    DR_STANDBY = "dr_standby"                # 主备/灾备架构
    MULTI_ACTIVE = "multi_active"            # 多活架构 (双活/三活)
    # ── 纯云 ──
    PURE_CLOUD = "pure_cloud"                # 纯公有云 (单云)
    SERVERLESS_CLOUD = "serverless_cloud"    # 纯 Serverless (函数计算+API网关+OSS)
    HOSTED_PRIVATE = "hosted_private"        # 托管私有云 (华为云Stack/阿里Apsara Stack)
    # ── 混合 (本地+单云) ──
    HYBRID_VIRTUAL_CLOUD = "hybrid_virtual_cloud"  # 本地虚拟化 + 云
    HYBRID_PHYSICAL_CLOUD = "hybrid_physical_cloud"  # 本地物理机 + 云
    HYBRID_CONTAINER_CLOUD = "hybrid_container_cloud"  # 本地容器 + 云
    BURST_CLOUD = "burst_cloud"              # 弹性云扩展 (本地为主,峰值burst到云)
    # ── 多云 ──
    MULTI_CLOUD = "multi_cloud"              # 多公有云 (2+ 云厂商)
    HYBRID_MULTI_CLOUD = "hybrid_multi_cloud"  # 本地 + 多云
    # ── 跨境/边缘 ──
    CROSS_BORDER = "cross_border"            # 跨境: 境内云 + 境外云/本地
    EDGE = "edge"                            # 边缘 + 中心云
    FULL_EDGE = "full_edge"                  # 边缘+本地+云三层架构
    # ── 国产化 ──
    DOMESTIC_STACK = "domestic_stack"        # 国产化全栈 (华为云Stack+达梦+麒麟+TongWeb)


class CloudProvider(str, enum.Enum):
    """云厂商 - 国内外全覆盖"""
    # 国内云
    ALIYUN = "aliyun"          # 阿里云
    HUAWEI = "huawei"          # 华为云
    TENCENT = "tencent"        # 腾讯云
    BAIDU = "baidu"            # 百度智能云
    VOLCENGINE = "volcengine"  # 火山引擎
    UCloud = "ucloud"          # UCloud
    # 国际云
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ORACLE = "oracle"
    IBM = "ibm"


class InfraProvider(str, enum.Enum):
    """本地基础设施"""
    VMWARE = "vmware"      # vSphere / vCenter
    KVM = "kvm"            # KVM / libvirt
    PROXMOX = "proxmox"    # Proxmox VE
    OPENSTACK = "openstack"
    HYPERV = "hyperv"      # Hyper-V
    FUSIONSPHERE = "fusionsphere"  # 华为 FusionSphere
    AROUBA = "aikilai"     # 国产虚拟化


class NetworkZone(str, enum.Enum):
    """网络区域"""
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    DMZ = "dmz"
    MANAGEMENT = "management"
    EDGE = "edge"
    OVERSEAS = "overseas"


@dataclass
class CloudRegion:
    """云区域/可用区"""
    region_id: str                    # e.g. cn-hangzhou, ap-southeast-1
    region_name: str                  # e.g. 杭州, 新加坡
    provider: CloudProvider = CloudProvider.ALIYUN
    zones: list[str] = field(default_factory=list)  # 可用区列表
    network_zone: NetworkZone = NetworkZone.PRODUCTION
    latency_ms: Optional[float] = None  # 到主区域延迟


@dataclass
class OnPremSite:
    """本地数据中心/站点"""
    site_id: str
    site_name: str
    location: str = ""                # 地理位置
    network_zone: NetworkZone = NetworkZone.PRODUCTION
    infra_provider: InfraProvider = InfraProvider.VMWARE
    # 基础设施
    hypervisors: list[str] = field(default_factory=list)  # 物理主机列表
    storage_type: str = "SAN"         # SAN/NAS/Ceph/本地
    network_type: str = "10G"         # 网络带宽
    power_redundancy: bool = True     # 双路供电


@dataclass
class EdgeSite:
    """边缘站点"""
    site_id: str
    site_name: str
    location: str = ""
    device_type: str = "arm64"        # arm64/x86/gpu
    os: str = "Kylin V10"            # 操作系统
    connectivity: str = "VPN"         # VPN/专线/4G


@dataclass
class CrossBorderLink:
    """跨境链路"""
    link_id: str
    source_site: str                  # 源站点 ID
    target_site: str                  # 目标站点 ID
    link_type: str = "VPN"            # VPN/专线/SD-WAN
    bandwidth: str = "100Mbps"        # 带宽
    latency_ms: float = 0             # 延迟
    encrypted: bool = True            # 是否加密
    compliance: list[str] = field(default_factory=list)  # 合规要求: PIPL/GDPR


@dataclass
class ResourceSummary:
    """资源汇总"""
    total_servers: int = 0
    total_vms: int = 0
    total_containers: int = 0
    total_k8s_clusters: int = 0
    total_databases: int = 0
    total_network_devices: int = 0
    total_storage_tb: float = 0
    total_monthly_cost_yuan: float = 0


@dataclass
class EnvironmentHealth:
    """环境健康状态"""
    score: int = 100                  # 0-100
    status: str = "healthy"           # healthy/degraded/critical/offline
    last_check: str = ""
    issues: list[str] = field(default_factory=list)
    cross_region_latency_ms: float = 0  # 跨区域延迟


@dataclass
class Environment:
    """完整环境定义 - 一个企业可能有多个环境"""
    env_id: str
    env_name: str
    env_type: EnvironmentType
    description: str = ""
    # 云区域
    cloud_regions: list[CloudRegion] = field(default_factory=list)
    # 本地站点
    on_prem_sites: list[OnPremSite] = field(default_factory=list)
    # 边缘站点
    edge_sites: list[EdgeSite] = field(default_factory=list)
    # 跨境链路
    cross_border_links: list[CrossBorderLink] = field(default_factory=list)
    # 网络拓扑
    network_zones: list[NetworkZone] = field(default_factory=list)
    # VPN/专线连接
    interconnects: list[dict] = field(default_factory=list)
    # 资源汇总
    resources: ResourceSummary = field(default_factory=ResourceSummary)
    # 健康状态
    health: EnvironmentHealth = field(default_factory=EnvironmentHealth)
    # 标签
    tags: list[str] = field(default_factory=list)
    # 是否启用
    enabled: bool = True

    @property
    def all_providers(self) -> list[str]:
        """获取所有基础设施提供商"""
        providers = set()
        for r in self.cloud_regions:
            providers.add(r.provider.value)
        for s in self.on_prem_sites:
            providers.add(s.infra_provider.value)
        return sorted(providers)

    @property
    def all_regions(self) -> list[str]:
        """获取所有区域"""
        regions = []
        for r in self.cloud_regions:
            regions.append(f"{r.provider.value}:{r.region_id}")
        for s in self.on_prem_sites:
            regions.append(f"onprem:{s.site_id}")
        return regions

    @property
    def topology_label(self) -> str:
        """拓扑类型标签"""
        labels = {
            EnvironmentType.PURE_CLOUD: "纯云部署",
            EnvironmentType.PURE_ON_PREM: "纯本地物理机",
            EnvironmentType.PURE_VIRTUAL: "纯本地虚拟化",
            EnvironmentType.PURE_CONTAINER: "纯本地容器",
            EnvironmentType.MULTI_SITE_ONPREM: "多站点本地",
            EnvironmentType.DR_STANDBY: "主备/灾备",
            EnvironmentType.MULTI_ACTIVE: "多活架构",
            EnvironmentType.SERVERLESS_CLOUD: "Serverless",
            EnvironmentType.HOSTED_PRIVATE: "托管私有云",
            EnvironmentType.HYBRID_VIRTUAL_CLOUD: "混合云(虚拟+云)",
            EnvironmentType.HYBRID_PHYSICAL_CLOUD: "混合云(物理+云)",
            EnvironmentType.HYBRID_CONTAINER_CLOUD: "混合云(容器+云)",
            EnvironmentType.BURST_CLOUD: "弹性云扩展",
            EnvironmentType.MULTI_CLOUD: "多云部署",
            EnvironmentType.HYBRID_MULTI_CLOUD: "混合多云",
            EnvironmentType.CROSS_BORDER: "跨境部署",
            EnvironmentType.EDGE: "边缘+中心云",
            EnvironmentType.FULL_EDGE: "边缘+本地+云",
            EnvironmentType.DOMESTIC_STACK: "国产化全栈",
        }
        return labels.get(self.env_type, self.env_type.value)

    @property
    def topology_icon(self) -> str:
        icons = {
            EnvironmentType.PURE_CLOUD: "☁️",
            EnvironmentType.PURE_ON_PREM: "🏢",
            EnvironmentType.PURE_VIRTUAL: "🖥️",
            EnvironmentType.PURE_CONTAINER: "🐳",
            EnvironmentType.MULTI_SITE_ONPREM: "🏛️",
            EnvironmentType.DR_STANDBY: "🔄",
            EnvironmentType.MULTI_ACTIVE: "⚡",
            EnvironmentType.SERVERLESS_CLOUD: "λ",
            EnvironmentType.HOSTED_PRIVATE: "🏰",
            EnvironmentType.HYBRID_VIRTUAL_CLOUD: "🔗",
            EnvironmentType.HYBRID_PHYSICAL_CLOUD: "🔗",
            EnvironmentType.HYBRID_CONTAINER_CLOUD: "🔗",
            EnvironmentType.BURST_CLOUD: "🚀",
            EnvironmentType.MULTI_CLOUD: "🌐",
            EnvironmentType.HYBRID_MULTI_CLOUD: "🌐",
            EnvironmentType.CROSS_BORDER: "🌍",
            EnvironmentType.EDGE: "📡",
            EnvironmentType.FULL_EDGE: "📡",
            EnvironmentType.DOMESTIC_STACK: "🇨🇳",
        }
        return icons.get(self.env_type, "❓")

    def to_dict(self) -> dict:
        return {
            "env_id": self.env_id,
            "env_name": self.env_name,
            "env_type": self.env_type.value,
            "topology_label": self.topology_label,
            "topology_icon": self.topology_icon,
            "description": self.description,
            "cloud_regions": [
                {"region_id": r.region_id, "region_name": r.region_name,
                 "provider": r.provider.value, "zones": r.zones,
                 "network_zone": r.network_zone.value, "latency_ms": r.latency_ms}
                for r in self.cloud_regions
            ],
            "on_prem_sites": [
                {"site_id": s.site_id, "site_name": s.site_name,
                 "location": s.location, "infra_provider": s.infra_provider.value,
                 "network_zone": s.network_zone.value, "storage_type": s.storage_type}
                for s in self.on_prem_sites
            ],
            "edge_sites": [
                {"site_id": e.site_id, "site_name": e.site_name,
                 "location": e.location, "device_type": e.device_type,
                 "os": e.os, "connectivity": e.connectivity}
                for e in self.edge_sites
            ],
            "cross_border_links": [
                {"link_id": l.link_id, "source": l.source_site, "target": l.target_site,
                 "link_type": l.link_type, "bandwidth": l.bandwidth,
                 "latency_ms": l.latency_ms, "encrypted": l.encrypted,
                 "compliance": l.compliance}
                for l in self.cross_border_links
            ],
            "network_zones": [z.value for z in self.network_zones],
            "interconnects": self.interconnects,
            "resources": {
                "total_servers": self.resources.total_servers,
                "total_vms": self.resources.total_vms,
                "total_containers": self.resources.total_containers,
                "total_k8s_clusters": self.resources.total_k8s_clusters,
                "total_databases": self.resources.total_databases,
                "total_network_devices": self.resources.total_network_devices,
                "total_storage_tb": self.resources.total_storage_tb,
                "total_monthly_cost_yuan": self.resources.total_monthly_cost_yuan,
            },
            "health": {
                "score": self.health.score,
                "status": self.health.status,
                "last_check": self.health.last_check,
                "issues": self.health.issues,
                "cross_region_latency_ms": self.health.cross_region_latency_ms,
            },
            "all_providers": self.all_providers,
            "all_regions": self.all_regions,
            "tags": self.tags,
            "enabled": self.enabled,
        }
