@echo off
chcp 65001 >nul
echo ========================================
echo   欧冶钢材自动搜索工具 - 安装和运行
echo ========================================
echo.

echo [1/3] 安装 Python 依赖...
pip install selenium xlrd --quiet
if %errorlevel% neq 0 (
    echo ❌ pip 安装失败，请检查 Python 是否安装
    pause
    exit /b 1
)
echo ✅ 依赖安装完成

echo.
echo [2/3] 检查 Edge WebDriver...
if not exist "%USERPROFILE%\.hermes\edgedriver\msedgedriver.exe" (
    echo 📥 需要下载 Edge WebDriver
    echo 请手动下载: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    echo 下载后放到: %USERPROFILE%\.hermes\edgedriver\
    mkdir "%USERPROFILE%\.hermes\edgedriver" 2>nul
    echo 文件放好后重新运行此脚本
    pause
    exit /b 1
)
echo ✅ Edge WebDriver 已就绪

echo.
echo [3/3] 运行自动搜索...
python "%~dp0ouyeel_auto_search.py" "%~dp06月期货(1).xls"
pause
