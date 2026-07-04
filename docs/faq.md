# FAQ

## 常见问题

### Q: 连接服务器失败？

**A:** 检查以下几点：

1. SSH 密钥或密码配置是否正确
2. 服务器防火墙是否开放 22 端口
3. 网络是否能连通服务器

```bash
# 测试连接
aiops tools run ssh_test_connection --host 10.0.0.1
```

### Q: AI API 调用失败？

**A:** 检查以下几点：

1. API Key 是否正确设置
2. 网络是否能访问 API 地址
3. 账户余额是否充足

```bash
# 测试 API
aiops test-api --provider deepseek
```

### Q: 命令被安全策略阻止？

**A:** 检查命令是否在黑名单中：

```yaml
security:
  blocked_commands:
    - rm -rf
    - shutdown
```

可以临时关闭安全检查（不推荐生产环境）：

```yaml
security:
  enabled: false
```

### Q: 如何添加自定义工具？

**A:** 参考 [MCP 工具市场文档](mcp.md) 中的插件开发章节。

### Q: 如何配置审批流程？

**A:** 参考 [审批系统文档](approval.md)。

### Q: 记忆数据存储在哪里？

**A:** 默认存储在 `~/.aiops/memory/` 目录：

```
~/.aiops/memory/
├── short_term/    # 短期记忆
├── long_term/     # 长期记忆
├── semantic/      # 语义记忆
└── episodic/      # 情景记忆
```

### Q: 如何备份知识库？

**A:** 知识库存储在 `~/.aiops/knowledge/` 目录：

```bash
# 备份
cp -r ~/.aiops/knowledge/ /backup/knowledge/

# 恢复
cp -r /backup/knowledge/ ~/.aiops/knowledge/
```

### Q: 支持哪些数据库？

**A:** 目前支持：

- MySQL
- Redis
- PostgreSQL
- MongoDB
- Elasticsearch
- Kafka

### Q: 支持哪些云平台？

**A:** 目前支持：

- AWS
- 阿里云
- 腾讯云

### Q: 如何查看审计日志？

**A:**

```bash
# 查看最近日志
aiops audit log --days 7

# 导出日志
aiops audit export --format csv --output audit.csv
```

### Q: 如何更新版本？

**A:**

```bash
# 更新代码
cd agentic-aiops
git pull

# 重新安装
pip install -e .

# 检查版本
aiops version
```

### Q: 如何贡献代码？

**A:** 请查看 [CONTRIBUTING.md](../CONTRIBUTING.md)。

### Q: 如何报告 Bug？

**A:** 请在 GitHub/Gitee 提交 Issue，包含：

1. 问题描述
2. 复现步骤
3. 期望行为
4. 实际行为
5. 环境信息
