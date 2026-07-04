import { useState, useEffect, useCallback } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { fetchApi, type MulticloudData, demoMulticloud } from '../api';

// ══════════════════════════════════════════
// 类型定义
// ══════════════════════════════════════════

interface CloudRegion {
  region_id: string; region_name: string; provider: string;
  zones: string[]; network_zone: string; latency_ms: number | null;
}
interface OnPremSite {
  site_id: string; site_name: string; location: string;
  infra_provider: string; network_zone: string; storage_type: string;
}
interface EdgeSiteData {
  site_id: string; site_name: string; location: string;
  device_type: string; os: string; connectivity: string;
}
interface CrossBorderLinkData {
  link_id: string; source: string; target: string;
  link_type: string; bandwidth: string; latency_ms: number;
  encrypted: boolean; compliance: string[];
}
interface Environment {
  env_id: string; env_name: string; env_type: string;
  topology_label: string; topology_icon: string; description: string;
  cloud_regions: CloudRegion[]; on_prem_sites: OnPremSite[];
  edge_sites: EdgeSiteData[]; cross_border_links: CrossBorderLinkData[];
  network_zones: string[]; interconnects: any[];
  resources: {
    total_servers: number; total_vms: number; total_containers: number;
    total_k8s_clusters: number; total_databases: number;
    total_network_devices: number; total_storage_tb: number;
    total_monthly_cost_yuan: number;
  };
  health: { score: number; status: string; last_check: string;
    issues: string[]; cross_region_latency_ms: number; };
  all_providers: string[]; all_regions: string[];
  tags: string[]; enabled: boolean;
  source?: 'demo' | 'discovered'; // 标记来源
}

interface DiscoveryResult {
  os: { os_type: string; os_name: string; os_version: string; kernel: string; arch: string; hostname: string; domestic_os?: boolean };
  hardware: { cpu_cores: number; memory_gb: number; disk_gb: number; load_1m: number; is_virtual: boolean; virtual_type: string; arch: string };
  cloud: { is_cloud: boolean; provider: string; region: string; instance_type: string; instance_id: string };
  containers: { docker: boolean; docker_version: string; docker_running: boolean; containerd: boolean; podman: boolean; k3s: boolean };
  kubernetes: { available: boolean; version: string; nodes: number; namespaces: number; pods: number; provider: string };
  middleware: { name: string; version: string; running: boolean }[];
  databases: { name: string; version: string; port: number; running: boolean }[];
  network: { private_ip: string; public_ip: string; dns: string[]; interfaces: { name: string; ip: string }[] };
  services: { systemd_count: number; docker_containers: number; listening_ports: number[] };
  deployment: { docker_compose: boolean; k8s_deployment: boolean; ansible: boolean; terraform: boolean; helm: boolean; gitops: boolean };
  recommended_agents: { name: string; icon: string; reason: string; priority: string; category: string }[];
  inferred_topology: { type: string; label: string; confidence: number };
}

// ══════════════════════════════════════════
// 常量
// ══════════════════════════════════════════

const providerColors: Record<string, { color: string; label: string; icon: string }> = {
  aliyun: { color: '#ff6a00', label: '阿里云', icon: '☁️' },
  huawei: { color: '#cf0a2c', label: '华为云', icon: '☁️' },
  tencent: { color: '#006eff', label: '腾讯云', icon: '☁️' },
  aws: { color: '#ff9900', label: 'AWS', icon: '☁️' },
  azure: { color: '#0078d4', label: 'Azure', icon: '☁️' },
  gcp: { color: '#4285f4', label: 'GCP', icon: '☁️' },
  vmware: { color: '#607078', label: 'VMware', icon: '🖥️' },
  kvm: { color: '#e04e39', label: 'KVM', icon: '🖥️' },
  proxmox: { color: '#e57000', label: 'Proxmox', icon: '🖥️' },
  openstack: { color: '#003d6b', label: 'OpenStack', icon: '🖥️' },
  k3s: { color: '#0ea5e9', label: 'K3s', icon: '🐳' },
};

const healthColors: Record<string, string> = {
  healthy: '#10b981', degraded: '#f59e0b', critical: '#ef4444', offline: '#6b7280',
};

const typeColors: Record<string, string> = {
  pure_cloud: '#3b82f6', pure_on_prem: '#8b5cf6', pure_virtual: '#06b6d4',
  pure_container: '#0ea5e9', multi_site_onprem: '#a855f7',
  dr_standby: '#ef4444', multi_active: '#f97316',
  serverless_cloud: '#8b5cf6', hosted_private: '#cf0a2c',
  hybrid_virtual_cloud: '#10b981', hybrid_physical_cloud: '#14b8a6',
  hybrid_container_cloud: '#06b6d4', burst_cloud: '#f59e0b',
  multi_cloud: '#f97316', hybrid_multi_cloud: '#ef4444',
  cross_border: '#ec4899', edge: '#84cc16', full_edge: '#22c55e',
  domestic_stack: '#dc2626',
};

// ══════════════════════════════════════════
// Demo 数据 — 18种环境拓扑 (不同行业)
// ══════════════════════════════════════════

