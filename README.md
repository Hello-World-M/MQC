# MQC
毛庆灿的代码仓库

## 📋 项目信息

- **项目类型**: 扫雷游戏（Python + Web）
- **开发语言**: Python 3.11+, JavaScript
- **版本**: v0.3.0
- **许可证**: MIT

## 🚀 快速开始

```bash
# 运行游戏
cd minesweeper-game/src
python3 minesweeper_color.py

# 查看文档
cat CONTRIBUTING.md    # 贡献指南
cat AGENTS.md        # 代码规范
cat VERSION_MANAGEMENT.md # 版本管理
```

## 📦 主要项目

### 扫雷游戏
一个使用 Python 3.11 开发的经典扫雷游戏，提供命令行和 Web 两种版本，支持 Windows/Linux/macOS。

#### Python 版本（命令行）
- 5x5 网格，地雷数量随机（3-5 个）
- 彩色命令行界面
- 第一次点击保护
- 自动展开空白区域
- 支持地雷标记
- **倒计时挑战**：4 个难度级别（简单 15 分钟、困难 10 分钟、极限 5 分钟、自定义）
- 实时显示剩余时间（动态颜色：绿→黄→红）
- 超时自动判定为失败
- 重新开始功能
- 跨平台兼容

#### Web 版本（浏览器）
- 完全同步 Python 版本的所有功能
- **双重难度系统**：
  - 时间挑战模式：简单/困难/极限/自定义（倒计时）
  - 网格挑战模式：初级(5x5)/中级(8x8)/高级(10x10)
- 动态剩余时间显示（绿→橙→红）
- 超时自动判定
- 一键切换模式
- 美观的渐变背景和响应式设计
- 支持左键揭开、右键标记

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解：
- 开发流程
- 分支策略
- 代码规范
- 提交规范
- Pull Request 流程

## 📄 文档

- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- [AGENTS.md](AGENTS.md) - AI 编码助手指南
- [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) - 版本管理指南

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👤 作者

毛庆灿
