# 安装指南

## 系统要求

- Python 3.9+
- SSH 访问目标服务器
- AI API Key (DeepSeek/OpenAI/Anthropic)

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://gitee.com/neal4752/agentic-aiops.git
cd agentic-aiops
```

### 2. 安装依赖

```bash
# 基础安装
pip install -e .

# 安装所有可选依赖
pip install -e ".[all]"

# 仅安装开发依赖
pip install -e ".[dev]"
```

### 3. 配置

```bash
cp config.example.yaml config.yaml
```

编辑 `config.yaml`：

```yaml
servers:
  - name: production
    host: 10.0.0.1
    port: 22
    user: root
    # 建议使用环境变量存储密码

ai:
  enabled: true
  provider: deepseek
  # api_key 建议使用环境变量
  model: deepseek-chat
```

### 4. 设置环境变量

```bash
# Linux/macOS
export AIOPS_SERVER_PRODUCTION_PASSWORD="your-password"
export AIOPS_AI_API_KEY="your-api-key"

# Windows PowerShell
$env:AIOPS_SERVER_PRODUCTION_PASSWORD="your-password"
$env:AIOPS_AI_API_KEY="your-api-key"
```

### 5. 验证安装

```bash
aiops version
aiops tools
```

## Docker 安装

```bash
docker build -t agentic-aiops .
docker run -it agentic-aiops aiops diagnose --help
```

## 常见问题

### Q: 连接服务器失败？

检查：
1. SSH 密钥或密码配置
2. 服务器防火墙
3. 网络连通性

### Q: AI API 调用失败？

检查：
1. API Key 是否正确
2. 网络是否能访问 API 地址
3. 余额是否充足
