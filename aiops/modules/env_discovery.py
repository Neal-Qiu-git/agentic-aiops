"""环境发现模块"""
from ..collectors.system import SystemCollector
from ..collectors.docker import DockerCollector
from ..collectors.network import NetworkCollector
from ..collectors.service import ServiceCollector

class EnvDiscoveryModule:
    name = "env-discovery"
    def run(self, ctx):
        ssh, server = ctx["ssh"], ctx["server"]
        sys_d = SystemCollector().collect(ssh,server)
        docker_d = DockerCollector().collect(ssh,server)
        net_d = NetworkCollector().collect(ssh,server)
        svc_d = ServiceCollector().collect(ssh,server)
        ports = []
        for p in net_d.get("listening_ports",[]):
            local = p.get("local","")
            if ":" in local:
                port = local.rsplit(":",1)[-1]
                if port.isdigit(): ports.append(int(port))
        return {"inventory":{"hostname":sys_d.get("hostname",""),"os":sys_d.get("os",""),
                "cpu_cores":sys_d.get("cpu",{}).get("cores",0),
                "memory_gb":round(sys_d.get("memory",{}).get("total",0)/1024**3,1),
                "open_ports":sorted(set(ports)),"docker":docker_d.get("available",False),
                "failed_services":len(svc_d.get("failed",[]))}}
