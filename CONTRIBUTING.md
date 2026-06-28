# 贡献指南

感谢你对 Agentic AIOps 的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 1. Fork 仓库

```bash
# 点击 Fork 按钮
# 然后 Clone 你的 Fork
git clone https://gitee.com/your-username/agentic-aiops.git
cd agentic-aiops
```

### 2. 创建分支

```bash
# 创建特性分支
git checkout -b feature/your-feature

# 或修复分支
git checkout -b fix/your-fix
```

### 3. 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black aiops/

# 类型检查
mypy aiops/
```

### 4. 提交

```bash
# 添加修改
git add .

# 提交（使用 Conventional Commits）
git commit -m "feat: 添加新功能"
git commit -m "fix: 修复 bug"
git commit -m "docs: 更新文档"
```

### 5. Push & PR

```bash
# Push 到你的 Fork
git push origin feature/your-feature

# 在 Gitee/GitHub 创建 Pull Request
```

## 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/)：

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `test` | 测试 |
| `chore` | 构建/工具 |
| `ci` | CI 配置 |

## 开发环境

### 必需

- Python 3.9+
- Git

### 可选

- Docker
- kubectl
- Terraform

### IDE 推荐

- VS Code + Python 插件
- PyCharm

## 代码规范

### Python 风格

- 遵循 PEP 8
- 使用 Black 格式化
- 类型注解
- Docstring (Google style)

### 示例

```python
def diagnose_cpu(host: str, threshold: int = 80) -> DiagnoseResult:
    """
    诊断 CPU 问题

    Args:
        host: 目标主机
        threshold: CPU 阈值

    Returns:
        诊断结果
    """
    pass
```

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_memory.py

# 覆盖率
pytest --cov=aiops
```

## 文档

- 新功能请更新相关文档
- 确保文档清晰易懂
- 添加使用示例

## Issue 规范

### Bug 报告

```markdown
## 描述
简要描述问题

## 复现步骤
1. ...
2. ...

## 期望行为
描述期望的行为

## 实际行为
描述实际的行为

## 环境
- OS: 
- Python: 
- Version: 
```

### Feature Request

```markdown
## 描述
简要描述功能需求

## 使用场景
描述使用场景

## 实现建议
如果有，提出实现建议
```

## 行为准则

- 尊重每一位参与者
- 建设性的反馈
- 专注于技术
- 欢迎新人

## 联系方式

- Issues: https://gitee.com/neal4752/agentic-aiops/issues
- Email: neal@example.com

## 致谢

感谢所有贡献者！

[![Contributors](https://contrib.rocks/image?repo=neal4752/agentic-aiops)]()
