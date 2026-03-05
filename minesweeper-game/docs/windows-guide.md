# Windows用户指南

本指南为Windows用户提供了扫雷游戏的详细安装和运行说明，包括多种便捷的启动方式和特定于Windows的优化功能。

## 🚀 Windows快速启动方式

### 方法一：一键启动脚本（推荐）

使用提供的批处理文件快速启动游戏：

1. 双击运行 `scripts/start_game.bat` 文件
2. 根据提示选择版本：
   - 选择1：彩色命令行版本
   - 选择2：基础命令行版本
   - 选择3：Web版本（浏览器）
   - 选择4：生成Windows可执行文件

### 方法二：使用可执行文件

如果已生成exe文件，直接双击运行：
```
dist/minesweeper.exe
```

### 方法三：直接运行Python文件

1. 确保已安装Python 3.11或更高版本
2. 打开命令提示符(CMD)或PowerShell
3. 切换到游戏目录并运行：

   ```cmd
   # 彩色版本（推荐）
   python src/minesweeper_color.py
   
   # 基础版本
   python src/minesweeper.py
   ```

## 💻 Windows系统特定优化

### 终端兼容性

游戏已针对Windows环境进行了以下优化：

- **自动检测Windows系统**：程序启动时自动识别Windows环境
- **CMD和PowerShell支持**：完全兼容Windows的两种主要命令行环境
- **中文字符编码**：正确处理Windows下的中文字符显示
- **颜色显示优化**：通过ctypes启用ANSI颜色支持

### 终端选择建议

1. **Windows Terminal**（推荐）
   - 最佳的颜色支持
   - UTF-8编码完美支持
   - 现代化的界面体验

2. **PowerShell**
   - 良好的颜色支持
   - 内置于Windows 10/11

3. **命令提示符(CMD)**
   - 基本兼容性
   - 适合老旧系统

## 🔧 构建Windows可执行文件

### 自动构建

1. 运行 `scripts/start_game.bat`
2. 选择选项4："生成Windows可执行文件"
3. 等待构建完成

### 手动构建

1. 打开命令提示符或PowerShell
2. 运行构建脚本：

   ```cmd
   python scripts/build.py
   ```

3. 构建完成后，可执行文件将位于 `dist/minesweeper.exe`

### 构建要求

- Python 3.11+
- 稳定的网络连接（用于下载PyInstaller依赖）
- 约50MB的可用磁盘空间

## 📁 Windows文件结构

```
minesweeper-game/
├── src/                       # Python源代码
│   ├── minesweeper.py         # 基础版本
│   └── minesweeper_color.py   # 彩色版本
├── web/                       # Web版本
│   └── minesweeper_web.html   # 浏览器版本
├── scripts/                   # Windows脚本
│   ├── start_game.bat         # 一键启动脚本
│   └── build.py               # 构建脚本
├── dist/                      # 构建输出（生成后）
│   └── minesweeper.exe       # Windows可执行文件
└── docs/                      # 文档
    └── windows-guide.md       # 本指南
```

## 🐛 Windows特定故障排除

### 中文显示问题

**问题**：运行时显示中文乱码

**解决方案**：
1. 使用提供的批处理文件启动
2. 在Windows Terminal或PowerShell中运行
3. 手动设置代码页：

   ```cmd
   chcp 65001
   python src/minesweeper_color.py
   ```

### 颜色显示问题

**问题**：颜色显示不正常或无颜色

**解决方案**：
1. 使用Windows Terminal（推荐）
2. 尝试基础版本（无颜色）：
   ```cmd
   python src/minesweeper.py
   ```
3. 在CMD中启用虚拟终端：
   ```cmd
   python src/minesweeper_color.py
   ```

### Python安装问题

**问题**：提示"python不是内部或外部命令"

**解决方案**：
1. 从 [python.org](https://www.python.org/downloads/) 下载Python 3.11+
2. 安装时勾选"Add Python to PATH"选项
3. 重新启动命令提示符

### 构建失败问题

**问题**：无法生成exe文件

**解决方案**：
1. 检查网络连接
2. 更新pip：
   ```cmd
   python -m pip install --upgrade pip
   ```
3. 手动安装PyInstaller：
   ```cmd
   pip install pyinstaller
   ```

## 🎮 Windows特定功能

### 批处理启动脚本特性

- **环境检测**：自动检测Python安装
- **版本选择**：交互式选择游戏版本
- **错误处理**：友好的错误提示
- **编码设置**：自动设置正确的代码页

### 可执行文件特性

- **独立运行**：无需安装Python
- **便携性**：可复制到其他Windows电脑
- **小体积**：打包后的文件约15-20MB
- **快速启动**：秒级启动时间

## 📊 性能优化建议

### 提升游戏体验

1. **使用SSD硬盘**：加快启动速度
2. **关闭杀毒软件实时扫描**：避免游戏卡顿
3. **使用现代终端**：获得最佳显示效果
4. **调整终端字体**：使用等宽字体如Consolas

### 系统要求细节

- **操作系统**：Windows 7 SP1或更高版本
- **内存**：最少512MB可用内存
- **硬盘**：至少50MB可用空间（包含构建文件）
- **处理器**：任何现代处理器

## 🔗 相关链接

- [Python官方下载](https://www.python.org/downloads/)
- [Windows Terminal下载](https://aka.ms/terminal)
- [项目主页](../README.md)

---

**需要更多帮助？**

如果遇到其他问题，可以：
1. 查看项目主README文档
2. 尝试使用Web版本作为替代方案
3. 检查系统是否满足最低要求