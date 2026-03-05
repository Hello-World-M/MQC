# 更新日志

本文档记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

## [0.4.0] - 2026-03-05

### 新增

#### Web 版本
- 添加倒计时模式（15分钟/10分钟/5分钟/自定义）
- 添加超时判定功能（TIMEOUT 状态）
- 实现剩余时间动态颜色显示（绿色>60秒，橙色>30秒，红色≤30秒）
- 添加双重难度系统：
  - **时间挑战模式**：简单/困难/极限/自定义
  - **网格挑战模式**：初级(5x5)/中级(8x8)/高级(10x10)
- 添加模式切换按钮（网格/时间）
- 添加 `get_remaining_time()` 方法
- 添加 `check_timeout()` 方法
- 添加超时状态样式（`.message-timeout`）
- 自定义时间输入提示

#### 文档
- 更新 README.md，添加 Web 版本特性说明
- 更新版本管理指南，添加 v0.4.0 记录
- 创建 CHANGELOG.md

### 变更

#### Web 版本
- 重构难度系统从单一数组改为双重对象结构
- 重构计时器逻辑，支持倒计时和向上计时两种模式
- 更新 `GameStatus` 枚举，添加 `TIMEOUT = 3`
- 更新 `Minesweeper` 构造函数，添加 `timeLimit` 参数
- 更新 `reveal_cell()` 方法，添加超时检查
- 更新 `startTimer()` 方法，实现倒计时和动态颜色
- 更新 `get_status_text()` 方法，添加超时状态文本
- 更新游戏显示逻辑，添加超时状态样式处理

### 修复

#### Web 版本
- 修复计时器逻辑在网格模式下的显示问题

### 技术细节

#### Web 版本改动统计
- 总行数：553 → 690（+137 行）
- 新增方法：2 个
- 修改方法：3 个
- 新增 UI 元素：1 个按钮（切换模式）
- 新增 CSS 样式：1 个

#### 版本同步
- ✅ Python 版本：无需改动（已有完整功能）
- ✅ Windows 版本：无需改动（启动脚本，自动继承 Python 功能）
- ✅ Web 版本：已更新，功能完全同步

## [0.3.0] - 2026-03-05

### 新增
- 添加倒计时挑战模式
- 添加难度选择（简单 15 分钟、困难 10 分钟、极限 5 分钟、自定义）
- 添加剩余时间显示（动态颜色：绿→黄→红）
- 添加超时自动判定功能
- 添加 TIMEOUT 游戏状态

### 变更
- 重构难度系统，使用 Difficulty 枚举
- 更新游戏状态枚举，添加 TIMEOUT
- 添加时间限制相关属性和方法

## [0.2.0] - 2026-03-05

### 新增
- 地雷数量随机化（3-5 个）
- 隐藏地雷数量显示（显示 "???"）
- 添加地雷计数开关（`mines` 参数控制）

### 变更
- 更新游戏显示逻辑，支持隐藏地雷数量
- 更新构造函数，添加 `show_mine_count` 属性

## [0.1.1] - 2026-03-05

### 修复
- 修复 .gitignore 规则，排除批处理文件
- 将 Windows 批处理文件改为英文名称

## [0.1.0] - 2026-03-05

### 新增
- 初始版本的扫雷游戏
- 支持 5x5 网格
- 基础游戏逻辑（揭开、标记、获胜判定）
- 第一次点击保护
- 自动展开空白区域
- 命令行界面
- 跨平台支持（Windows/Linux/macOS）

[未发布]: https://github.com/Hello-World-M/MQC/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/Hello-World-M/MQC/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/Hello-World-M/MQC/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Hello-World-M/MQC/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/Hello-World-M/MQC/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Hello-World-M/MQC/releases/tag/v0.1.0
