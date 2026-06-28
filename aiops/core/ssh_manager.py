"""SSH 连接管理器"""
import paramiko, os

class SSHManager:
    def __init__(self, timeout=10, retry=3, retry_delay=5):
        self.timeout = timeout; self.retry = retry; self.retry_delay = retry_delay; self._clients = {}

    def connect(self, server):
        key = f"{server.host}:{server.port}"
        if key in self._clients:
            try: self._clients[key].exec_command("echo ok", timeout=3); return self._clients[key]
            except: del self._clients[key]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        kw = {"hostname": server.host, "port": server.port, "username": server.user, "timeout": self.timeout}
        if server.key_file: kw["key_filename"] = os.path.expanduser(server.key_file)
        elif server.password: kw["password"] = server.password
        for attempt in range(self.retry):
            try: client.connect(**kw); self._clients[key] = client; return client
            except Exception as e:
                if attempt < self.retry - 1: import time; time.sleep(self.retry_delay)
                else: raise ConnectionError(f"连接失败 {server.host}: {e}")

    def exec_command(self, server, command, timeout=30):
        client = self.connect(server)
        _, stdout, stderr = client.exec_command(command, timeout=timeout)
        return stdout.read().decode("utf-8", errors="replace"), stderr.read().decode("utf-8", errors="replace"), stdout.channel.recv_exit_status()

    def close(self):
        for c in self._clients.values():
            try: c.close()
            except: pass
        self._clients.clear()