const demoEnvironments: Environment[] = [
  // ═══ 纯本地 ═══
  { env_id:'env-mfg-onsite', env_name:'汽车制造 - 产线控制系统', env_type:'pure_on_prem', topology_label:'纯本地物理机', topology_icon:'🏢',
    description:'产线MES/SCADA/PLC控制系统,物理机部署,工业网络隔离,不连互联网',
    cloud_regions:[], on_prem_sites:[
      {site_id:'factory-wuhan',site_name:'武汉工厂',location:'武汉',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
      {site_id:'factory-xian',site_name:'西安工厂',location:'西安',infra_provider:'kvm',network_zone:'production',storage_type:'本地SSD'},
    ], edge_sites:[], cross_border_links:[], network_zones:['production'],
    interconnects:[{type:'工业以太网',bandwidth:'万兆',latency_ms:0.5,source:'factory-wuhan',target:'factory-xian'}],
    resources:{total_servers:30,total_vms:45,total_containers:0,total_k8s_clusters:0,total_databases:4,total_network_devices:60,total_storage_tb:80,total_monthly_cost_yuan:0},
    health:{score:98,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:0.5},
    all_providers:['vmware','kvm'], all_regions:['onprem:factory-wuhan','onprem:factory-xian'],
    tags:['manufacturing','mes','scada','air-gapped'], enabled:true, source:'demo' },

  { env_id:'env-hospital', env_name:'三甲医院 - HIS/LIS/PACS', env_type:'pure_on_prem', topology_label:'纯本地物理机', topology_icon:'🏢',
    description:'医院核心信息系统(HIS/LIS/PACS/EMR),等保三级要求,数据不出院',
    cloud_regions:[], on_prem_sites:[
      {site_id:'dc-hospital',site_name:'院内机房',location:'成都',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
    ], edge_sites:[], cross_border_links:[], network_zones:['production','management'],
    interconnects:[],
    resources:{total_servers:12,total_vms:35,total_containers:0,total_k8s_clusters:0,total_databases:8,total_network_devices:8,total_storage_tb:50,total_monthly_cost_yuan:0},
    health:{score:97,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:0},
    all_providers:['vmware'], all_regions:['onprem:dc-hospital'],
    tags:['healthcare','compliance','HIPAA','HIS'], enabled:true, source:'demo' },

  { env_id:'env-university', env_name:'高校超算中心 - VMware集群', env_type:'pure_virtual', topology_label:'纯本地虚拟化', topology_icon:'🖥️',
    description:'高校科研计算平台,VMware+超算节点,跑AI训练和科学计算',
    cloud_regions:[], on_prem_sites:[
      {site_id:'dc-hpc',site_name:'超算中心机房',location:'北京',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
    ], edge_sites:[], cross_border_links:[], network_zones:['production','development'],
    interconnects:[],
    resources:{total_servers:8,total_vms:60,total_containers:15,total_k8s_clusters:1,total_databases:3,total_network_devices:4,total_storage_tb:200,total_monthly_cost_yuan:0},
    health:{score:94,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:0},
    all_providers:['vmware'], all_regions:['onprem:dc-hpc'],
    tags:['education','research','HPC','AI-training'], enabled:true, source:'demo' },

  { env_id:'env-startup-k8s', env_name:'创业公司 - K3s轻量集群', env_type:'pure_container', topology_label:'纯本地容器', topology_icon:'🐳',
    description:'3台物理机跑K3s,无虚拟化无云,本地开发+测试,节省成本',
    cloud_regions:[], on_prem_sites:[
      {site_id:'k3s-cluster',site_name:'K3s集群',location:'深圳',infra_provider:'kvm',network_zone:'development',storage_type:'本地NVMe'},
    ], edge_sites:[], cross_border_links:[], network_zones:['development','staging'],
    interconnects:[], resources:{total_servers:3,total_vms:0,total_containers:52,total_k8s_clusters:1,total_databases:2,total_network_devices:0,total_storage_tb:3,total_monthly_cost_yuan:0},
    health:{score:95,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:0},
    all_providers:['kvm'], all_regions:['onprem:k3s-cluster'],
    tags:['startup','k3s','cost-effective','dev'], enabled:true, source:'demo' },

  // ═══ 纯云 ═══
  { env_id:'env-internet-aliyun', env_name:'电商平台 - 阿里云全托管', env_type:'pure_cloud', topology_label:'纯云部署', topology_icon:'☁️',
    description:'中型电商平台,全面托管在阿里云,ECS+RDS+Redis+OSS+CDN,无自有机房',
    cloud_regions:[
      {region_id:'cn-hangzhou',region_name:'杭州',provider:'aliyun',zones:['cn-hangzhou-b','cn-hangzhou-c'],network_zone:'production',latency_ms:null},
      {region_id:'cn-shanghai',region_name:'上海',provider:'aliyun',zones:['cn-shanghai-a'],network_zone:'production',latency_ms:8.0},
    ], on_prem_sites:[], edge_sites:[], cross_border_links:[], network_zones:['production','staging'],
    interconnects:[], resources:{total_servers:0,total_vms:0,total_containers:420,total_k8s_clusters:3,total_databases:25,total_network_devices:0,total_storage_tb:30,total_monthly_cost_yuan:220000},
    health:{score:96,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:8.0},
    all_providers:['aliyun'], all_regions:['aliyun:cn-hangzhou','aliyun:cn-shanghai'],
    tags:['ecommerce','aliyun','cloud-native','high-traffic'], enabled:true, source:'demo' },

  { env_id:'env-saas-serverless', env_name:'SaaS平台 - Serverless架构', env_type:'serverless_cloud', topology_label:'Serverless', topology_icon:'λ',
    description:'B2B SaaS产品,函数计算+API网关+OSS+表格存储,按量付费,0运维',
    cloud_regions:[
      {region_id:'cn-shanghai',region_name:'上海',provider:'aliyun',zones:['cn-shanghai-a'],network_zone:'production',latency_ms:null},
    ], on_prem_sites:[], edge_sites:[], cross_border_links:[], network_zones:['production'],
    interconnects:[], resources:{total_servers:0,total_vms:0,total_containers:0,total_k8s_clusters:0,total_databases:0,total_network_devices:0,total_storage_tb:8,total_monthly_cost_yuan:15000},
    health:{score:100,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:0},
    all_providers:['aliyun'], all_regions:['aliyun:cn-shanghai'],
    tags:['saas','serverless','startup','cost-optimized'], enabled:true, source:'demo' },

  { env_id:'env-gov-cloud', env_name:'省级政务云 - 华为云Stack', env_type:'hosted_private', topology_label:'托管私有云', topology_icon:'🏰',
    description:'省级政务云平台,华为云Stack部署在电信机房,承载120+政务系统',
    cloud_regions:[
      {region_id:'hosted-gov',region_name:'政务云数据中心',provider:'huawei',zones:['zone-a','zone-b','zone-c'],network_zone:'production',latency_ms:null},
    ], on_prem_sites:[], edge_sites:[], cross_border_links:[], network_zones:['production','management','dmz'],
    interconnects:[], resources:{total_servers:0,total_vms:580,total_containers:200,total_k8s_clusters:4,total_databases:45,total_network_devices:15,total_storage_tb:300,total_monthly_cost_yuan:0},
    health:{score:97,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:0},
    all_providers:['huawei'], all_regions:['huawei:hosted-gov'],
    tags:['government','hosted-private','huawei-stack','multi-tenant'], enabled:true, source:'demo' },

  // ═══ 混合云 ═══
  { env_id:'env-ecommerce-hybrid', env_name:'大型电商 - 本地IDC+阿里云', env_type:'hybrid_virtual_cloud', topology_label:'混合云(虚拟+云)', topology_icon:'🔗',
    description:'核心交易在本地IDC(低延迟),前端/搜索/推荐在阿里云(弹性),专线互联',
    cloud_regions:[
      {region_id:'cn-hangzhou',region_name:'杭州',provider:'aliyun',zones:['cn-hangzhou-b'],network_zone:'production',latency_ms:6.0},
    ], on_prem_sites:[
      {site_id:'idc-main',site_name:'主IDC',location:'杭州',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
    ], edge_sites:[], cross_border_links:[], network_zones:['production','dmz'],
    interconnects:[{type:'专线',bandwidth:'10Gbps',latency_ms:6.0,source:'idc-main',target:'cn-hangzhou'}],
    resources:{total_servers:20,total_vms:150,total_containers:380,total_k8s_clusters:4,total_databases:30,total_network_devices:15,total_storage_tb:120,total_monthly_cost_yuan:350000},
    health:{score:95,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:6.0},
    all_providers:['aliyun','vmware'], all_regions:['aliyun:cn-hangzhou','onprem:idc-main'],
    tags:['ecommerce','hybrid','peak-scaling','double11'], enabled:true, source:'demo' },

  { env_id:'env-auto-hybrid', env_name:'汽车集团 - 产线+华为云', env_type:'hybrid_physical_cloud', topology_label:'混合云(物理+云)', topology_icon:'🔗',
    description:'产线控制系统在本地物理机,研发数据/车联网/OTA在华为云',
    cloud_regions:[
      {region_id:'cn-north-4',region_name:'北京四',provider:'huawei',zones:['cn-north-4a','cn-north-4b'],network_zone:'production',latency_ms:12.0},
    ], on_prem_sites:[
      {site_id:'factory-wuhan',site_name:'武汉工厂',location:'武汉',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
    ], edge_sites:[], cross_border_links:[], network_zones:['production','management'],
    interconnects:[{type:'专线',bandwidth:'2Gbps',latency_ms:12.0,source:'factory-wuhan',target:'cn-north-4'}],
    resources:{total_servers:25,total_vms:40,total_containers:60,total_k8s_clusters:1,total_databases:8,total_network_devices:30,total_storage_tb:100,total_monthly_cost_yuan:68000},
    health:{score:96,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:12.0},
    all_providers:['huawei','vmware'], all_regions:['huawei:cn-north-4','onprem:factory-wuhan'],
    tags:['manufacturing','automotive','industry4.0','iot'], enabled:true, source:'demo' },

  { env_id:'env-retail-hybrid', env_name:'连锁零售 - SAP+腾讯云', env_type:'hybrid_container_cloud', topology_label:'混合云(容器+云)', topology_icon:'🔗',
    description:'本地SAP ERP(核心库存/财务),门店系统+小程序+会员在腾讯云',
    cloud_regions:[
      {region_id:'ap-guangzhou',region_name:'广州',provider:'tencent',zones:['ap-guangzhou-2'],network_zone:'production',latency_ms:10.0},
    ], on_prem_sites:[
      {site_id:'dc-hq',site_name:'总部机房',location:'上海',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
    ], edge_sites:[], cross_border_links:[], network_zones:['production','dmz'],
    interconnects:[{type:'专线',bandwidth:'1Gbps',latency_ms:10.0,source:'dc-hq',target:'ap-guangzhou'}],
    resources:{total_servers:6,total_vms:30,total_containers:180,total_k8s_clusters:2,total_databases:12,total_network_devices:8,total_storage_tb:40,total_monthly_cost_yuan:85000},
    health:{score:94,status:'degraded',last_check:'刚刚',issues:['门店小程序偶尔超时'],cross_region_latency_ms:10.0},
    all_providers:['tencent','vmware'], all_regions:['tencent:ap-guangzhou','onprem:dc-hq'],
    tags:['retail','sap','tencent','omnichannel'], enabled:true, source:'demo' },

  // ═══ 多云 ═══
  { env_id:'env-multinational', env_name:'跨国企业 - 全球三云架构', env_type:'multi_cloud', topology_label:'多云部署', topology_icon:'🌐',
    description:'国内阿里云,海外AWS,Azure做容灾,三云统一管控平台',
    cloud_regions:[
      {region_id:'cn-hangzhou',region_name:'杭州',provider:'aliyun',zones:['cn-hangzhou-b'],network_zone:'production',latency_ms:null},
      {region_id:'us-east-1',region_name:'弗吉尼亚',provider:'aws',zones:['us-east-1a'],network_zone:'overseas',latency_ms:180.0},
      {region_id:'westeurope',region_name:'荷兰',provider:'azure',zones:['westeurope-1'],network_zone:'overseas',latency_ms:200.0},
    ], on_prem_sites:[], edge_sites:[], cross_border_links:[], network_zones:['production','overseas'],
    interconnects:[{type:'VPN',bandwidth:'200Mbps',latency_ms:180.0,source:'cn-hangzhou',target:'us-east-1'},{type:'VPN',bandwidth:'100Mbps',latency_ms:200.0,source:'cn-hangzhou',target:'westeurope'}],
    resources:{total_servers:0,total_vms:0,total_containers:500,total_k8s_clusters:8,total_databases:35,total_network_devices:0,total_storage_tb:80,total_monthly_cost_yuan:520000},
    health:{score:92,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:200.0},
    all_providers:['aliyun','aws','azure'], all_regions:['aliyun:cn-hangzhou','aws:us-east-1','azure:westeurope'],
    tags:['multinational','multi-cloud','global','compliance'], enabled:true, source:'demo' },

  { env_id:'env-game-dual', env_name:'游戏公司 - 腾讯云+阿里云', env_type:'multi_cloud', topology_label:'多云部署', topology_icon:'🌐',
    description:'游戏运行在腾讯云(CDK/GSE),官网/支付/数据分析在阿里云,双云灾备',
    cloud_regions:[
      {region_id:'ap-guangzhou',region_name:'广州',provider:'tencent',zones:['ap-guangzhou-2'],network_zone:'production',latency_ms:null},
      {region_id:'cn-hangzhou',region_name:'杭州',provider:'aliyun',zones:['cn-hangzhou-b'],network_zone:'production',latency_ms:25.0},
    ], on_prem_sites:[], edge_sites:[], cross_border_links:[], network_zones:['production','staging'],
    interconnects:[{type:'VPN',bandwidth:'500Mbps',latency_ms:25.0,source:'ap-guangzhou',target:'cn-hangzhou'}],
    resources:{total_servers:0,total_vms:0,total_containers:250,total_k8s_clusters:4,total_databases:15,total_network_devices:0,total_storage_tb:50,total_monthly_cost_yuan:280000},
    health:{score:95,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:25.0},
    all_providers:['tencent','aliyun'], all_regions:['tencent:ap-guangzhou','aliyun:cn-hangzhou'],
    tags:['gaming','multi-cloud','peak-scaling','low-latency'], enabled:true, source:'demo' },

  // ═══ 灾备/多活 ═══
  { env_id:'env-securities-dual', env_name:'证券公司 - 同城双活', env_type:'multi_active', topology_label:'多活架构', topology_icon:'⚡',
    description:'交易系统同城双活(上海浦东+张江),RPO=0,切换时间<10s',
    cloud_regions:[], on_prem_sites:[
      {site_id:'dc-pudong',site_name:'浦东数据中心',location:'上海浦东',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
      {site_id:'dc-zhangjiang',site_name:'张江灾备中心',location:'上海张江',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
    ], edge_sites:[], cross_border_links:[], network_zones:['production','management'],
    interconnects:[{type:'专线',bandwidth:'40Gbps',latency_ms:1.2,source:'dc-pudong',target:'dc-zhangjiang'}],
    resources:{total_servers:50,total_vms:200,total_containers:60,total_k8s_clusters:1,total_databases:22,total_network_devices:30,total_storage_tb:300,total_monthly_cost_yuan:0},
    health:{score:99,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:1.2},
    all_providers:['vmware'], all_regions:['onprem:dc-pudong','onprem:dc-zhangjiang'],
    tags:['securities','trading','dual-active','low-latency'], enabled:true, source:'demo' },

  { env_id:'env-insurance-dr', env_name:'保险集团 - 双活+异地灾备', env_type:'dr_standby', topology_label:'主备/灾备', topology_icon:'🔄',
    description:'北京主中心+同城双活+贵阳异地灾备,RPO=0,RTO<15min',
    cloud_regions:[], on_prem_sites:[
      {site_id:'dc-primary',site_name:'北京主中心',location:'北京',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
      {site_id:'dc-secondary',site_name:'同城双活',location:'北京亦庄',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
      {site_id:'dc-dr',site_name:'异地灾备',location:'贵阳',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
    ], edge_sites:[], cross_border_links:[], network_zones:['production','management'],
    interconnects:[{type:'专线',bandwidth:'20Gbps',latency_ms:1.5,source:'dc-primary',target:'dc-secondary'},{type:'专线',bandwidth:'2Gbps',latency_ms:35.0,source:'dc-primary',target:'dc-dr'}],
    resources:{total_servers:55,total_vms:180,total_containers:0,total_k8s_clusters:0,total_databases:18,total_network_devices:28,total_storage_tb:400,total_monthly_cost_yuan:0},
    health:{score:99,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:35.0},
    all_providers:['vmware'], all_regions:['onprem:dc-primary','onprem:dc-secondary','onprem:dc-dr'],
    tags:['insurance','disaster-recovery','compliance','银保监'], enabled:true, source:'demo' },

  // ═══ 边缘 ═══
  { env_id:'env-smart-mfg', env_name:'智能制造 - 边缘产线+云端AI', env_type:'edge', topology_label:'边缘+中心云', topology_icon:'📡',
    description:'工厂边缘节点实时质检(ARM+GPU),分析结果上传阿里云训练模型',
    cloud_regions:[
      {region_id:'cn-shanghai',region_name:'上海',provider:'aliyun',zones:['cn-shanghai-a'],network_zone:'production',latency_ms:8.0},
    ], on_prem_sites:[], edge_sites:[
      {site_id:'edge-line-1',site_name:'产线1-视觉检测',location:'苏州',device_type:'gpu',os:'Ubuntu 22.04',connectivity:'专线'},
      {site_id:'edge-line-2',site_name:'产线2-振动监测',location:'苏州',device_type:'arm64',os:'RT-Linux',connectivity:'专线'},
      {site_id:'edge-line-3',site_name:'产线3-能耗采集',location:'苏州',device_type:'arm64',os:'FreeRTOS',connectivity:'4G'},
    ], cross_border_links:[], network_zones:['production','edge'],
    interconnects:[{type:'专线',bandwidth:'200Mbps',latency_ms:8.0,source:'edge-line-1',target:'cn-shanghai'}],
    resources:{total_servers:0,total_vms:0,total_containers:15,total_k8s_clusters:1,total_databases:2,total_network_devices:20,total_storage_tb:8,total_monthly_cost_yuan:45000},
    health:{score:93,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:8.0},
    all_providers:['aliyun'], all_regions:['aliyun:cn-shanghai','onprem:edge-line-1','onprem:edge-line-2'],
    tags:['manufacturing','edge-ai','quality-inspection','iot'], enabled:true, source:'demo' },

  { env_id:'env-smart-city', env_name:'智慧城市 - 三层架构', env_type:'full_edge', topology_label:'边缘+本地+云', topology_icon:'📡',
    description:'路口摄像头边缘计算(华为Atlas)+本地数据中心(视频存储)+华为云(AI分析)',
    cloud_regions:[
      {region_id:'cn-north-4',region_name:'北京四',provider:'huawei',zones:['cn-north-4a'],network_zone:'production',latency_ms:15.0},
    ], on_prem_sites:[
      {site_id:'dc-city',site_name:'市级数据中心',location:'成都',infra_provider:'vmware',network_zone:'production',storage_type:'SAN'},
    ], edge_sites:[
      {site_id:'edge-intersection-01',site_name:'天府路口',location:'成都天府新区',device_type:'gpu',os:'Ubuntu+Atlas',connectivity:'专线'},
      {site_id:'edge-intersection-02',site_name:'春熙路口',location:'成都锦江区',device_type:'gpu',os:'Ubuntu+Atlas',connectivity:'专线'},
      {site_id:'edge-camera-farm',site_name:'郊县摄像头群',location:'成都郊区',device_type:'arm64',os:'HiLinux',connectivity:'4G/5G'},
    ], cross_border_links:[], network_zones:['production','edge','dmz'],
    interconnects:[{type:'专线',bandwidth:'1Gbps',latency_ms:2.0,source:'dc-city',target:'cn-north-4'},{type:'专线',bandwidth:'500Mbps',latency_ms:3.0,source:'edge-intersection-01',target:'dc-city'}],
    resources:{total_servers:5,total_vms:40,total_containers:30,total_k8s_clusters:1,total_databases:6,total_network_devices:50,total_storage_tb:80,total_monthly_cost_yuan:55000},
    health:{score:91,status:'degraded',last_check:'刚刚',issues:['郊县4G链路偶发丢包'],cross_region_latency_ms:15.0},
    all_providers:['huawei','vmware'], all_regions:['huawei:cn-north-4','onprem:dc-city','onprem:edge-intersection-01'],
    tags:['smart-city','edge-ai','surveillance','public-safety'], enabled:true, source:'demo' },

  // ═══ 国产化 ═══
  { env_id:'env-soe-domestic', env_name:'央企集团 - 信创全栈替代', env_type:'domestic_stack', topology_label:'国产化全栈', topology_icon:'🇨🇳',
    description:'华为云Stack+达梦DM8+麒麟V10+东方通TongWeb+金山办公,全栈国产替代',
    cloud_regions:[
      {region_id:'hosted-soe',region_name:'央企信创云',provider:'huawei',zones:['zone-a','zone-b'],network_zone:'production',latency_ms:null},
    ], on_prem_sites:[
      {site_id:'dc-soe',site_name:'集团总部机房',location:'北京',infra_provider:'vmware',network_zone:'production',storage_type:'达梦DSC'},
    ], edge_sites:[], cross_border_links:[], network_zones:['production','management'],
    interconnects:[], resources:{total_servers:10,total_vms:80,total_containers:50,total_k8s_clusters:1,total_databases:12,total_network_devices:8,total_storage_tb:60,total_monthly_cost_yuan:0},
    health:{score:96,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:0},
    all_providers:['huawei','vmware'], all_regions:['huawei:hosted-soe','onprem:dc-soe'],
    tags:['soe','domestic','kylin','dm8','tongweb','compliance'], enabled:true, source:'demo' },

  // ═══ 跨境 ═══
  { env_id:'env-crossborder-ecom', env_name:'跨境电商 - 境内+境外多云', env_type:'cross_border', topology_label:'跨境部署', topology_icon:'🌍',
    description:'国内阿里云(仓储/财务)+AWS新加坡(东南亚商城)+AWS美西(独立站),PIPL+GDPR合规',
    cloud_regions:[
      {region_id:'cn-shenzhen',region_name:'深圳',provider:'aliyun',zones:['cn-shenzhen-a'],network_zone:'production',latency_ms:null},
      {region_id:'ap-southeast-1',region_name:'新加坡',provider:'aws',zones:['ap-southeast-1a'],network_zone:'overseas',latency_ms:55.0},
      {region_id:'us-west-2',region_name:'俄勒冈',provider:'aws',zones:['us-west-2a'],network_zone:'overseas',latency_ms:160.0},
    ], on_prem_sites:[], edge_sites:[], cross_border_links:[
      {link_id:'link-sg',source:'cn-shenzhen',target:'ap-southeast-1',link_type:'IPSec VPN',bandwidth:'200Mbps',latency_ms:55.0,encrypted:true,compliance:['PIPL','PDPA']},
      {link_id:'link-us',source:'ap-southeast-1',target:'us-west-2',link_type:'AWS内部',bandwidth:'1Gbps',latency_ms:120.0,encrypted:true,compliance:['GDPR']},
    ], network_zones:['production','overseas','dmz'],
    interconnects:[{type:'IPSec VPN',bandwidth:'200Mbps',latency_ms:55.0,source:'cn-shenzhen',target:'ap-southeast-1'}],
    resources:{total_servers:0,total_vms:0,total_containers:180,total_k8s_clusters:4,total_databases:12,total_network_devices:0,total_storage_tb:25,total_monthly_cost_yuan:165000},
    health:{score:93,status:'healthy',last_check:'刚刚',issues:[],cross_region_latency_ms:160.0},
    all_providers:['aliyun','aws'], all_regions:['aliyun:cn-shenzhen','aws:ap-southeast-1','aws:us-west-2'],
    tags:['cross-border','ecommerce','compliance','PIPL','GDPR'], enabled:true, source:'demo' },
];

// ══════════════════════════════════════════
// Discovery Demo 数据
// ══════════════════════════════════════════

const demoDiscovery: DiscoveryResult = {
  os: { os_type: 'linux', os_name: '银河麒麟 V10', os_version: 'V10-SP2', kernel: '4.19.91-24.9.el7.ky10.aarch64', arch: 'aarch64', hostname: 'mes-db01', domestic_os: true },
  hardware: { cpu_cores: 8, memory_gb: 32, disk_gb: 500, load_1m: 1.2, is_virtual: false, virtual_type: '', arch: 'aarch64' },
  cloud: { is_cloud: false, provider: '', region: '', instance_type: '', instance_id: '' },
  containers: { docker: true, docker_version: '24.0.7', docker_running: true, containerd: true, podman: false, k3s: false },
  kubernetes: { available: false, version: '', nodes: 0, namespaces: 0, pods: 0, provider: '' },
  middleware: [
    { name: 'Nginx', version: 'nginx/1.29.0', running: true },
    { name: 'Redis', version: 'redis-cli 7.2.14', running: true },
    { name: 'RabbitMQ', version: 'RabbitMQ 5.4.0', running: true },
    { name: 'TongWeb', version: 'TongWeb 7.0', running: true },
  ],
  databases: [
    { name: '达梦DM8', version: 'DM Database Server 64 V8.1.3.100', port: 5236, running: true },
    { name: 'Redis', version: 'redis-cli 7.2.14', port: 6379, running: true },
  ],
  network: { private_ip: '192.168.10.22', public_ip: '', dns: ['114.114.114.114', '223.5.5.5'], interfaces: [{ name: 'eth0', ip: '192.168.10.22/24' }, { name: 'docker0', ip: '172.17.0.1/16' }] },
  services: { systemd_count: 156, docker_containers: 8, listening_ports: [22, 80, 443, 3306, 5236, 6379, 5672, 8080, 8801, 9060] },
  deployment: { docker_compose: true, k8s_deployment: false, ansible: false, terraform: false, helm: false, gitops: false },
  recommended_agents: [
    { name: 'linux', icon: '🐧', reason: '系统基础监控与诊断', priority: 'high', category: '基础' },
    { name: 'docker', icon: '🐳', reason: '检测到 Docker 24.0.7 运行时', priority: 'high', category: '容器' },
    { name: 'db', icon: '🗄️', reason: '检测到数据库: 达梦DM8, Redis', priority: 'high', category: '数据' },
    { name: 'middleware', icon: '📦', reason: '检测到中间件: Nginx, Redis, RabbitMQ, TongWeb', priority: 'high', category: '中间件' },
    { name: 'security', icon: '🔒', reason: '安全扫描与合规检查', priority: 'medium', category: '安全' },
    { name: 'monitor', icon: '📊', reason: '系统监控与告警', priority: 'high', category: '监控' },
    { name: 'sre', icon: '🏥', reason: 'SLI/SLO 管理', priority: 'medium', category: '运维' },
    { name: 'incident', icon: '🚨', reason: '故障应急响应', priority: 'medium', category: '运维' },
    { name: 'planner', icon: '📋', reason: '任务编排调度', priority: 'high', category: '核心' },
    { name: 'copilot', icon: '🤖', reason: 'AI 对话助手', priority: 'medium', category: '核心' },
  ],
  inferred_topology: { type: 'pure_on_prem', label: '🏢 本地物理机 (国产化)', confidence: 85 },
};

// ══════════════════════════════════════════
// 子组件
// ══════════════════════════════════════════

// ── 探测卡片 ──
function DetectionCard({ title, icon, items, color }: { title: string; icon: string; items: { label: string; value: string | number | boolean; highlight?: boolean }[]; color: string }) {
  return (
    <div className="card" style={{ padding: '14px 16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
        <span style={{ fontSize: 18 }}>{icon}</span>
        <span style={{ fontWeight: 600, fontSize: 13 }}>{title}</span>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '6px 16px' }}>
        {items.map((item, i) => (
          <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11 }}>
            <span style={{ color: 'var(--text-muted)' }}>{item.label}</span>
            <span style={{ color: item.highlight ? color : 'var(--text-secondary)', fontWeight: item.highlight ? 600 : 400 }}>
              {typeof item.value === 'boolean' ? (item.value ? '✅' : '❌') : item.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── 统计卡片 ──
function SummaryStats({ envs }: { envs: Environment[] }) {
  const totalProviders = new Set(envs.flatMap(e => e.all_providers)).size;
  const totalVMs = envs.reduce((s, e) => s + e.resources.total_vms, 0);
  const totalContainers = envs.reduce((s, e) => s + e.resources.total_containers, 0);
  const totalCost = envs.reduce((s, e) => s + e.resources.total_monthly_cost_yuan, 0);
  const avgHealth = envs.length ? Math.round(envs.reduce((s, e) => s + e.health.score, 0) / envs.length) : 0;
  const discovered = envs.filter(e => e.source === 'discovered').length;

  const stats = [
    { label: '环境总数', value: envs.length, icon: '🏗️', color: '#3b82f6' },
    { label: '已发现', value: discovered, icon: '🔍', color: '#10b981' },
    { label: '基础设施', value: totalProviders, icon: '☁️', color: '#8b5cf6' },
    { label: '虚拟机', value: totalVMs, icon: '🖥️', color: '#06b6d4' },
    { label: '容器', value: totalContainers, icon: '🐳', color: '#10b981' },
    { label: '月度总成本', value: `¥${(totalCost / 10000).toFixed(1)}万`, icon: '💰', color: '#f97316' },
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 10, marginBottom: 20 }}>
      {stats.map(s => (
        <div key={s.label} className="card" style={{ padding: '12px 14px', textAlign: 'center' }}>
          <div style={{ fontSize: 18, marginBottom: 2 }}>{s.icon}</div>
          <div style={{ fontSize: 20, fontWeight: 700, color: s.color }}>{s.value}</div>
          <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 2 }}>{s.label}</div>
        </div>
      ))}
    </div>
  );
}

// ── 拓扑可视化 ──
function TopologyDiagram({ env }: { env: Environment }) {
  const nodes: { id: string; label: string; type: string; color: string; x: number; y: number }[] = [];
  let xOff = 0;

  env.on_prem_sites.forEach((s) => {
    const p = providerColors[s.infra_provider] || { color: '#6b7280', label: s.infra_provider, icon: '🏢' };
    nodes.push({ id: s.site_id, label: s.site_name, type: 'onprem', color: p.color, x: xOff, y: 0 });
    xOff += 1;
  });
  env.edge_sites.forEach((s) => {
    nodes.push({ id: s.site_id, label: s.site_name, type: 'edge', color: '#84cc16', x: xOff, y: 0 });
    xOff += 1;
  });
  env.cloud_regions.forEach((r) => {
    const p = providerColors[r.provider] || { color: '#6b7280', label: r.provider, icon: '☁️' };
    nodes.push({ id: `${r.provider}:${r.region_id}`, label: r.region_name, type: 'cloud',
      color: p.color, x: xOff, y: r.network_zone === 'overseas' ? 1 : 0 });
    xOff += 1;
  });

  const totalWidth = Math.max(xOff, 3) * 130;

  return (
    <div style={{ position: 'relative', height: 120, width: '100%', overflow: 'hidden' }}>
      <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
        {env.interconnects.map((ic) => {
          const src = nodes.find(n => n.id === ic.source || n.label.includes(ic.source));
          const tgt = nodes.find(n => n.id === ic.target || n.label.includes(ic.target));
          if (!src || !tgt) return null;
          const sx = (src.x / Math.max(xOff, 1)) * totalWidth + 50;
          const sy = 35 + src.y * 45;
          const tx = (tgt.x / Math.max(xOff, 1)) * totalWidth + 50;
          const ty = 35 + tgt.y * 45;
          return (
            <g key={ic.source + ic.target}>
              <line x1={sx} y1={sy} x2={tx} y2={ty} stroke="rgba(59,130,246,0.3)" strokeWidth="2" strokeDasharray="6,4" />
              <text x={(sx+tx)/2} y={(sy+ty)/2 - 4} textAnchor="middle" fill="var(--text-muted)" fontSize="8">
                {ic.type} {ic.latency_ms}ms
              </text>
            </g>
          );
        })}
      </svg>
      {nodes.map((n) => {
        const left = (n.x / Math.max(xOff, 1)) * totalWidth;
        const top = 25 + n.y * 50;
        const isCloud = n.type === 'cloud';
        const isEdge = n.type === 'edge';
        return (
          <div key={n.id} style={{
            position: 'absolute', left, top,
            width: 100, padding: '8px 6px', borderRadius: 8, textAlign: 'center',
            background: `${n.color}15`, border: `1.5px solid ${n.color}40`,
          }}>
            <div style={{ fontSize: 16 }}>{isCloud ? '☁️' : isEdge ? '📡' : '🏢'}</div>
            <div style={{ fontSize: 10, fontWeight: 600, color: n.color, marginTop: 2 }}>{n.label}</div>
          </div>
        );
      })}
    </div>
  );
}

// ── 环境卡片 ──
function EnvironmentCard({ env, onRemove }: { env: Environment; onRemove?: (id: string) => void }) {
  const [expanded, setExpanded] = useState(false);
  const tc = typeColors[env.env_type] || '#6b7280';
  const hc = healthColors[env.health.status] || '#6b7280';
  const isDiscovered = env.source === 'discovered';

  return (
    <div className="card" style={{ overflow: 'hidden', transition: 'all 0.2s', border: isDiscovered ? '1px solid rgba(16,185,129,0.3)' : undefined }}>
      <div onClick={() => setExpanded(!expanded)} style={{ cursor: 'pointer', padding: '14px 18px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, minWidth: 0 }}>
            <span style={{ fontSize: 22 }}>{env.topology_icon}</span>
            <div>
              <div style={{ fontSize: 14, fontWeight: 600, display: 'flex', alignItems: 'center', gap: 8 }}>
                {env.env_name}
                {isDiscovered && <span style={{ fontSize: 9, padding: '1px 6px', borderRadius: 4, background: 'rgba(16,185,129,0.15)', color: '#10b981' }}>🔍 已发现</span>}
              </div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 1 }}>{env.description}</div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
            <span className="badge" style={{ fontSize: 10, padding: '2px 8px', background: `${tc}20`, color: tc }}>
              {env.topology_label}
            </span>
            <span className="badge" style={{ fontSize: 10, padding: '2px 8px', background: `${hc}20`, color: hc }}>
              {env.health.status === 'healthy' ? '✅' : env.health.status === 'degraded' ? '⚠️' : '❌'} {env.health.score}%
            </span>
            <span style={{ fontSize: 12, color: 'var(--text-muted)', transform: expanded ? 'rotate(180deg)' : 'rotate(0)', transition: '0.2s' }}>▼</span>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 6, marginTop: 8, flexWrap: 'wrap' }}>
          {env.all_providers.map(p => {
            const pc = providerColors[p] || { color: '#6b7280', label: p, icon: '❓' };
            return (
              <span key={p} style={{ fontSize: 10, padding: '2px 8px', borderRadius: 10, background: `${pc.color}15`, color: pc.color, border: `1px solid ${pc.color}30` }}>
                {pc.icon} {pc.label}
              </span>
            );
          })}
          {env.all_regions.map(r => (
            <span key={r} style={{ fontSize: 9, padding: '1px 6px', borderRadius: 8, background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
              {r}
            </span>
          ))}
        </div>

        <div style={{ display: 'flex', gap: 16, marginTop: 10, fontSize: 11, color: 'var(--text-secondary)', flexWrap: 'wrap' }}>
          {env.resources.total_servers > 0 && <span>🖥️ {env.resources.total_servers} 服务器</span>}
          {env.resources.total_vms > 0 && <span>💻 {env.resources.total_vms} 虚拟机</span>}
          {env.resources.total_containers > 0 && <span>🐳 {env.resources.total_containers} 容器</span>}
          {env.resources.total_k8s_clusters > 0 && <span>☸️ {env.resources.total_k8s_clusters} K8s</span>}
          {env.resources.total_databases > 0 && <span>🗄️ {env.resources.total_databases} 数据库</span>}
          {env.resources.total_storage_tb > 0 && <span>💾 {env.resources.total_storage_tb}TB</span>}
          {env.resources.total_monthly_cost_yuan > 0 && <span>💰 ¥{(env.resources.total_monthly_cost_yuan/10000).toFixed(1)}万/月</span>}
        </div>
      </div>

      {expanded && (
        <div style={{ padding: '0 18px 18px', borderTop: '1px solid var(--border)' }}>
          <div style={{ marginTop: 14 }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 8 }}>🗺️ 网络拓扑</div>
            <TopologyDiagram env={env} />
          </div>

          {env.cloud_regions.length > 0 && (
            <div style={{ marginTop: 12 }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>☁️ 云区域</div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 8 }}>
                {env.cloud_regions.map(r => {
                  const pc = providerColors[r.provider] || { color: '#6b7280', label: r.provider };
                  return (
                    <div key={r.region_id} style={{ padding: '8px 10px', borderRadius: 6, fontSize: 11, background: `${pc.color}08`, border: `1px solid ${pc.color}25` }}>
                      <div style={{ fontWeight: 600, color: pc.color }}>{pc.label} · {r.region_name}</div>
                      <div style={{ color: 'var(--text-muted)', marginTop: 2, fontFamily: 'monospace' }}>{r.region_id}</div>
                      {r.zones.length > 0 && <div style={{ color: 'var(--text-muted)', marginTop: 1 }}>可用区: {r.zones.join(', ')}</div>}
                      {r.latency_ms !== null && <div style={{ color: r.latency_ms > 100 ? '#ef4444' : '#10b981', marginTop: 1 }}>延迟: {r.latency_ms}ms</div>}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {env.on_prem_sites.length > 0 && (
            <div style={{ marginTop: 12 }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>🏢 本地站点</div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 8 }}>
                {env.on_prem_sites.map(s => {
                  const pc = providerColors[s.infra_provider] || { color: '#6b7280', label: s.infra_provider };
                  return (
                    <div key={s.site_id} style={{ padding: '8px 10px', borderRadius: 6, fontSize: 11, background: `${pc.color}08`, border: `1px solid ${pc.color}25` }}>
                      <div style={{ fontWeight: 600, color: pc.color }}>{s.site_name}</div>
                      <div style={{ color: 'var(--text-muted)', marginTop: 2 }}>📍 {s.location} · {pc.label}</div>
                      <div style={{ color: 'var(--text-muted)' }}>💾 {s.storage_type}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {env.edge_sites.length > 0 && (
            <div style={{ marginTop: 12 }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>📡 边缘节点</div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 8 }}>
                {env.edge_sites.map(e => (
                  <div key={e.site_id} style={{ padding: '8px 10px', borderRadius: 6, fontSize: 11, background: 'rgba(132,204,22,0.08)', border: '1px solid rgba(132,204,22,0.25)' }}>
                    <div style={{ fontWeight: 600, color: '#84cc16' }}>📡 {e.site_name}</div>
                    <div style={{ color: 'var(--text-muted)', marginTop: 2 }}>📍 {e.location} · {e.os}</div>
                    <div style={{ color: 'var(--text-muted)' }}>🔌 {e.connectivity} · {e.device_type}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {env.cross_border_links.length > 0 && (
            <div style={{ marginTop: 12 }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>🌍 跨境链路</div>
              {env.cross_border_links.map(l => (
                <div key={l.link_id} style={{ padding: '8px 12px', borderRadius: 6, fontSize: 11, background: 'rgba(236,72,153,0.08)', border: '1px solid rgba(236,72,153,0.25)', display: 'flex', gap: 16, alignItems: 'center' }}>
                  <span style={{ color: '#ec4899', fontWeight: 600 }}>{l.source} → {l.target}</span>
                  <span style={{ color: 'var(--text-muted)' }}>{l.link_type} · {l.bandwidth} · {l.latency_ms}ms</span>
                  <span style={{ color: l.encrypted ? '#10b981' : '#ef4444' }}>{l.encrypted ? '🔒 加密' : '⚠️ 未加密'}</span>
                  {l.compliance.length > 0 && <span style={{ color: '#8b5cf6' }}>📋 {l.compliance.join(' / ')}</span>}
                </div>
              ))}
            </div>
          )}

          {env.interconnects.length > 0 && (
            <div style={{ marginTop: 12 }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>🔗 互联链路</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                {env.interconnects.map((ic: any) => (
                  <div key={ic.source + ic.target} style={{ padding: '5px 10px', borderRadius: 4, fontSize: 11, background: 'rgba(59,130,246,0.06)', border: '1px solid rgba(59,130,246,0.12)', display: 'flex', gap: 12, fontFamily: 'monospace' }}>
                    <span style={{ color: '#93c5fd' }}>{ic.source} ↔ {ic.target}</span>
                    <span style={{ color: 'var(--text-muted)' }}>{ic.type} · {ic.bandwidth}</span>
                    <span style={{ color: ic.latency_ms > 50 ? '#ef4444' : '#10b981' }}>{ic.latency_ms}ms</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {env.health.issues.length > 0 && (
            <div style={{ marginTop: 12, padding: '8px 12px', borderRadius: 6, background: 'rgba(245,158,11,0.08)', border: '1px solid rgba(245,158,11,0.25)' }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: '#f59e0b', marginBottom: 4 }}>⚠️ 健康问题</div>
              {env.health.issues.map((issue) => (
                <div key={issue} style={{ fontSize: 11, color: 'var(--text-secondary)' }}>• {issue}</div>
              ))}
            </div>
          )}

          <div style={{ display: 'flex', gap: 4, marginTop: 12, flexWrap: 'wrap' }}>
            {env.tags.map(t => (
              <span key={t} style={{ fontSize: 9, padding: '1px 6px', borderRadius: 4, background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)' }}>
                #{t}
              </span>
            ))}
          </div>

          {/* 删除按钮 - 仅已发现的环境 */}
          {isDiscovered && onRemove && (
            <div style={{ marginTop: 10, textAlign: 'right' }}>
              <button onClick={(e) => { e.stopPropagation(); onRemove(env.env_id); }} style={{
                padding: '4px 12px', borderRadius: 6, border: '1px solid rgba(239,68,68,0.3)',
                background: 'rgba(239,68,68,0.08)', color: '#ef4444', cursor: 'pointer', fontSize: 11,
              }}>
                🗑️ 移除
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ══════════════════════════════════════════
// 主页面 — 发现 + 管理 一体化
// ══════════════════════════════════════════

export default function EnvironmentPage() {
  const [tab, setTab] = useState<'discover' | 'manage' | 'multicloud'>('discover');
  const [environments, setEnvironments] = useState<Environment[]>(demoEnvironments);
  const [activeType, setActiveType] = useState<string>('all');

  // Discovery state
  const [scanning, setScanning] = useState(false);
  const [discoveryResult, setDiscoveryResult] = useState<DiscoveryResult | null>(null);

  // Multicloud state
  const [clouds, setClouds] = useState<MulticloudData[]>(demoMulticloud);
  const [mcMode, setMcMode] = useState<'loading' | 'demo' | 'real'>('loading');
  const loadClouds = useCallback(async () => {
    const r = await fetchApi<MulticloudData[]>('/api/v1/multicloud', demoMulticloud);
    setClouds(r.data);
    setMcMode(r.mode === 'live' ? 'real' : 'demo');
  }, []);
  useEffect(() => { loadClouds(); }, [loadClouds]);
  useEffect(() => {
    if (mcMode !== 'real') return;
    const iv = setInterval(loadClouds, 30000);
    return () => clearInterval(iv);
  }, [mcMode, loadClouds]);

  // 过滤
  const filtered = activeType === 'all'
    ? environments
    : environments.filter(e => e.env_type === activeType);

  const typeCounts: Record<string, number> = {};
  environments.forEach(e => { typeCounts[e.env_type] = (typeCounts[e.env_type] || 0) + 1; });

  const typeOptions = [
    { key: 'all', label: '全部', icon: '🏠', count: environments.length },
    { key: 'pure_on_prem', label: '纯本地', icon: '🏢' },
    { key: 'pure_virtual', label: '纯虚拟化', icon: '🖥️' },
    { key: 'pure_container', label: '纯容器', icon: '🐳' },
    { key: 'dr_standby', label: '主备/灾备', icon: '🔄' },
    { key: 'multi_active', label: '多活', icon: '⚡' },
    { key: 'pure_cloud', label: '纯云', icon: '☁️' },
    { key: 'serverless_cloud', label: 'Serverless', icon: 'λ' },
    { key: 'hosted_private', label: '托管私有云', icon: '🏰' },
    { key: 'hybrid_virtual_cloud', label: '混合云(虚拟+云)', icon: '🔗' },
    { key: 'hybrid_physical_cloud', label: '混合云(物理+云)', icon: '🔗' },
    { key: 'hybrid_container_cloud', label: '混合云(容器+云)', icon: '🔗' },
    { key: 'multi_cloud', label: '多云', icon: '🌐' },
    { key: 'cross_border', label: '跨境', icon: '🌍' },
    { key: 'edge', label: '边缘+云', icon: '📡' },
    { key: 'full_edge', label: '三层架构', icon: '📡' },
    { key: 'domestic_stack', label: '国产化全栈', icon: '🇨🇳' },
  ];

  // ── 探测逻辑 ──
  const startDiscovery = () => {
    setScanning(true);
    setTimeout(() => {
      setDiscoveryResult(demoDiscovery);
      setScanning(false);
    }, 2000);
  };

  // ── 保存发现结果到环境列表 ──
  const saveDiscovery = () => {
    if (!discoveryResult) return;
    const topo = discoveryResult.inferred_topology;
    const newEnv: Environment = {
      env_id: `env-discovered-${Date.now()}`,
      env_name: `${discoveryResult.os.hostname} — ${discoveryResult.os.os_name}`,
      env_type: topo.type,
      topology_label: topo.label,
      topology_icon: topo.type.includes('cloud') ? '☁️' : topo.type.includes('container') ? '🐳' : '🏢',
      description: `${discoveryResult.os.os_name} ${discoveryResult.os.os_version} · ${discoveryResult.hardware.cpu_cores}核 ${discoveryResult.hardware.memory_gb}GB · ${discoveryResult.middleware.map(m=>m.name).join('/')}`,
      cloud_regions: discoveryResult.cloud.is_cloud ? [{
        region_id: discoveryResult.cloud.region || 'unknown',
        region_name: discoveryResult.cloud.region || '未知',
        provider: discoveryResult.cloud.provider || 'unknown',
        zones: [], network_zone: 'production', latency_ms: null,
      }] : [],
      on_prem_sites: !discoveryResult.cloud.is_cloud ? [{
        site_id: 'discovered-site', site_name: discoveryResult.os.hostname,
        location: '本地', infra_provider: 'kvm', network_zone: 'production', storage_type: '本地',
      }] : [],
      edge_sites: [], cross_border_links: [],
      network_zones: ['production'],
      interconnects: [],
      resources: {
        total_servers: discoveryResult.hardware.is_virtual ? 0 : 1,
        total_vms: discoveryResult.hardware.is_virtual ? 1 : 0,
        total_containers: discoveryResult.services.docker_containers,
        total_k8s_clusters: discoveryResult.kubernetes.nodes,
        total_databases: discoveryResult.databases.length,
        total_network_devices: 0,
        total_storage_tb: Math.round(discoveryResult.hardware.disk_gb / 1000 * 10) / 10 || 0.5,
        total_monthly_cost_yuan: 0,
      },
      health: { score: 95, status: 'healthy', last_check: '刚刚', issues: [], cross_region_latency_ms: 0 },
      all_providers: discoveryResult.cloud.is_cloud ? [discoveryResult.cloud.provider] : ['kvm'],
      all_regions: discoveryResult.cloud.is_cloud ? [`${discoveryResult.cloud.provider}:${discoveryResult.cloud.region}`] : [`onprem:${discoveryResult.os.hostname}`],
      tags: ['discovered', discoveryResult.os.os_type, ...discoveryResult.middleware.map(m => m.name.toLowerCase())],
      enabled: true,
      source: 'discovered',
    };
    setEnvironments(prev => [newEnv, ...prev]);
    setDiscoveryResult(null);
    setTab('manage');
  };

  const removeEnvironment = (id: string) => {
    setEnvironments(prev => prev.filter(e => e.env_id !== id));
  };

  const highAgents = discoveryResult?.recommended_agents.filter(a => a.priority === 'high') || [];
  const medAgents = discoveryResult?.recommended_agents.filter(a => a.priority === 'medium') || [];
  const categories = [...new Set(discoveryResult?.recommended_agents.map(a => a.category) || [])];

  return (
    <div className="animate-fade-in">
      {/* ── 顶部：标题 + Tab 切换 ── */}
      <div className="page-header">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
          <div>
            <h1 className="page-title">🏗️ 环境管理</h1>
            <p className="page-subtitle">自动发现 + 全场景管理 · {environments.length} 个环境</p>
          </div>
          <div style={{ display: 'flex', gap: 4, padding: 3, borderRadius: 10, background: 'rgba(255,255,255,0.05)' }}>
            <button onClick={() => setTab('discover')} style={{
              padding: '7px 18px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: 600,
              background: tab === 'discover' ? 'linear-gradient(135deg, #3b82f6, #8b5cf6)' : 'transparent',
              color: tab === 'discover' ? '#fff' : 'var(--text-secondary)',
              transition: 'all 0.2s',
            }}>
              🔍 环境发现
            </button>
            <button onClick={() => setTab('manage')} style={{
              padding: '7px 18px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: 600,
              background: tab === 'manage' ? 'linear-gradient(135deg, #10b981, #06b6d4)' : 'transparent',
              color: tab === 'manage' ? '#fff' : 'var(--text-secondary)',
              transition: 'all 0.2s',
            }}>
              🏗️ 环境列表
            </button>
            <button onClick={() => setTab('multicloud')} style={{
              padding: '7px 18px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: 600,
              background: tab === 'multicloud' ? 'linear-gradient(135deg, #f97316, #ef4444)' : 'transparent',
              color: tab === 'multicloud' ? '#fff' : 'var(--text-secondary)',
              transition: 'all 0.2s',
            }}>
              ☁️ 多云账户
            </button>
          </div>
        </div>
      </div>

      {/* ═══ 环境发现 Tab ═══ */}
      {tab === 'discover' && (
        <>
          {/* 探测按钮 */}
          {!discoveryResult && !scanning && (
            <div className="card" style={{ padding: 40, textAlign: 'center' }}>
              <div style={{ fontSize: 48, marginBottom: 16 }}>🔍</div>
              <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 8 }}>一键环境探测</div>
              <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 20, maxWidth: 400, margin: '0 auto 20px' }}>
                自动检测操作系统、硬件、云平台、容器、中间件、数据库、网络等，<br/>推断环境拓扑并推荐最佳 Agent 组合
              </div>
              <button onClick={startDiscovery} style={{
                padding: '12px 32px', borderRadius: 10, border: 'none',
                background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', color: '#fff',
                cursor: 'pointer', fontSize: 14, fontWeight: 600,
              }}>
                🚀 开始探测
              </button>
              <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 8 }}>本地运行时自动检测 · Dashboard 使用 Demo 数据</div>
            </div>
          )}

          {/* 扫描中 */}
          {scanning && (
            <div className="card" style={{ padding: 40, textAlign: 'center' }}>
              <div style={{ fontSize: 48, marginBottom: 16, animation: 'spin 1s linear infinite' }}>⚙️</div>
              <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 8 }}>正在探测环境...</div>
              <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>检测系统信息 · 扫描中间件 · 发现数据库</div>
              <div style={{ display: 'flex', gap: 4, justifyContent: 'center', marginTop: 16 }}>
                {['OS', 'HW', 'Cloud', 'Docker', 'K8s', 'DB', 'MW', 'Net'].map((step, i) => (
                  <div key={step} style={{
                    padding: '3px 8px', borderRadius: 4, fontSize: 10,
                    background: 'rgba(59,130,246,0.15)', color: '#3b82f6',
                  }}>
                    {step}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 探测结果 */}
          {discoveryResult && (
            <>
              {/* 推断拓扑 */}
              <div className="card" style={{
                padding: '16px 20px', marginBottom: 16,
                background: 'linear-gradient(135deg, rgba(59,130,246,0.08), rgba(139,92,246,0.08))',
                border: '2px solid rgba(59,130,246,0.2)',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <div style={{ fontSize: 11, color: '#3b82f6', fontWeight: 600 }}>🎯 推断环境拓扑</div>
                    <div style={{ fontSize: 18, fontWeight: 700, marginTop: 4 }}>{discoveryResult.inferred_topology.label}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: 24, fontWeight: 700, color: '#3b82f6' }}>{discoveryResult.inferred_topology.confidence}%</div>
                    <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>置信度</div>
                  </div>
                </div>
              </div>

              {/* 探测结果网格 */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12, marginBottom: 16 }}>
                <DetectionCard title="操作系统" icon="🐧" color="#10b981" items={[
                  { label: '系统', value: discoveryResult.os.os_name, highlight: true },
                  { label: '版本', value: discoveryResult.os.os_version },
                  { label: '内核', value: discoveryResult.os.kernel },
                  { label: '架构', value: discoveryResult.os.arch },
                  { label: '主机名', value: discoveryResult.os.hostname },
                  { label: '国产OS', value: !!discoveryResult.os.domestic_os },
                ]} />
                <DetectionCard title="硬件" icon="🖥️" color="#3b82f6" items={[
                  { label: 'CPU', value: `${discoveryResult.hardware.cpu_cores} 核 (${discoveryResult.hardware.arch})`, highlight: true },
                  { label: '内存', value: `${discoveryResult.hardware.memory_gb} GB`, highlight: true },
                  { label: '磁盘', value: `${discoveryResult.hardware.disk_gb} GB` },
                  { label: '负载', value: discoveryResult.hardware.load_1m },
                  { label: '虚拟化', value: discoveryResult.hardware.is_virtual ? discoveryResult.hardware.virtual_type || '是' : '物理机' },
                ]} />
                <DetectionCard title="云平台" icon="☁️" color="#f97316" items={[
                  { label: '云环境', value: discoveryResult.cloud.is_cloud ? '是' : '否', highlight: true },
                  { label: '厂商', value: discoveryResult.cloud.provider || '-' },
                  { label: '区域', value: discoveryResult.cloud.region || '-' },
                  { label: '规格', value: discoveryResult.cloud.instance_type || '-' },
                ]} />
                <DetectionCard title="容器" icon="🐳" color="#0ea5e9" items={[
                  { label: 'Docker', value: discoveryResult.containers.docker, highlight: true },
                  { label: '版本', value: discoveryResult.containers.docker_version || '-' },
                  { label: '运行中', value: discoveryResult.containers.docker_running },
                  { label: 'containerd', value: discoveryResult.containers.containerd },
                  { label: 'Podman', value: discoveryResult.containers.podman },
                  { label: 'K3s', value: discoveryResult.containers.k3s },
                ]} />
                <DetectionCard title="Kubernetes" icon="☸️" color="#8b5cf6" items={[
                  { label: '可用', value: discoveryResult.kubernetes.available, highlight: true },
                  { label: '版本', value: discoveryResult.kubernetes.version || '-' },
                  { label: '节点', value: discoveryResult.kubernetes.nodes },
                  { label: 'Pods', value: discoveryResult.kubernetes.pods },
                  { label: '云厂商', value: discoveryResult.kubernetes.provider || '-' },
                ]} />
                <DetectionCard title="网络" icon="🌐" color="#06b6d4" items={[
                  { label: '内网IP', value: discoveryResult.network.private_ip, highlight: true },
                  { label: '公网IP', value: discoveryResult.network.public_ip || '无' },
                  { label: 'DNS', value: discoveryResult.network.dns.join(', ') },
                  { label: '网卡数', value: discoveryResult.network.interfaces.length },
                  { label: '监听端口', value: discoveryResult.services.listening_ports.length },
                ]} />
              </div>

              {/* 中间件和数据库 */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
                <div className="card" style={{ padding: '14px 16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                    <span style={{ fontSize: 18 }}>📦</span>
                    <span style={{ fontWeight: 600, fontSize: 13 }}>中间件 ({discoveryResult.middleware.length})</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {discoveryResult.middleware.map(m => (
                      <div key={m.name} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '6px 10px', borderRadius: 6, background: 'rgba(255,255,255,0.03)' }}>
                        <span style={{ color: m.running ? '#10b981' : '#ef4444', fontSize: 10 }}>{m.running ? '●' : '○'}</span>
                        <span style={{ fontWeight: 600, fontSize: 12, minWidth: 80 }}>{m.name}</span>
                        <span style={{ fontSize: 10, color: 'var(--text-muted)', fontFamily: 'monospace' }}>{m.version}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="card" style={{ padding: '14px 16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                    <span style={{ fontSize: 18 }}>🗄️</span>
                    <span style={{ fontWeight: 600, fontSize: 13 }}>数据库 ({discoveryResult.databases.length})</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {discoveryResult.databases.map(d => (
                      <div key={d.name} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '6px 10px', borderRadius: 6, background: 'rgba(255,255,255,0.03)' }}>
                        <span style={{ color: d.running ? '#10b981' : '#ef4444', fontSize: 10 }}>{d.running ? '●' : '○'}</span>
                        <span style={{ fontWeight: 600, fontSize: 12, minWidth: 80 }}>{d.name}</span>
                        <span style={{ fontSize: 10, color: 'var(--text-muted)', fontFamily: 'monospace' }}>:{d.port}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* 推荐 Agent 组合 */}
              <div className="card" style={{ padding: '16px 20px', marginBottom: 16 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
                  <span style={{ fontSize: 20 }}>🤖</span>
                  <div>
                    <span style={{ fontWeight: 700, fontSize: 14 }}>推荐 Agent 组合</span>
                    <span style={{ fontSize: 11, color: 'var(--text-muted)', marginLeft: 8 }}>基于探测结果自动推荐</span>
                  </div>
                </div>
                <div style={{ marginBottom: 12 }}>
                  <div style={{ fontSize: 11, fontWeight: 600, color: '#ef4444', marginBottom: 8 }}>🔴 核心 Agent (必须启用)</div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 8 }}>
                    {highAgents.map(a => (
                      <div key={a.name} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 12px', borderRadius: 8, background: 'rgba(239,68,68,0.06)', border: '1px solid rgba(239,68,68,0.2)' }}>
                        <span style={{ fontSize: 22 }}>{a.icon}</span>
                        <div>
                          <div style={{ fontWeight: 600, fontSize: 12 }}>{a.name}</div>
                          <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>{a.reason}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: 11, fontWeight: 600, color: '#3b82f6', marginBottom: 8 }}>🔵 推荐 Agent (按需启用)</div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 8 }}>
                    {medAgents.map(a => (
                      <div key={a.name} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 12px', borderRadius: 8, background: 'rgba(59,130,246,0.06)', border: '1px solid rgba(59,130,246,0.15)' }}>
                        <span style={{ fontSize: 22 }}>{a.icon}</span>
                        <div>
                          <div style={{ fontWeight: 600, fontSize: 12 }}>{a.name}</div>
                          <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>{a.reason}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div style={{ display: 'flex', gap: 8, marginTop: 14, flexWrap: 'wrap' }}>
                  {categories.map(cat => (
                    <span key={cat} style={{ padding: '3px 10px', borderRadius: 6, fontSize: 10, fontWeight: 500, background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)' }}>
                      {cat}: {discoveryResult.recommended_agents.filter(a => a.category === cat).length} 个
                    </span>
                  ))}
                  <span style={{ padding: '3px 10px', borderRadius: 6, fontSize: 10, fontWeight: 600, background: 'rgba(59,130,246,0.1)', color: '#3b82f6' }}>
                    共 {discoveryResult.recommended_agents.length} 个 Agent
                  </span>
                </div>
              </div>

              {/* 操作按钮 */}
              <div style={{ display: 'flex', gap: 10, justifyContent: 'center', marginTop: 16 }}>
                <button onClick={saveDiscovery} style={{
                  padding: '10px 28px', borderRadius: 8, border: 'none',
                  background: 'linear-gradient(135deg, #10b981, #06b6d4)', color: '#fff',
                  cursor: 'pointer', fontSize: 13, fontWeight: 600,
                }}>
                  💾 保存到环境列表
                </button>
                <button onClick={() => { setDiscoveryResult(null); }} style={{
                  padding: '8px 20px', borderRadius: 8, border: '1px solid var(--border)',
                  background: 'transparent', color: 'var(--text-secondary)', cursor: 'pointer', fontSize: 12,
                }}>
                  🔄 重新探测
                </button>
              </div>
            </>
          )}
        </>
      )}

      {/* ═══ 环境管理 Tab ═══ */}
      {tab === 'manage' && (
        <>
          <SummaryStats envs={filtered} />

          {/* 拓扑类型筛选 */}
          <div style={{ display: 'flex', gap: 6, marginBottom: 16, flexWrap: 'wrap' }}>
            {typeOptions.map(opt => {
              const count = opt.key === 'all' ? environments.length : (typeCounts[opt.key] || 0);
              if (opt.key !== 'all' && count === 0) return null;
              const tc = opt.key === 'all' ? '#6b7280' : (typeColors[opt.key] || '#6b7280');
              return (
                <button
                  key={opt.key}
                  onClick={() => setActiveType(opt.key)}
                  style={{
                    padding: '5px 12px', borderRadius: 8, cursor: 'pointer', fontSize: 11,
                    border: `1px solid ${activeType === opt.key ? tc + '60' : 'var(--border)'}`,
                    background: activeType === opt.key ? `${tc}18` : 'transparent',
                    color: activeType === opt.key ? tc : 'var(--text-secondary)',
                    fontWeight: 500, transition: 'all 0.15s',
                  }}
                >
                  {opt.icon} {opt.label} ({count})
                </button>
              );
            })}
          </div>

          {/* 环境列表 */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {filtered.map(env => (
              <EnvironmentCard key={env.env_id} env={env} onRemove={removeEnvironment} />
            ))}
            {filtered.length === 0 && (
              <div className="card" style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
                <div style={{ fontSize: 32, marginBottom: 8 }}>🔍</div>
                <div>暂无匹配的环境</div>
                <button onClick={() => setTab('discover')} style={{
                  marginTop: 12, padding: '8px 20px', borderRadius: 8, border: '1px solid rgba(59,130,246,0.3)',
                  background: 'rgba(59,130,246,0.08)', color: '#3b82f6', cursor: 'pointer', fontSize: 12,
                }}>
                  🔍 去发现新环境
                </button>
              </div>
            )}
          </div>
        </>
      )}

      {/* ═══ 多云账户 Tab ═══ */}
      {tab === 'multicloud' && (
        <div style={{ animation: 'fadeIn 0.3s ease' }}>
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
            <span style={{ padding: '6px 12px', borderRadius: 8, background: mcMode === 'real' ? 'rgba(16,185,129,0.12)' : 'rgba(245,158,11,0.12)', color: mcMode === 'real' ? '#10b981' : '#f59e0b', fontSize: 12, fontWeight: 600 }}>
              {mcMode === 'real' ? '🟢 实时' : '🟡 Demo'}
            </span>
          </div>

          {/* Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 20 }}>
            {[
              { label: '云平台', value: clouds.length, icon: '☁️', color: '#3b82f6', bg: 'rgba(59,130,246,0.12)' },
              { label: '总实例', value: clouds.reduce((a: number, c: MulticloudData) => a + c.instances, 0), icon: '🖥️', color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
              { label: '月费用', value: `¥${(clouds.reduce((a: number, c: MulticloudData) => a + c.monthly_cost, 0) / 10000).toFixed(1)}万`, icon: '💰', color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
              { label: '区域', value: clouds.reduce((a: number, c: MulticloudData) => a + c.regions.length, 0), icon: '🌍', color: '#8b5cf6', bg: 'rgba(139,92,246,0.12)' },
            ].map((item, i) => (
              <div key={i} className="card" style={{ padding: 20, display: 'flex', alignItems: 'center', gap: 14 }}>
                <div style={{ width: 48, height: 48, borderRadius: 12, background: item.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22 }}>{item.icon}</div>
                <div><div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{item.label}</div><div style={{ fontSize: 28, fontWeight: 700, color: item.color }}>{item.value}</div></div>
              </div>
            ))}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16, marginBottom: 20 }}>
            {/* Cloud Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              {clouds.map((c: MulticloudData, i: number) => {
                const cfg = c.status === 'healthy' ? { color: '#10b981', bg: 'rgba(16,185,129,0.12)' }
                  : c.status === 'degraded' ? { color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' }
                  : { color: '#ef4444', bg: 'rgba(239,68,68,0.12)' };
                const pi: Record<string, string> = { '阿里云': '🟣', 'AWS': '🟠', '华为云': '🔴', '腾讯云': '🔵', 'Azure': '🔵', 'GCP': '🔴' };
                return (
                  <div key={i} className="card" style={{ padding: 20, borderLeft: `3px solid ${cfg.color}` }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span style={{ fontSize: 24 }}>{pi[c.provider] || '☁️'}</span>
                        <span style={{ fontSize: 16, fontWeight: 700 }}>{c.provider}</span>
                      </div>
                      <span style={{ padding: '3px 8px', borderRadius: 4, fontSize: 10, fontWeight: 600, background: cfg.bg, color: cfg.color }}>{c.status}</span>
                    </div>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 8 }}>
                      {c.regions.join(' · ')}
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8 }}>
                      <div style={{ textAlign: 'center', padding: 8, background: 'rgba(255,255,255,0.02)', borderRadius: 8 }}>
                        <div style={{ fontSize: 18, fontWeight: 700, color: '#3b82f6' }}>{c.instances}</div>
                        <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>实例</div>
                      </div>
                      <div style={{ textAlign: 'center', padding: 8, background: 'rgba(255,255,255,0.02)', borderRadius: 8 }}>
                        <div style={{ fontSize: 18, fontWeight: 700, color: '#f59e0b' }}>¥{(c.monthly_cost / 1000).toFixed(0)}k</div>
                        <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>月费</div>
                      </div>
                      <div style={{ textAlign: 'center', padding: 8, background: 'rgba(255,255,255,0.02)', borderRadius: 8 }}>
                        <div style={{ fontSize: 14, fontWeight: 600, color: '#10b981', marginTop: 4 }}>{c.services.length}</div>
                        <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>服务</div>
                      </div>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 10 }}>
                      {c.services.map((s: string, j: number) => (
                        <span key={j} style={{ padding: '2px 6px', borderRadius: 4, fontSize: 9, background: 'rgba(59,130,246,0.1)', color: '#60a5fa' }}>{s}</span>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Cost Pie */}
            <div className="card" style={{ padding: 20 }}>
              <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>💰 费用分布</div>
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie data={clouds.map((c: MulticloudData) => ({ name: c.provider, value: c.monthly_cost }))} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" label={({ name, percent }: any) => `${name} ${((percent || 0) * 100).toFixed(0)}%`} labelLine={false}>
                    {clouds.map((_: any, i: number) => <Cell key={i} fill={['#8b5cf6', '#f97316', '#ef4444', '#3b82f6', '#06b6d4'][i % 5]} />)}
                  </Pie>
                  <Tooltip formatter={(v: any) => `¥${Number(v).toLocaleString()}`} />
                </PieChart>
              </ResponsiveContainer>
              <div style={{ borderTop: '1px solid var(--border)', paddingTop: 12, marginTop: 8 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: 'var(--text-muted)' }}>
                  <span>总月费</span>
                  <span style={{ fontWeight: 700, color: '#f59e0b' }}>¥{clouds.reduce((a: number, c: MulticloudData) => a + c.monthly_cost, 0).toLocaleString()}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
