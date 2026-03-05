# 贡献指南

感谢你对本项目的关注和贡献！本文档将帮助你了解如何参与开发。

## 📋 目录

- [开发流程](#开发流程)
- [分支策略](#分支策略)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)
- [测试要求](#测试要求)

## 开发流程

### 小型改动

**适用场景：**
- 文档更新（README、AGENTS.md 等）
- 配置文件修改（.gitignore、.editorconfig 等）
- 小型 bug 修复（不影响核心逻辑）
- 代码格式调整

**操作步骤：**
```bash
# 1. 直接在 main 分支修改
git checkout main

# 2. 进行修改
# ... 编辑文件 ...

# 3. 提交更改
git add .
git commit -m "docs: 更新安装说明"

# 4. 推送到远端
git push origin main
```

### 中型改动

**适用场景：**
- 新功能开发
- Bug 修复（影响核心逻辑）
- 功能改进
- 性能优化

**操作步骤：**
```bash
# 1. 创建功能分支
git checkout -b feature/your-feature-name

# 2. 进行开发
# ... 修改代码 ...
# ... 测试功能 ...

# 3. 提交更改
git add .
git commit -m "feat(game): 添加新功能"

# 4. 切换回 main 并合并
git checkout main
git merge feature/your-feature-name --no-ff

# 5. 删除功能分支
git branch -d feature/your-feature-name

# 6. 推送到远端
git push origin main
```

### 大型改动

**适用场景：**
- 重构项目结构
- 架构变更
- 多个相关功能

**操作步骤：**
```bash
# 1. 创建功能分支并充分开发
git checkout -b feature/your-feature-name

# 2. 多次提交，充分测试
# ... 开发 ...
# ... 测试 ...
# ... 修复 bug ...

# 3. 创建 PR 或直接合并（如无团队）
git checkout main
git merge feature/your-feature-name --no-ff

# 4. 删除分支
git branch -d feature/your-feature-name

# 5. 打标签（如果是发布）
git tag -a v0.3.0 -m "Release v0.3.0"

# 6. 推送
git push origin main --tags
```

### 紧急修复

**适用场景：**
- 已发布版本的严重 bug
- 生产环境问题

**操作步骤：**
```bash
# 1. 从最近的标签创建修复分支
git checkout v0.2.0
git checkout -b hotfix/critical-fix

# 2. 修复问题
# ... 修改 ...

# 3. 合并到 main
git checkout main
git merge hotfix/critical-fix --no-ff

# 4. 创建新标签
git tag -a v0.2.1 -m "Hotfix: 修复严重问题"

# 5. 删除修复分支
git branch -d hotfix/critical-fix

# 6. 推送
git push origin main --tags
```

## 分支策略

### 分支命名规范

| 类型 | 前缀 | 示例 | 说明 |
|------|--------|------|------|
| 功能开发 | `feature/` | `feature/random-mines` | 开发新功能 |
| Bug 修复 | `bugfix/` | `bugfix/display-error` | 修复非紧急 bug |
| 热修复 | `hotfix/` | `hotfix/crash-on-start` | 已发布版本的紧急修复 |
| 重构 | `refactor/` | `refactor/code-structure` | 代码重构 |
| 文档 | `docs/` | `docs/readme-update` | 文档更新 |
| 测试 | `test/` | `test/edge-cases` | 添加测试 |

### 分支生命周期

```bash
# 创建分支
git checkout -b feature/xxx

# 开发和提交
# ... 多次提交 ...

# 合并到 main
git checkout main
git merge feature/xxx --no-ff

# 删除已合并分支
git branch -d feature/xxx
```

### 合并策略

- **使用 `--no-ff`**：保留分支历史，便于回滚
- **避免 rebase**：对于已推送的分支，不要 rebase
- **保持历史清晰**：每个分支完成一个独立功能

## 代码规范

### 文件结构
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模块级文档字符串（中文）
"""

import os
import random
from enum import Enum


class MyClass:
    """类文档字符串"""

    def method_name(self, param):
        """
        方法文档字符串

        Args:
            param: 参数说明

        Returns:
            type: 返回值说明
        """
        pass
```

### 命名约定
- **类名**：PascalCase（`Minesweeper`、`CellState`）
- **函数/方法**：snake_case（`reveal_cell`、`toggle_flag`）
- **变量**：snake_case（`first_move`、`mines_placed`）
- **常量**：UPPER_SNAKE_CASE（`SUPPORTS_COLOR`）
- **枚举成员**：UPPER_SNAKE_CASE（`HIDDEN`、`REVEALED`）

### 格式化
- **缩进**：4 空格（不使用制表符）
- **行宽**：最多 120 字符
- **空行**：类方法之间空一行，类定义前空两行
- **注释**：使用中文，简洁明了

### 文档
- **文档字符串**：必须包含 Args/Returns 部分（中文）
- **注释**：解释复杂逻辑，不重复代码
- **README**：更新新增功能和改动说明

## 提交规范

### Conventional Commits 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型（type）

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(game): 添加计时器功能` |
| `fix` | Bug 修复 | `fix(game): 修复首次点击保护失效` |
| `docs` | 文档更新 | `docs(readme): 更新安装说明` |
| `style` | 代码格式 | `style: 修复缩进问题` |
| `refactor` | 重构 | `refactor(core): 简化地雷放置逻辑` |
| `perf` | 性能优化 | `perf(grid): 优化邻居查找算法` |
| `test` | 测试相关 | `test(game): 添加边界测试` |
| `chore` | 构建/工具 | `chore(deps): 更新依赖版本` |
| `ci` | CI/CD | `ci(github): 添加自动化测试` |

### 范围（scope）

常用范围：
- `game`：游戏核心逻辑
- `ui`：用户界面
- `docs`：文档
- `build`：构建工具
- `config`：配置文件

### 示例

```bash
# 新功能
git commit -m "feat(game): 添加计时器功能

新增游戏计时器，实时显示已用时间"

# Bug 修复
git commit -m "fix(ui): 修复颜色显示异常

解决终端颜色支持检测失败的问题"

# 文档更新
git commit -m "docs(readme): 更新游戏规则说明

补充关于标记功能的详细说明"

# 关联 JIRA
git commit -m "fix(core): 修复内存泄漏问题

JIRA: MQC-123"
```

## Pull Request 流程

### 创建 PR

1. **推送到远端**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **在 GitHub 创建 Pull Request**
   - 标题：遵循 Conventional Commits 格式
   - 描述：填写 PR 模板内容
   - 关联 Issue：`Closes #123`

3. **等待代码审查**（如有团队）

4. **合并到 main**
   - 使用 `Squash and merge` 保持历史整洁
   - 或使用 `Merge commit` 保留分支历史

### PR 模板

创建 PR 时会自动显示模板，需要填写：
- 变更类型
- 变更说明
- 测试清单
- 相关 Issue

### PR 检查清单

在提交 PR 前，请确认：
- [ ] 代码已通过本地测试
- [ ] 遵循 AGENTS.md 中的代码规范
- [ ] 文档已同步更新
- [ ] 提交信息符合规范
- [ ] 如涉及游戏逻辑，已充分测试
- [ ] PR 描述清晰完整

## 测试要求

### 手动测试流程

#### 基础版本测试
```bash
# 1. 运行基础版本
cd minesweeper-game/src
python3 minesweeper.py

# 2. 测试基本功能
# - 首次点击
# - 揭开格子
# - 标记地雷
# - 胜利/失败场景
# - 重新开始
# - 退出游戏
```

#### 彩色版本测试
```bash
# 1. 运行彩色版本
cd minesweeper-game/src
python3 minesweeper_color.py

# 2. 测试颜色显示
# - 数字颜色正确
# - 状态颜色正确
# - 提示信息清晰

# 3. 测试所有功能
# - 基本功能同基础版本
# - 颜色显示正常
```

#### 特定场景测试

根据变更内容，测试特定场景：
```bash
# 示例：测试地雷随机化
for i in {1..10}; do
    echo "测试轮次 $i"
    python3 minesweeper_color.py
done
```

### 测试清单

- [ ] 游戏正常启动
- [ ] 首次点击保护生效
- [ ] 地雷放置正确
- [ ] 数字显示准确
- [ ] 递归展开正常
- [ ] 标记功能正常
- [ ] 胜利/失败判断正确
- [ ] 重新开始功能正常
- [ ] 退出功能正常
- [ ] 无中文乱码（Windows）
- [ ] 颜色显示正常（彩色版）
- [ ] 输入验证正确
- [ ] 错误处理友好

## 其他

### 报告问题

如果发现 bug 或有建议：
1. 在 GitHub 创建 Issue
2. 清晰描述问题或建议
3. 提供复现步骤（如适用）
4. 附上截图或日志（如适用）

### 获取帮助

- 查看 [AGENTS.md](../AGENTS.md) 了解代码规范
- 查看 [VERSION_MANAGEMENT.md](../VERSION_MANAGEMENT.md) 了解版本管理
- 查看 [README.md](../README.md) 了解项目概况

---

感谢你的贡献！🎉
