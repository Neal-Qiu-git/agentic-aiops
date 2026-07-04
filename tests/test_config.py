from aiops.core.config import Config, ServerConfig

def test_default():
    assert Config().servers == []

def test_get_server():
    c = Config()
    c.servers.append(ServerConfig(name="s1", host="1.1.1.1"))
    assert c.get_server(name="s1").host == "1.1.1.1"
    assert c.get_server(name="nope") is None
