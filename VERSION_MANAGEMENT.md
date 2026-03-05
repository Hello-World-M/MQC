# 版本管理指南

本文档说明如何进行版本管理和回退操作，确保在 purge 后也能安全恢复。

## 当前版本

- **最新版本**: v0.1.0
- **发布日期**: 2026-03-05

## 版本历史

| 版本 | 提交 SHA | 描述 |
|------|----------|------|
| v0.1.0 | 3a76cd0 | 初始版本，包含扫雷游戏和项目配置 |
| (未标记) | 9370624 | 添加扫雷游戏项目 |
| (未标记) | ba3f803 | 初始提交 |

## 版本回退指南

### 方案 1: 回退到指定标签（推荐）

```bash
# 查看所有标签
git tag

# 回退到 v0.1.0
git checkout v0.1.0

# 或者创建新分支从标签开始
git checkout -b restore-branch v0.1.0
```

### 方案 2: 使用 git reflog（即使 purge 后也能恢复）

```bash
# 查看 reflog 历史
git reflog

# 找到目标提交的 SHA（例如 3a76cd0）
# 使用 reset 回退
git reset --hard 3a76cd0

# 或者创建新分支指向旧提交
git checkout -b restore-branch 3a76cd0
```

### 方案 3: 从远端恢复（如果本地被 purge）

```bash
# 强制拉取远端最新状态
git fetch origin
git reset --hard origin/main

# 或者从远端标签恢复
git fetch --tags
git checkout v0.1.0
```

## 版本发布流程

### 创建新版本

```bash
# 1. 确保所有更改已提交
git status

# 2. 创建带注释的标签
git tag -a v0.2.0 -m "Release v0.2.0

新增功能：
- 功能描述 1
- 功能描述 2

修复问题：
- 修复的问题 1
- 修复的问题 2"

# 3. 推送标签到远端
git push origin v0.2.0
```

### 版本命名规范

遵循语义化版本（Semantic Versioning）：
- **MAJOR.MINOR.PATCH**（例如：1.0.0, 1.2.3）

  - **MAJOR**: 不兼容的 API 修改
  - **MINOR**: 向下兼容的功能新增
  - **PATCH**: 向下兼容的问题修正

示例：
- `v0.1.0` → `v0.1.1` (Bug 修复)
- `v0.1.0` → `v0.2.0` (新增功能)
- `v0.1.0` → `v1.0.0` (重大更新)

## 提交信息规范

使用 Conventional Commits 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型（type）
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链相关
- `ci`: CI/CD 配置

### 示例

```bash
# 功能添加
git commit -m "feat(game): 添加计时器功能"

# Bug 修复
git commit -m "fix(game): 修复首次点击保护失效问题"

# 文档更新
git commit -m "docs(readme): 更新安装说明"

# JIRA 集成
git commit -m "fix(core): 修复内存泄漏问题

JIRA: MQC-123"
```

## 备份建议

### 定期备份到远端

```bash
# 每次重要更改后推送
git push origin main

# 推送所有标签
git push origin --tags
```

### 使用 GitHub Release

在 GitHub 上创建正式 Release：
1. 进入仓库的 Releases 页面
2. 点击 "Create a new release"
3. 选择或创建标签（例如 v0.1.0）
4. 填写发布说明
5. 发布

GitHub Release 会永久保存该版本，即使 purge 也不会丢失。

## 紧急恢复清单

如果遇到 purge 或误操作，按以下顺序尝试：

1. ✅ **检查本地 reflog**: `git reflog`
2. ✅ **从远端拉取**: `git fetch origin && git reset --hard origin/main`
3. ✅ **从标签恢复**: `git checkout v0.1.0`
4. ✅ **从 GitHub Release 下载**: 在 GitHub Releases 页面下载源码
5. ✅ **从远端仓库克隆**: `git clone git@github.com:Hello-World-M/MQC.git`

## 防护措施

### 启用分支保护（GitHub 设置）

1. 进入仓库 Settings → Branches
2. 添加分支保护规则
3. 保护 `main` 分支，要求：
   - Pull Request 审查
   - 状态检查通过
   - 限制直接推送

### 配置 Git Hooks

在 `.git/hooks/pre-commit` 中添加保护逻辑（可选）。

## 相关资源

- [语义化版本](https://semver.org/lang/zh-CN/)
- [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)
- [Git Reflog 文档](https://git-scm.com/docs/git-reflog)
