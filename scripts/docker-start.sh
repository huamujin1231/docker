#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目配置
PROJECT_NAME="Docker项目"
APP_PORT="5000"
INIT_SCRIPT="docker-init.py"

show_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}    $PROJECT_NAME 启动脚本${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
}

show_menu() {
    echo "请选择操作:"
    echo "[1] 启动项目 (构建+运行)"
    echo "[2] 重新构建并启动"
    echo "[3] 停止项目"
    echo "[4] 查看运行状态"
    echo "[5] 查看日志"
    echo "[6] 初始化数据库"
    echo "[7] 进入应用容器"
    echo "[8] 清理所有容器和镜像"
    echo "[0] 退出"
    echo
}

start_project() {
    echo -e "${YELLOW}启动项目...${NC}"
    if docker-compose up -d; then
        echo -e "${GREEN}✓ 项目启动成功！${NC}"
        echo -e "${GREEN}访问地址: http://localhost:$APP_PORT${NC}"
    else
        echo -e "${RED}✗ 启动失败${NC}"
    fi
}

rebuild_project() {
    echo -e "${YELLOW}重新构建并启动...${NC}"
    if docker-compose up --build -d; then
        echo -e "${GREEN}✓ 重新构建成功！${NC}"
        echo -e "${GREEN}访问地址: http://localhost:$APP_PORT${NC}"
    else
        echo -e "${RED}✗ 构建失败${NC}"
    fi
}

stop_project() {
    echo -e "${YELLOW}停止项目...${NC}"
    docker-compose down
    echo -e "${GREEN}✓ 项目已停止${NC}"
}

show_status() {
    echo -e "${YELLOW}查看运行状态...${NC}"
    docker-compose ps
}

show_logs() {
    echo -e "${YELLOW}查看日志 (按 Ctrl+C 退出)...${NC}"
    docker-compose logs -f
}

init_database() {
    echo -e "${YELLOW}初始化数据库...${NC}"
    if docker-compose exec app python $INIT_SCRIPT; then
        echo -e "${GREEN}✓ 数据库初始化成功${NC}"
    else
        echo -e "${RED}✗ 数据库初始化失败${NC}"
    fi
}

enter_shell() {
    echo -e "${YELLOW}进入应用容器...${NC}"
    docker-compose exec app bash
}

cleanup_all() {
    echo -e "${RED}警告: 这将删除所有相关的容器、镜像和数据卷！${NC}"
    read -p "确认删除? (y/N): " confirm
    if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
        docker-compose down -v --rmi all
        echo -e "${GREEN}✓ 清理完成${NC}"
    else
        echo "取消清理"
    fi
}

main() {
    show_header
    
    while true; do
        show_menu
        read -p "请输入选项 (0-8): " choice
        
        case $choice in
            1) start_project ;;
            2) rebuild_project ;;
            3) stop_project ;;
            4) show_status ;;
            5) show_logs ;;
            6) init_database ;;
            7) enter_shell ;;
            8) cleanup_all ;;
            0) echo "再见！"; exit 0 ;;
            *) echo -e "${RED}无效选项，请重新选择${NC}" ;;
        esac
        
        echo
        read -p "按回车键继续..."
        echo
    done
}

main