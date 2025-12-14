@echo off
chcp 65001 >nul
echo ================================
echo    Docker 项目启动脚本
echo ================================
echo.

:menu
echo 请选择操作:
echo [1] 启动项目 (构建+运行)
echo [2] 重新构建并启动
echo [3] 停止项目
echo [4] 查看运行状态
echo [5] 查看日志
echo [6] 初始化数据库
echo [7] 进入应用容器
echo [8] 清理所有容器和镜像
echo [0] 退出
echo.
set /p choice=请输入选项 (0-8): 

if "%choice%"=="1" goto start
if "%choice%"=="2" goto rebuild
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto status
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto init_db
if "%choice%"=="7" goto shell
if "%choice%"=="8" goto cleanup
if "%choice%"=="0" goto exit
echo 无效选项，请重新选择
goto menu

:start
echo 启动项目...
docker-compose up -d
if %errorlevel% equ 0 (
    echo ✓ 项目启动成功！
    echo 访问地址: http://localhost:5000
) else (
    echo ✗ 启动失败
)
goto menu

:rebuild
echo 重新构建并启动...
docker-compose up --build -d
if %errorlevel% equ 0 (
    echo ✓ 重新构建成功！
    echo 访问地址: http://localhost:5000
) else (
    echo ✗ 构建失败
)
goto menu

:stop
echo 停止项目...
docker-compose down
echo ✓ 项目已停止
goto menu

:status
echo 查看运行状态...
docker-compose ps
goto menu

:logs
echo 查看日志 (按 Ctrl+C 退出)...
docker-compose logs -f
goto menu

:init_db
echo 初始化数据库...
docker-compose exec app python docker-init.py
if %errorlevel% equ 0 (
    echo ✓ 数据库初始化成功
) else (
    echo ✗ 数据库初始化失败
)
goto menu

:shell
echo 进入应用容器...
docker-compose exec app bash
goto menu

:cleanup
echo 警告: 这将删除所有相关的容器、镜像和数据卷！
set /p confirm=确认删除? (y/N): 
if /i "%confirm%"=="y" (
    docker-compose down -v --rmi all
    echo ✓ 清理完成
) else (
    echo 取消清理
)
goto menu

:exit
echo 再见！
pause