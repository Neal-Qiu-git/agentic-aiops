# 贡献指南

感谢你对 Agentic AIOps 的关注！我们欢迎各种形式的贡献。

---

## 🌿 分支规范

### 分支类型

| 分支类型 | 命名格式 | 来源 | 合并目标 | 用途 |
|----------|----------|------|----------|------|
| `main` | `main` | — | — | 稳定发布版，每个tag对应可部署版本 |
| `develop` | `develop` | `main` | `main` | 日常开发主分支 |
| 功能分支 | `feat/xxx` | `develop` | `develop` | 新功能开发 |
| 修复分支 | `fix/xxx` | `main` 或 `develop` | `main` + `develop` | Bug修复 |
| 热修复 | `hotfix/xxx` | `main` | `main` + `develop` | 紧急线上修复 |
| 预发布 | `release/x.x.x` | `develop` | `main` + `develop` | 版本发布准备 |

### 分支工作流

```
main (稳定版)
  ↑
  ├── hotfix/xxx ──────→ 合并回 main + develop
  │
  ├── release/4.2.0 ──→ 合并回 main + develop
  │
  develop (开发版)
    ↑
    ├── feat/xxx ──────→ 合并回 develop
    │
    └── fix/xxx ───────→ 合并回 develop
```

### 操作流程

**开发新功能：**
```bash
git checkout develop
git checkout -b feat/新功能名
# 开发...
git add -A && git commit -m "feat: 描述"
git push origin feat/新功能名
# 在 Gitee 创建 PR → develop
```

**修复 Bug：**
```bash
git checkout develop
git checkout -b fix/修复描述
# 修复...
git add -A && git commit -m "fix: 描述"
git push origin fix/修复描述
# 在 Gitee 创建 PR → develop
```

**紧急线上修复：**
```bash
git checkout main
git checkout -b hotfix/紧急修复
# 修复...
git add -A && git commit -m "hotfix: 描述"
git push origin hotfix/紧急修复
# PR → main + develop
```

**版本发布：**
```bash
git checkout develop
git checkout -b release/4.2.0
# 最终测试、文档更新...
git push origin release/4.2.0
# PR → main（打 tag）+ develop
git checkout main
git tag -a v4.2.0 -m "版本说明"
git push origin v4.2.0
```

---

## 📌 版本号规范

遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)

```
MAJOR.MINOR.PATCH
  │      │      │
  │      │      └── PATCH: 小修复（bugfix、hotfix）
  │      └───────── MINOR: 新功能（向下兼容）
  └──────────────── MAJOR: 大版本（不兼容变更）
```

### 示例

| 变更类型 | 版本号 | 示例 |
|----------|--------|------|
| 修了个bug | `x.x.1` → `x.x.2` | v4.1.0 → v4.1.1 |
| 加了新Agent | `x.1.x` → `x.2.x` | v4.1.0 → v4.2.0 |
| 架构重构 | `1.x.x` → `2.0.0` | v4.2.0 → v5.0.0 |

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)：

```
<type>(<scope>): <subject>

type 类型：
  feat:     新功能
  fix:      Bug修复
  docs:     文档更新
  style:    代码格式（不影响功能）
  refactor: 重构
  test:     测试
  chore:    构建/工具变更
  perf:     性能优化

示例：
  feat(agent): 新增网络诊断 Agent
  fix(memory): 修复记忆检索超时问题
  docs: 更新安装文档
  chore(ci): 配置 GitHub Actions
```

---

## 🚀 快速开始

### 1. Fork 仓库

```bash
# 点击 Fork 按钮
git clone https://gitee.com/your-username/agentic-aiops.git
cd agentic-aiops
```

### 2. 创建分支

```bash
git checkout develop
git checkout -b feat/你的功能
```

### 3. 开发

```bash
pip install -e ".[dev]"
# 编写代码...
```

### 4. 测试

```bash
pytest tests/ -v
```

### 5. 提交 PR

```bash
git add -A
git commit -m "feat: 你的功能描述"
git push origin feat/你的功能
# 在 Gitee 创建 Pull Request → develop
```

---

## 📋 开发规范

### 代码风格

- Python: PEP 8 + Black 格式化
- 类型注解: 必须
- 文档字符串: 必须（Google style）
- 测试覆盖: 新功能必须有测试

### 文件组织

- `aiops/agents/` — 智能体代码
- `aiops/tools/` — MCP 工具
- `aiops/workflow/` — 工作流定义
- `examples/` — 使用示例
- `tests/` — 测试代码
- `docs/` — 文档
