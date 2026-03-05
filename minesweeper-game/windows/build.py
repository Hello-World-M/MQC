#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
扫雷游戏打包脚本
用于生成Windows可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller安装成功!")
        return True
    except subprocess.CalledProcessError:
        print("PyInstaller安装失败!")
        return False

def create_spec_file():
    """创建PyInstaller规格文件"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['minesweeper_color.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='扫雷游戏',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=' minesweeper.ico' if os.path.exists(' minesweeper.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='扫雷游戏',
)
'''
    
    with open('minesweeper.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("已创建minesweeper.spec文件")

def create_windows_batch_file():
    """创建Windows批处理启动脚本"""
    batch_content = '''@echo off
chcp 65001 >nul
title Minesweeper Game

echo ================================
echo       Minesweeper Game
echo ================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not detected!
    echo.
    echo Please install Python 3.11 or higher
    echo Download: https://www.python.org/downloads/
    echo.
    echo Note: Check "Add Python to PATH" during installation
    pause
    exit /b 1
)

:: 检查Python版本是否符合要求
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [Info] Python version detected: %PYTHON_VERSION%

:: 运行游戏
echo.
echo [Info] Starting game...
python minesweeper_color.py

if errorlevel 1 (
    echo.
    echo [Error] Game execution failed, please check error messages
    pause
)
'''

    with open('start_game.bat', 'w', encoding='gbk') as f:
        f.write(batch_content)

    print("已创建 start_game.bat 启动脚本")

def create_requirements_txt():
    """创建requirements.txt文件"""
    requirements = "# 扫雷游戏依赖项\n# 基础版本只需要Python标准库\n# 打包时需要:\npyinstaller>=5.0.0"
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("已创建requirements.txt文件")

def create_readme():
    """创建Windows用户指南"""
    readme_content = '''# 扫雷游戏 - Windows版本

一个经典的5x5扫雷游戏，使用Python开发，已优化支持Windows系统。

## 功能特点

- 5x5游戏网格，包含5个地雷
- 彩色界面，数字用不同颜色标识
- 第一次点击保护（确保首次点击及周围没有地雷）
- 自动展开空白区域
- 地雷标记功能
- 游戏状态显示（剩余地雷数、游戏进度）

## 安装方法

### 方法一：使用批处理文件（推荐）

1. 双击运行 `扫雷游戏.bat`
2. 如果系统提示缺少Python，请先安装Python 3.11或更高版本
   - 下载地址：https://www.python.org/downloads/
   - 安装时请勾选"Add Python to PATH"

### 方法二：直接运行Python文件

1. 确保已安装Python 3.11或更高版本
2. 在命令行中运行：`python minesweeper_color.py`

### 方法三：使用可执行文件（如已生成）

1. 如果已生成exe文件，直接双击 `扫雷游戏.exe` 运行
2. 无需安装Python环境

## 游戏规则

1. 输入坐标来揭开格子，格式: 行列 (例如: 12 表示第1行第2列)
2. 输入 f + 坐标来标记地雷，格式: f 行列 (例如: f12)
3. 输入 r 重新开始，输入 q 退出游戏
4. 数字表示周围地雷的数量
5. 揭开所有非地雷格子即可获胜
6. 点到地雷则游戏失败

## 操作示例

```
请输入操作: 12    # 揭开第1行第2列
请输入操作: f03   # 标记第0行第3列为地雷
请输入操作: r     # 重新开始游戏
请输入操作: q     # 退出游戏
```

## 技术支持

- 兼容Windows 7及以上版本
- 支持Windows CMD和PowerShell
- 支持现代Windows终端的颜色显示
- 已处理跨平台兼容性问题

## 开发信息

- 开发语言：Python 3.11
- 界面类型：命令行界面(CLI)
- 跨平台：支持Windows/Linux/macOS
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("已创建README.md用户指南")

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    try:
        # 使用--onefile参数生成单个exe文件
        # 使用--windowed参数隐藏控制台窗口（如需GUI版本）
        # 使用--icon参数添加图标（如果有图标文件）
        cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--name", "minesweeper", "minesweeper_color.py"]
        subprocess.check_call(cmd)
        print("可执行文件构建成功!")
        print("可执行文件位置: dist/minesweeper.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"可执行文件构建失败: {e}")
        return False

def main():
    """主函数"""
    print("扫雷游戏Windows移植工具")
    print("========================")
    print()
    
    # 创建必要文件
    create_spec_file()
    create_windows_batch_file()
    create_requirements_txt()
    create_readme()
    
    # 询问是否安装PyInstaller
    install_choice = input("是否安装PyInstaller用于构建可执行文件? (y/n): ").lower()
    if install_choice == 'y':
        if install_pyinstaller():
            # 询问是否构建可执行文件
            build_choice = input("是否构建Windows可执行文件? (y/n): ").lower()
            if build_choice == 'y':
                build_executable()
    
    print()
    print("Windows移植准备完成!")
    print("文件列表:")
    print("- minesweeper.py: 基础版本")
    print("- minesweeper_color.py: 彩色版本")
    print("- start_game.bat: Windows批处理启动脚本")
    print("- README.md: 用户指南")
    print("- requirements.txt: 依赖项列表")

if __name__ == "__main__":
    main()