# Docker 项目 Makefile
# 使用方法: make <command>

.PHONY: help start stop restart build logs status shell init clean

# 默认目标
help:
	@echo "Docker 项目管理命令:"
	@echo "  make start    - 启动项目"
	@echo "  make build    - 构建并启动项目"
	@echo "  make stop     - 停止项目"
	@echo "  make restart  - 重启项目"
	@echo "  make logs     - 查看日志"
	@echo "  make status   - 查看状态"
	@echo "  make shell    - 进入应用容器"
	@echo "  make init     - 初始化数据库"
	@echo "  make clean    - 清理容器和镜像"

# 启动项目
start:
	@echo "🚀 启动项目..."
	docker-compose up -d
	@echo "✅ 项目启动完成！访问: http://localhost:5000"

# 构建并启动
build:
	@echo "🔄 构建并启动项目..."
	docker-compose up --build -d
	@echo "✅ 构建完成！访问: http://localhost:5000"

# 停止项目
stop:
	@echo "🛑 停止项目..."
	docker-compose down
	@echo "✅ 项目已停止"

# 重启项目
restart: stop start

# 查看日志
logs:
	@echo "📋 查看日志 (Ctrl+C 退出)..."
	docker-compose logs -f

# 查看状态
status:
	@echo "📊 容器状态:"
	docker-compose ps

# 进入容器
shell:
	@echo "💻 进入应用容器..."
	docker-compose exec app bash

# 初始化数据库
init:
	@echo "🗄️ 初始化数据库..."
	docker-compose exec app python docker-init.py
	@echo "✅ 数据库初始化完成"

# 清理
clean:
	@echo "🧹 清理容器和镜像..."
	docker-compose down -v --rmi all
	@echo "✅ 清理完成"