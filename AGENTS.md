# AGENTS.md

本文件包含在此仓库工作的 AI 编码助手的指南。

## 构建/测试命令

### 运行游戏
```bash
# 基础命令行版本
python3 minesweeper-game/src/minesweeper.py

# 彩色命令行版本（推荐）
python3 minesweeper-game/src/minesweeper_color.py

# Web 版本
# 在浏览器中打开 minesweeper-game/web/minesweeper_web.html
```

### 测试
```bash
# 目前未实现自动化测试
# pytest 被列为开发依赖项，但尚无测试文件
# 需要手动测试：运行游戏并验证功能
```

### 构建可执行文件（Windows）
```bash
# 安装依赖
pip install -r minesweeper-game/windows/requirements.txt

# 构建可执行文件
python minesweeper-game/windows/build.py

# 这将创建：dist/扫雷游戏.exe
```

## 代码风格指南

### 文件结构
- 所有 Python 文件必须以 shebang 开头：`#!/usr/bin/env python3`
- 显式 UTF-8 编码：`# -*- coding: utf-8 -*-`
- 模块级文档字符串描述用途（中文）

### 导入
- 仅使用标准库导入（os、random、sys、enum、pathlib、subprocess、shutil）
- 导入顺序：字母顺序，每行一个
- 核心功能无需外部依赖

### 命名约定
- **类名**：PascalCase（例如：`Minesweeper`、`CellState`、`Colors`）
- **函数/方法**：snake_case（例如：`reveal_cell`、`toggle_flag`）
- **变量**：snake_case（例如：`first_move`、`mines_placed`）
- **常量**：UPPER_SNAKE_CASE（例如：`SUPPORTS_COLOR`）
- **枚举成员**：UPPER_SNAKE_CASE（例如：`HIDDEN`、`REVEALED`、`PLAYING`）

### 类设计
- 使用类来管理游戏状态和逻辑
- 使用 `Enum` 进行状态管理（CellState、GameStatus）
- 私有/内部方法前缀下划线（如适用）
- 公共方法具有全面的文档字符串

### 文档
- 所有类必须有描述用途的文档字符串
- 所有方法必须有包含 Args/Returns 部分的文档字符串（中文）
- 格式：
  ```python
  """
  简要描述此功能的作用

  Args:
      param1: 描述
      param2: 描述

  Returns:
      type: 返回值描述
  """
  ```

### 错误处理
- 对用户输入操作使用 try-except（EOFError 处理）
- 在处理前验证用户输入
- 对无效操作返回 False/None 而非抛出异常
- 向用户提供清晰的错误信息

### 格式化
- 4 空格缩进（不使用制表符）
- 每行最多 120 字符（允许中文文本灵活性）
- 类方法之间空一行
- 类定义前空两行
- 逻辑相关的代码块之间空一行

### 语言和编码
- 所有文档字符串和注释使用中文（与现有代码库匹配）
- 所有文件使用 UTF-8 编码
- 处理跨平台问题（Windows/Linux/macOS）
- 使用 `sys.platform.startswith('win')` 进行 Windows 检测

### 特定模式
- **网格表示**：列表的列表 `[[0 for _ in range(size)] for _ in range(size)]`
- **地雷数量随机化**：`mines=None` 时使用 `random.randint(3, 5)` 生成随机数量
- **首次点击保护**：确保首次点击和周围没有地雷
- **递归展开**：自动展开空白单元格
- **坐标验证**：访问前检查 `0 <= row < size`
- **颜色支持**：使用 ANSI 代码前检查 `sys.stdout.isatty()`

### 项目结构
```
minesweeper-game/
├── src/           # Python 源代码
├── web/           # Web 版本文件
├── docs/          # 文档
└── windows/       # Windows 特定文件
```

### 添加功能时
1. 检查 `minesweeper.py` 和 `minesweeper_color.py` 中是否存在类似功能
2. 保持两个版本的一致性
3. 用中文更新文档字符串
4. 如可能，在多个平台上手动测试
5. 考虑跨平台兼容性（Windows/Linux/macOS）

### 禁止事项
- 不使用类型提示（当前代码库中未使用）
- 核心游戏逻辑不使用外部依赖
- 不使用空 catch 块抑制错误
- 不使用硬编码路径（使用 pathlib 进行文件操作）
