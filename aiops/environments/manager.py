"""环境管理器 - 加载配置、健康检查、跨环境路由"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Optional

import yaml

from .models import (
    CloudProvider,
    CloudRegion,
    CrossBorderLink,
    EdgeSite,
    Environment,
    EnvironmentHealth,
    EnvironmentType,
    InfraProvider,
    NetworkZone,
    OnPremSite,
    ResourceSummary,
)


# ── Demo 环境数据 (无配置文件时使用) ──

def _build_demo_environments() -> list[Environment]:
    """构建 Demo 环境数据 - 覆盖全部 9 种拓扑类型"""
    return [
        # 1. 纯云 (阿里云)
        Environment(
            env_id="env-prod-aliyun",
            env_name="生产环境 - 阿里云",
            env_type=EnvironmentType.PURE_CLOUD,
            description="全站生产环境，部署在阿里云华东2，单一云厂商",
            cloud_regions=[
                CloudRegion("cn-shanghai", "上海", CloudProvider.ALIYUN,
                            ["cn-shanghai-h", "cn-shanghai-i"], NetworkZone.PRODUCTION),
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.DMZ],
            resources=ResourceSummary(
                total_servers=0, total_vms=0, total_containers=156,
                total_k8s_clusters=2, total_databases=8, total_network_devices=0,
                total_storage_tb=12.5, total_monthly_cost_yuan=85000,
            ),
            health=EnvironmentHealth(score=98, status="healthy", last_check="刚刚", cross_region_latency_ms=0),
            tags=["production", "aliyun", "core"],
        ),
        # 2. 纯本地物理机
        Environment(
            env_id="env-bank-onprem",
            env_name="银行核心系统 - 本地物理机",
            env_type=EnvironmentType.PURE_ON_PREM,
            description="银行核心业务系统，全部部署在本地数据中心，符合金融监管要求",
            on_prem_sites=[
                OnPremSite("dc-hq", "总部数据中心", "泸州", NetworkZone.PRODUCTION,
                           storage_type="SAN", network_type="万兆"),
                OnPremSite("dc-dr", "灾备数据中心", "成都", NetworkZone.PRODUCTION,
                           storage_type="SAN", network_type="万兆"),
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.MANAGEMENT, NetworkZone.DMZ],
            resources=ResourceSummary(
                total_servers=45, total_vms=120, total_containers=0,
                total_k8s_clusters=0, total_databases=15, total_network_devices=32,
                total_storage_tb=200, total_monthly_cost_yuan=0,
            ),
            health=EnvironmentHealth(score=99, status="healthy", last_check="刚刚", cross_region_latency_ms=2.3),
            tags=["production", "banking", "compliance", "on-premise"],
        ),
        # 3. 纯本地虚拟化
        Environment(
            env_id="env-dev-virtual",
            env_name="开发测试环境 - VMware",
            env_type=EnvironmentType.PURE_VIRTUAL,
            description="开发测试环境，VMware vSphere 虚拟化平台",
            on_prem_sites=[
                OnPremSite("dc-dev", "开发机房", "泸州", NetworkZone.DEVELOPMENT,
                           InfraProvider.VMWARE, storage_type="NAS"),
            ],
            network_zones=[NetworkZone.DEVELOPMENT, NetworkZone.STAGING],
            resources=ResourceSummary(
                total_servers=3, total_vms=35, total_containers=10,
                total_k8s_clusters=1, total_databases=6, total_network_devices=4,
                total_storage_tb=15, total_monthly_cost_yuan=0,
            ),
            health=EnvironmentHealth(score=95, status="healthy", last_check="刚刚"),
            tags=["development", "vmware"],
        ),
        # 4. 混合云 (本地虚拟化 + 华为云)
        Environment(
            env_id="env-prod-hybrid",
            env_name="生产混合环境 - VMware + 华为云",
            env_type=EnvironmentType.HYBRID_VIRTUAL_CLOUD,
            description="核心系统在本地 VMware，前端/移动端在华为云，通过专线互联",
            cloud_regions=[
                CloudRegion("cn-north-4", "北京四", CloudProvider.HUAWEI,
                            ["cn-north-4a", "cn-north-4b"], NetworkZone.PRODUCTION, 3.2),
            ],
            on_prem_sites=[
                OnPremSite("dc-core", "核心机房", "泸州", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
            ],
            interconnects=[
                {"type": "专线", "bandwidth": "1Gbps", "latency_ms": 3.2,
                 "source": "dc-core", "target": "cn-north-4"},
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.DMZ, NetworkZone.MANAGEMENT],
            resources=ResourceSummary(
                total_servers=8, total_vms=65, total_containers=80,
                total_k8s_clusters=2, total_databases=10, total_network_devices=12,
                total_storage_tb=80, total_monthly_cost_yuan=42000,
            ),
            health=EnvironmentHealth(score=96, status="healthy", last_check="刚刚", cross_region_latency_ms=3.2),
            tags=["production", "hybrid", "vmware", "huawei"],
        ),
        # 5. 多云 (阿里 + 华为 + AWS)
        Environment(
            env_id="env-multi-cloud",
            env_name="多云业务环境",
            env_type=EnvironmentType.MULTI_CLOUD,
            description="国内业务在阿里云/华为云，海外业务在 AWS，三云统一管控",
            cloud_regions=[
                CloudRegion("cn-hangzhou", "杭州", CloudProvider.ALIYUN,
                            ["cn-hangzhou-b"], NetworkZone.PRODUCTION),
                CloudRegion("cn-north-1", "北京", CloudProvider.HUAWEI,
                            ["cn-north-1a"], NetworkZone.PRODUCTION, 12.5),
                CloudRegion("ap-southeast-1", "新加坡", CloudProvider.AWS,
                            ["ap-southeast-1a"], NetworkZone.OVERSEAS, 45.0),
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.OVERSEAS],
            interconnects=[
                {"type": "VPN", "bandwidth": "200Mbps", "latency_ms": 12.5,
                 "source": "cn-hangzhou", "target": "cn-north-1"},
                {"type": "专线", "bandwidth": "500Mbps", "latency_ms": 45.0,
                 "source": "cn-hangzhou", "target": "ap-southeast-1"},
            ],
            resources=ResourceSummary(
                total_servers=0, total_vms=0, total_containers=320,
                total_k8s_clusters=5, total_databases=18, total_network_devices=0,
                total_storage_tb=45, total_monthly_cost_yuan=186000,
            ),
            health=EnvironmentHealth(score=94, status="healthy", last_check="刚刚", cross_region_latency_ms=45.0),
            tags=["production", "multi-cloud", "aliyun", "huawei", "aws"],
        ),
        # 6. 混合多云 (本地 + 多云)
        Environment(
            env_id="env-hybrid-multi",
            env_name="全栈混合多云",
            env_type=EnvironmentType.HYBRID_MULTI_CLOUD,
            description="核心数据在本地 VMware，计算在华为云，CDN/边缘在腾讯云，海外在 AWS",
            cloud_regions=[
                CloudRegion("cn-north-4", "北京四", CloudProvider.HUAWEI,
                            ["cn-north-4a"], NetworkZone.PRODUCTION),
                CloudRegion("ap-guangzhou", "广州", CloudProvider.TENCENT,
                            ["ap-guangzhou-2"], NetworkZone.PRODUCTION),
                CloudRegion("us-east-1", "弗吉尼亚", CloudProvider.AWS,
                            ["us-east-1a"], NetworkZone.OVERSEAS, 180.0),
            ],
            on_prem_sites=[
                OnPremSite("dc-core", "总部机房", "泸州", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
            ],
            interconnects=[
                {"type": "专线", "bandwidth": "1Gbps", "latency_ms": 3.0,
                 "source": "dc-core", "target": "cn-north-4"},
                {"type": "VPN", "bandwidth": "200Mbps", "latency_ms": 25.0,
                 "source": "cn-north-4", "target": "ap-guangzhou"},
                {"type": "VPN", "bandwidth": "100Mbps", "latency_ms": 180.0,
                 "source": "cn-north-4", "target": "us-east-1"},
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.OVERSEAS, NetworkZone.DMZ],
            resources=ResourceSummary(
                total_servers=12, total_vms=85, total_containers=280,
                total_k8s_clusters=4, total_databases=22, total_network_devices=18,
                total_storage_tb=150, total_monthly_cost_yuan=235000,
            ),
            health=EnvironmentHealth(score=91, status="degraded", last_check="刚刚",
                                     issues=["us-east-1 延迟偏高: 180ms"], cross_region_latency_ms=180.0),
            tags=["production", "hybrid", "multi-cloud", "global"],
        ),
        # 7. 跨境部署
        Environment(
            env_id="env-cross-border",
            env_name="跨境合规环境",
            env_type=EnvironmentType.CROSS_BORDER,
            description="境内: 阿里云杭州(用户数据不出境), 境外: AWS 新加坡(海外服务), 链路加密+PIPL合规",
            cloud_regions=[
                CloudRegion("cn-hangzhou", "杭州", CloudProvider.ALIYUN,
                            ["cn-hangzhou-b"], NetworkZone.PRODUCTION),
                CloudRegion("ap-southeast-1", "新加坡", CloudProvider.AWS,
                            ["ap-southeast-1a"], NetworkZone.OVERSEAS, 52.0),
            ],
            cross_border_links=[
                CrossBorderLink("link-sg", "cn-hangzhou", "ap-southeast-1",
                                "IPSec VPN", "200Mbps", 52.0, True, ["PIPL", "PDPA"]),
            ],
            interconnects=[
                {"type": "IPSec VPN", "bandwidth": "200Mbps", "latency_ms": 52.0,
                 "source": "cn-hangzhou", "target": "ap-southeast-1"},
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.OVERSEAS, NetworkZone.DMZ],
            resources=ResourceSummary(
                total_servers=0, total_vms=0, total_containers=120,
                total_k8s_clusters=2, total_databases=6, total_network_devices=0,
                total_storage_tb=20, total_monthly_cost_yuan=98000,
            ),
            health=EnvironmentHealth(score=93, status="healthy", last_check="刚刚",
                                     cross_region_latency_ms=52.0),
            tags=["production", "cross-border", "compliance", "PIPL"],
        ),
        # 8. 边缘 + 中心云
        Environment(
            env_id="env-edge",
            env_name="边缘计算 + 中心云",
            env_type=EnvironmentType.EDGE,
            description="泸州本地 ARM64 边缘节点(银河麒麟V10) + 华为云中心集群",
            cloud_regions=[
                CloudRegion("cn-north-4", "北京四", CloudProvider.HUAWEI,
                            ["cn-north-4a"], NetworkZone.PRODUCTION),
            ],
            edge_sites=[
                EdgeSite("edge-luzhou-1", "泸州柜员终端", "泸州", "arm64", "Kylin V10", "专线"),
                EdgeSite("edge-luzhou-2", "泸州自助机", "泸州", "x86", "CentOS 7", "VPN"),
                EdgeSite("edge-chengdu-1", "成都分行", "成都", "arm64", "Kylin V10", "专线"),
            ],
            interconnects=[
                {"type": "专线", "bandwidth": "100Mbps", "latency_ms": 5.0,
                 "source": "edge-luzhou-1", "target": "cn-north-4"},
                {"type": "VPN", "bandwidth": "50Mbps", "latency_ms": 8.0,
                 "source": "edge-luzhou-2", "target": "cn-north-4"},
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.EDGE],
            resources=ResourceSummary(
                total_servers=3, total_vms=0, total_containers=45,
                total_k8s_clusters=1, total_databases=3, total_network_devices=6,
                total_storage_tb=5, total_monthly_cost_yuan=28000,
            ),
            health=EnvironmentHealth(score=97, status="healthy", last_check="刚刚", cross_region_latency_ms=5.0),
            tags=["production", "edge", "kylin", "arm64"],
        ),
        # 9. 纯物理机 (传统金融)
        Environment(
            env_id="env-legacy-bank",
            env_name="传统银行核心 - 物理机集群",
            env_type=EnvironmentType.HYBRID_PHYSICAL_CLOUD,
            description="核心账务系统在本地物理机(达梦DM8/TongWeb)，手机银行在华为云",
            cloud_regions=[
                CloudRegion("cn-north-4", "北京四", CloudProvider.HUAWEI,
                            ["cn-north-4a"], NetworkZone.PRODUCTION, 8.0),
            ],
            on_prem_sites=[
                OnPremSite("dc-core", "总行数据中心", "泸州", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
                OnPremSite("dc-dr", "灾备中心", "成都", NetworkZone.PRODUCTION,
                           storage_type="SAN"),
            ],
            interconnects=[
                {"type": "专线", "bandwidth": "2Gbps", "latency_ms": 8.0,
                 "source": "dc-core", "target": "cn-north-4"},
                {"type": "专线", "bandwidth": "1Gbps", "latency_ms": 15.0,
                 "source": "dc-core", "target": "dc-dr"},
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.MANAGEMENT, NetworkZone.DMZ],
            resources=ResourceSummary(
                total_servers=38, total_vms=95, total_containers=60,
                total_k8s_clusters=1, total_databases=25, total_network_devices=28,
                total_storage_tb=350, total_monthly_cost_yuan=0,
            ),
            health=EnvironmentHealth(score=99, status="healthy", last_check="刚刚",
                                     cross_region_latency_ms=8.0),
            tags=["production", "banking", "dm8", "tongweb", "hybrid"],
        ),
        # ── 10. 纯本地容器 (K3s on bare metal) ──
        Environment(
            env_id="env-pure-container",
            env_name="开发容器集群 - K3s",
            env_type=EnvironmentType.PURE_CONTAINER,
            description="本地物理机直接跑 K3s 容器集群,无虚拟化层无云,开发/测试用",
            on_prem_sites=[
                OnPremSite("k3s-cluster", "K3s 集群", "泸州", NetworkZone.DEVELOPMENT,
                           InfraProvider.KVM, storage_type="本地SSD"),
            ],
            network_zones=[NetworkZone.DEVELOPMENT, NetworkZone.STAGING],
            resources=ResourceSummary(
                total_servers=2, total_vms=0, total_containers=48,
                total_k8s_clusters=1, total_databases=2, total_network_devices=0,
                total_storage_tb=2, total_monthly_cost_yuan=0,
            ),
            health=EnvironmentHealth(score=96, status="healthy", last_check="刚刚"),
            tags=["development", "k3s", "container"],
        ),
        # ── 11. 多站点本地 (总行+分行) ──
        Environment(
            env_id="env-multi-site",
            env_name="银行多站点 - 总行+3分行",
            env_type=EnvironmentType.MULTI_SITE_ONPREM,
            description="总行数据中心 + 3个分行本地站点,专线互联,无云",
            on_prem_sites=[
                OnPremSite("dc-hq", "总行数据中心", "泸州", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
                OnPremSite("dc-cd", "成都分行", "成都", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="NAS"),
                OnPremSite("dc-nc", "南充分行", "南充", NetworkZone.DEVELOPMENT,
                           InfraProvider.KVM, storage_type="本地"),
                OnPremSite("dc-yb", "宜宾分行", "宜宾", NetworkZone.DEVELOPMENT,
                           InfraProvider.KVM, storage_type="本地"),
            ],
            interconnects=[
                {"type": "专线", "bandwidth": "2Gbps", "latency_ms": 3.0,
                 "source": "dc-hq", "target": "dc-cd"},
                {"type": "专线", "bandwidth": "500Mbps", "latency_ms": 8.0,
                 "source": "dc-hq", "target": "dc-nc"},
                {"type": "专线", "bandwidth": "500Mbps", "latency_ms": 10.0,
                 "source": "dc-hq", "target": "dc-yb"},
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.DEVELOPMENT, NetworkZone.MANAGEMENT],
            resources=ResourceSummary(
                total_servers=25, total_vms=80, total_containers=0,
                total_k8s_clusters=0, total_databases=12, total_network_devices=20,
                total_storage_tb=120, total_monthly_cost_yuan=0,
            ),
            health=EnvironmentHealth(score=98, status="healthy", last_check="刚刚",
                                     cross_region_latency_ms=10.0),
            tags=["production", "banking", "multi-site", "branch"],
        ),
        # ── 12. 主备/灾备架构 ──
        Environment(
            env_id="env-dr-standby",
            env_name="核心系统 - 同城双活+异地灾备",
            env_type=EnvironmentType.DR_STANDBY,
            description="泸州主中心+成都同城双活+重庆异地灾备,RPO=0/RTO<30min",
            on_prem_sites=[
                OnPremSite("dc-primary", "主中心", "泸州", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
                OnPremSite("dc-secondary", "同城双活中心", "泸州2", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
                OnPremSite("dc-dr", "异地灾备中心", "重庆", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
            ],
            interconnects=[
                {"type": "专线", "bandwidth": "10Gbps", "latency_ms": 1.5,
                 "source": "dc-primary", "target": "dc-secondary"},
                {"type": "专线", "bandwidth": "2Gbps", "latency_ms": 25.0,
                 "source": "dc-primary", "target": "dc-dr"},
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.MANAGEMENT],
            resources=ResourceSummary(
                total_servers=60, total_vms=180, total_containers=0,
                total_k8s_clusters=0, total_databases=20, total_network_devices=35,
                total_storage_tb=500, total_monthly_cost_yuan=0,
            ),
            health=EnvironmentHealth(score=99, status="healthy", last_check="刚刚",
                                     cross_region_latency_ms=25.0),
            tags=["production", "banking", "DR", "RPO=0", "multi-site"],
        ),
        # ── 13. 多活架构 ──
        Environment(
            env_id="env-multi-active",
            env_name="手机银行 - 双活架构",
            env_type=EnvironmentType.MULTI_ACTIVE,
            description="泸州+成都双活中心,同时对外提供服务,流量按地域DNS分流",
            on_prem_sites=[
                OnPremSite("dc-active-1", "泸州主活", "泸州", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
                OnPremSite("dc-active-2", "成都主活", "成都", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
            ],
            interconnects=[
                {"type": "专线", "bandwidth": "10Gbps", "latency_ms": 18.0,
                 "source": "dc-active-1", "target": "dc-active-2"},
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.MANAGEMENT],
            resources=ResourceSummary(
                total_servers=40, total_vms=150, total_containers=80,
                total_k8s_clusters=2, total_databases=16, total_network_devices=25,
                total_storage_tb=200, total_monthly_cost_yuan=0,
            ),
            health=EnvironmentHealth(score=99, status="healthy", last_check="刚刚",
                                     cross_region_latency_ms=18.0),
            tags=["production", "banking", "multi-active", "mobile-banking"],
        ),
        # ── 14. Serverless 纯云 ──
        Environment(
            env_id="env-serverless",
            env_name="营销活动 - Serverless",
            env_type=EnvironmentType.SERVERLESS_CLOUD,
            description="阿里云函数计算+API网关+OSS+表格存储,无服务器架构",
            cloud_regions=[
                CloudRegion("cn-hangzhou", "杭州", CloudProvider.ALIYUN,
                            ["cn-hangzhou-b"], NetworkZone.PRODUCTION),
            ],
            network_zones=[NetworkZone.PRODUCTION],
            resources=ResourceSummary(
                total_servers=0, total_vms=0, total_containers=0,
                total_k8s_clusters=0, total_databases=0, total_network_devices=0,
                total_storage_tb=5, total_monthly_cost_yuan=12000,
            ),
            health=EnvironmentHealth(score=100, status="healthy", last_check="刚刚"),
            tags=["production", "serverless", "aliyun", "cost-effective"],
        ),
        # ── 15. 托管私有云 ──
        Environment(
            env_id="env-hosted-private",
            env_name="政务云 - 华为云Stack",
            env_type=EnvironmentType.HOSTED_PRIVATE,
            description="华为云Stack部署在客户机房,提供类公有云体验的私有云",
            cloud_regions=[
                CloudRegion("hosted-luzhou", "泸州政务云", CloudProvider.HUAWEI,
                            ["zone-a", "zone-b"], NetworkZone.PRODUCTION),
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.MANAGEMENT, NetworkZone.DMZ],
            resources=ResourceSummary(
                total_servers=0, total_vms=200, total_containers=120,
                total_k8s_clusters=2, total_databases=15, total_network_devices=10,
                total_storage_tb=80, total_monthly_cost_yuan=0,
            ),
            health=EnvironmentHealth(score=97, status="healthy", last_check="刚刚"),
            tags=["production", "government", "hosted-private", "huawei-stack"],
        ),
        # ── 16. 弹性云扩展 ──
        Environment(
            env_id="env-burst",
            env_name="月末结算 - 弹性扩展",
            env_type=EnvironmentType.BURST_CLOUD,
            description="本地VMware为主,月末/季末结算高峰时弹性扩展到阿里云",
            cloud_regions=[
                CloudRegion("cn-shanghai", "上海", CloudProvider.ALIYUN,
                            ["cn-shanghai-h"], NetworkZone.PRODUCTION, 15.0),
            ],
            on_prem_sites=[
                OnPremSite("dc-core", "本地核心", "泸州", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
            ],
            interconnects=[
                {"type": "VPN", "bandwidth": "500Mbps", "latency_ms": 15.0,
                 "source": "dc-core", "target": "cn-shanghai"},
            ],
            network_zones=[NetworkZone.PRODUCTION],
            resources=ResourceSummary(
                total_servers=5, total_vms=40, total_containers=30,
                total_k8s_clusters=1, total_databases=6, total_network_devices=4,
                total_storage_tb=30, total_monthly_cost_yuan=35000,
            ),
            health=EnvironmentHealth(score=95, status="healthy", last_check="刚刚",
                                     cross_region_latency_ms=15.0),
            tags=["production", "burst", "cost-optimized"],
        ),
        # ── 17. 边缘+本地+云 三层 ──
        Environment(
            env_id="env-full-edge",
            env_name="智慧银行 - 三层架构",
            env_type=EnvironmentType.FULL_EDGE,
            description="边缘(网点ARM终端)+本地(核心机房VMware)+云(华为云前端)",
            cloud_regions=[
                CloudRegion("cn-north-4", "北京四", CloudProvider.HUAWEI,
                            ["cn-north-4a"], NetworkZone.PRODUCTION, 20.0),
            ],
            on_prem_sites=[
                OnPremSite("dc-core", "核心机房", "泸州", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="SAN"),
            ],
            edge_sites=[
                EdgeSite("edge-lz-branch", "泸州网点", "泸州", "arm64", "Kylin V10", "专线"),
                EdgeSite("edge-cd-branch", "成都网点", "成都", "arm64", "Kylin V10", "专线"),
                EdgeSite("edge-nc-branch", "南充网点", "南充", "x86", "CentOS 7", "VPN"),
            ],
            interconnects=[
                {"type": "专线", "bandwidth": "2Gbps", "latency_ms": 2.0,
                 "source": "dc-core", "target": "cn-north-4"},
                {"type": "专线", "bandwidth": "100Mbps", "latency_ms": 3.0,
                 "source": "edge-lz-branch", "target": "dc-core"},
                {"type": "专线", "bandwidth": "100Mbps", "latency_ms": 18.0,
                 "source": "edge-cd-branch", "target": "dc-core"},
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.EDGE, NetworkZone.DMZ],
            resources=ResourceSummary(
                total_servers=8, total_vms=55, total_containers=90,
                total_k8s_clusters=2, total_databases=8, total_network_devices=15,
                total_storage_tb=60, total_monthly_cost_yuan=38000,
            ),
            health=EnvironmentHealth(score=94, status="healthy", last_check="刚刚",
                                     cross_region_latency_ms=20.0),
            tags=["production", "edge", "hybrid", "banking", "three-tier"],
        ),
        # ── 18. 国产化全栈 ──
        Environment(
            env_id="env-domestic",
            env_name="信创环境 - 全栈国产化",
            env_type=EnvironmentType.DOMESTIC_STACK,
            description="华为云Stack+达梦DM8+麒麟V10+东方通TongWeb,全栈国产替代",
            cloud_regions=[
                CloudRegion("hosted-domestic", "泸州信创云", CloudProvider.HUAWEI,
                            ["zone-a"], NetworkZone.PRODUCTION),
            ],
            on_prem_sites=[
                OnPremSite("dc-domestic", "信创机房", "泸州", NetworkZone.PRODUCTION,
                           InfraProvider.VMWARE, storage_type="达梦DSC"),
            ],
            network_zones=[NetworkZone.PRODUCTION, NetworkZone.MANAGEMENT],
            resources=ResourceSummary(
                total_servers=6, total_vms=30, total_containers=20,
                total_k8s_clusters=1, total_databases=5, total_network_devices=4,
                total_storage_tb=20, total_monthly_cost_yuan=0,
            ),
            health=EnvironmentHealth(score=96, status="healthy", last_check="刚刚"),
            tags=["production", "domestic", "kylin", "dm8", "tongweb", "compliance"],
        ),
    ]


class EnvironmentManager:
    """环境管理器 - 核心组件"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.environments: list[Environment] = []
        self._load()

    def _load(self):
        """加载环境配置"""
        if self.config_path and os.path.exists(self.config_path):
            self._load_from_file(self.config_path)
        else:
            self.environments = _build_demo_environments()

    def _load_from_file(self, path: str):
        """从 YAML 文件加载环境配置"""
        with open(path) as f:
            raw = yaml.safe_load(f) or {}

        envs_raw = raw.get("environments", [])
        self.environments = []
        for env_data in envs_raw:
            env = self._parse_environment(env_data)
            if env:
                self.environments.append(env)

        if not self.environments:
            self.environments = _build_demo_environments()

    def _parse_environment(self, data: dict) -> Optional[Environment]:
        """解析单个环境配置"""
        try:
            env_type = EnvironmentType(data.get("type", "pure_cloud"))
        except ValueError:
            env_type = EnvironmentType.PURE_CLOUD

        # 解析云区域
        cloud_regions = []
        for r in data.get("cloud_regions", []):
            try:
                provider = CloudProvider(r.get("provider", "aliyun"))
            except ValueError:
                provider = CloudProvider.ALIYUN
            try:
                nz = NetworkZone(r.get("network_zone", "production"))
            except ValueError:
                nz = NetworkZone.PRODUCTION
            cloud_regions.append(CloudRegion(
                region_id=r.get("region_id", ""),
                region_name=r.get("region_name", ""),
                provider=provider,
                zones=r.get("zones", []),
                network_zone=nz,
                latency_ms=r.get("latency_ms"),
            ))

        # 解析本地站点
        on_prem_sites = []
        for s in data.get("on_prem_sites", []):
            try:
                ip = InfraProvider(s.get("infra_provider", "vmware"))
            except ValueError:
                ip = InfraProvider.VMWARE
            try:
                nz = NetworkZone(s.get("network_zone", "production"))
            except ValueError:
                nz = NetworkZone.PRODUCTION
            on_prem_sites.append(OnPremSite(
                site_id=s.get("site_id", ""),
                site_name=s.get("site_name", ""),
                location=s.get("location", ""),
                network_zone=nz,
                infra_provider=ip,
                storage_type=s.get("storage_type", "SAN"),
            ))

        # 解析边缘站点
        edge_sites = []
        for e in data.get("edge_sites", []):
            edge_sites.append(EdgeSite(
                site_id=e.get("site_id", ""),
                site_name=e.get("site_name", ""),
                location=e.get("location", ""),
                device_type=e.get("device_type", "arm64"),
                os=e.get("os", ""),
                connectivity=e.get("connectivity", "VPN"),
            ))

        # 解析跨境链路
        cross_border_links = []
        for l in data.get("cross_border_links", []):
            cross_border_links.append(CrossBorderLink(
                link_id=l.get("link_id", ""),
                source_site=l.get("source", ""),
                target_site=l.get("target", ""),
                link_type=l.get("link_type", "VPN"),
                bandwidth=l.get("bandwidth", ""),
                latency_ms=l.get("latency_ms", 0),
                encrypted=l.get("encrypted", True),
                compliance=l.get("compliance", []),
            ))

        # 网络区域
        network_zones = []
        for nz_str in data.get("network_zones", []):
            try:
                network_zones.append(NetworkZone(nz_str))
            except ValueError:
                pass

        # 资源
        res = data.get("resources", {})
        resources = ResourceSummary(
            total_servers=res.get("total_servers", 0),
            total_vms=res.get("total_vms", 0),
            total_containers=res.get("total_containers", 0),
            total_k8s_clusters=res.get("total_k8s_clusters", 0),
            total_databases=res.get("total_databases", 0),
            total_network_devices=res.get("total_network_devices", 0),
            total_storage_tb=res.get("total_storage_tb", 0),
            total_monthly_cost_yuan=res.get("total_monthly_cost_yuan", 0),
        )

        # 健康
        hp = data.get("health", {})
        health = EnvironmentHealth(
            score=hp.get("score", 100),
            status=hp.get("status", "healthy"),
            last_check=hp.get("last_check", ""),
            issues=hp.get("issues", []),
            cross_region_latency_ms=hp.get("cross_region_latency_ms", 0),
        )

        return Environment(
            env_id=data.get("env_id", ""),
            env_name=data.get("env_name", ""),
            env_type=env_type,
            description=data.get("description", ""),
            cloud_regions=cloud_regions,
            on_prem_sites=on_prem_sites,
            edge_sites=edge_sites,
            cross_border_links=cross_border_links,
            network_zones=network_zones,
            interconnects=data.get("interconnects", []),
            resources=resources,
            health=health,
            tags=data.get("tags", []),
            enabled=data.get("enabled", True),
        )

    # ── 查询接口 ──

    def list_environments(self) -> list[dict]:
        """列出所有环境"""
        return [e.to_dict() for e in self.environments if e.enabled]

    def get_environment(self, env_id: str) -> Optional[dict]:
        """获取单个环境详情"""
        for e in self.environments:
            if e.env_id == env_id:
                return e.to_dict()
        return None

    def get_topology_summary(self) -> dict:
        """获取拓扑概览"""
        type_counts = {}
        provider_counts = {}
        total_resources = ResourceSummary()
        total_cost = 0

        for e in self.environments:
            if not e.enabled:
                continue
            t = e.env_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
            for p in e.all_providers:
                provider_counts[p] = provider_counts.get(p, 0) + 1
            total_resources.total_servers += e.resources.total_servers
            total_resources.total_vms += e.resources.total_vms
            total_resources.total_containers += e.resources.total_containers
            total_resources.total_k8s_clusters += e.resources.total_k8s_clusters
            total_resources.total_databases += e.resources.total_databases
            total_resources.total_network_devices += e.resources.total_network_devices
            total_resources.total_storage_tb += e.resources.total_storage_tb
            total_cost += e.resources.total_monthly_cost_yuan

        avg_health = 0
        healthy_envs = [e for e in self.environments if e.enabled]
        if healthy_envs:
            avg_health = round(sum(e.health.score for e in healthy_envs) / len(healthy_envs))

        return {
            "total_environments": len([e for e in self.environments if e.enabled]),
            "type_distribution": type_counts,
            "provider_distribution": provider_counts,
            "resources": {
                "total_servers": total_resources.total_servers,
                "total_vms": total_resources.total_vms,
                "total_containers": total_resources.total_containers,
                "total_k8s_clusters": total_resources.total_k8s_clusters,
                "total_databases": total_resources.total_databases,
                "total_network_devices": total_resources.total_network_devices,
                "total_storage_tb": total_resources.total_storage_tb,
            },
            "total_monthly_cost_yuan": total_cost,
            "avg_health_score": avg_health,
            "cross_region_links": sum(len(e.cross_border_links) + len(e.interconnects) for e in self.environments),
        }

    def get_network_topology(self) -> list[dict]:
        """获取网络拓扑连线 (用于 Dashboard 可视化)"""
        edges = []
        for e in self.environments:
            if not e.enabled:
                continue
            # 云区域之间
            regions = e.cloud_regions
            for i in range(len(regions)):
                for j in range(i + 1, len(regions)):
                    edges.append({
                        "source": f"{regions[i].provider.value}:{regions[i].region_id}",
                        "target": f"{regions[j].provider.value}:{regions[j].region_id}",
                        "label": f"{regions[i].region_name}↔{regions[j].region_name}",
                        "env_id": e.env_id,
                    })
            # 本地 → 云
            for site in e.on_prem_sites:
                for region in e.cloud_regions:
                    edges.append({
                        "source": f"onprem:{site.site_id}",
                        "target": f"{region.provider.value}:{region.region_id}",
                        "label": f"{site.site_name}↔{region.region_name}",
                        "env_id": e.env_id,
                    })
            # 边缘 → 云
            for edge in e.edge_sites:
                if e.cloud_regions:
                    region = e.cloud_regions[0]
                    edges.append({
                        "source": f"edge:{edge.site_id}",
                        "target": f"{region.provider.value}:{region.region_id}",
                        "label": f"{edge.site_name}↔{region.region_name}",
                        "env_id": e.env_id,
                    })
        return edges
