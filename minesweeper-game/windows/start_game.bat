@echo off
chcp 65001 >nul
title 扫雷游戏 - Windows版

echo ================================
echo       扫雷游戏 Windows版
echo ================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python安装!
    echo.
    echo 请选择安装方式:
    echo 1. 下载并安装Python 3.11或更高版本
    echo    下载地址: https://www.python.org/downloads/
    echo    安装时请勾选 "Add Python to PATH"
    echo.
    echo 2. 或者直接运行Web版本（无需Python）
    echo    双击 minesweeper_web.html 文件
    echo.
    pause
    exit /b 1
)

:: 检查Python版本
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [信息] 检测到Python版本: %PYTHON_VERSION%

echo.
echo 请选择运行版本:
echo 1. 彩色命令行版本 (推荐)
echo 2. 基础命令行版本
echo 3. Web版本 (浏览器)
echo 4. 生成Windows可执行文件
echo.
set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" goto color_version
if "%choice%"=="2" goto basic_version
if "%choice%"=="3" goto web_version
if "%choice%"=="4" goto build_exe

echo [错误] 无效选择，默认运行彩色版本
goto color_version

:color_version
echo.
echo [信息] 正在启动彩色命令行版本...
echo.
python minesweeper_color.py
if errorlevel 1 (
    echo.
    echo [错误] 游戏运行出错，请检查错误信息
    pause
)
goto end

:basic_version
echo.
echo [信息] 正在启动基础命令行版本...
echo.
python minesweeper.py
if errorlevel 1 (
    echo.
    echo [错误] 游戏运行出错，请检查错误信息
    pause
)
goto end

:web_version
echo.
echo [信息] 正在启动Web版本...
echo.
if exist minesweeper_web.html (
    start minesweeper_web.html
    echo [信息] Web版本已在浏览器中打开
) else (
    echo [错误] 找不到 minesweeper_web.html 文件
)
goto end

:build_exe
echo.
echo [信息] 准备生成Windows可执行文件...
echo.

:: 检查是否安装了PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [信息] 正在安装PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller安装失败，请检查网络连接
        pause
        goto end
    )
)

echo [信息] 开始构建可执行文件...
python -m PyInstaller --onefile --name="扫雷游戏" minesweeper_color.py

if exist "dist\扫雷游戏.exe" (
    echo.
    echo [成功] 可执行文件已生成!
    echo 文件位置: %cd%\dist\扫雷游戏.exe
    echo.
    echo 是否立即运行生成的可执行文件? (Y/N)
    set /p run_exe="请选择: "
    if /i "%run_exe%"=="Y" (
        start "" "dist\扫雷游戏.exe"
    )
) else (
    echo [错误] 可执行文件生成失败
    pause
)

:end
echo.
echo 感谢使用扫雷游戏！
pause