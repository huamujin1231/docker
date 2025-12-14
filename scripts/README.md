# Docker 启动脚本使用说明

这个目录包含了多种启动脚本，适用于不同的操作系统和使用习惯。

## 脚本说明

### 1. Windows 批处理脚本
**文件**: `docker-start.bat`
**适用**: Windows 系统
**使用方法**:
```cmd
# 双击运行或在命令行中执行
scripts\docker-start.bat
```

### 2. Linux/Mac Shell 脚本
**文件**: `docker-start.sh`
**适用**: Linux/Mac 系统
**使用方法**:
```bash
# 添加执行权限
chmod +x scripts/docker-start.sh

# 运行脚本
./scripts/docker-start.sh
```

### 3. Python 跨平台脚本 (推荐)
**文件**: `quick-start.py`
**适用**: 所有系统 (需要Python 3.6+)
**使用方法**:
```bash
# 直接运行
python scripts/quick-start.py

# 或者
python3 scripts/quick-start.py
```

### 4. Makefile (Linux/Mac)
**文件**: `Makefile`
**适用**: Linux/Mac 系统 (需要make工具)
**使用方法**:
```bash
# 查看所有命令
make help

# 启动项目
make start

# 构建并启动
make build

# 停止项目
make stop

# 查看日志
make logs

# 初始化数据库
make init
```

## 功能对比

| 功能 | Windows批处理 | Shell脚本 | Python脚本 | Makefile |
|------|---------------|-----------|------------|----------|
| 跨平台 | ❌ | ❌ | ✅ | ❌ |
| 彩色输出 | ❌ | ✅ | ✅ | ❌ |
| 交互菜单 | ✅ | ✅ | ✅ | ❌ |
| 简洁命令 | ❌ | ❌ | ❌ | ✅ |
| 环境检查 | ❌ | ❌ | ✅ | ❌ |

## 推荐使用

1. **日常开发**: 使用 `quick-start.py` (跨平台，功能完整)
2. **快速操作**: 使用 `Makefile` (Linux/Mac，命令简洁)
3. **Windows用户**: 使用 `docker-start.bat`
4. **Linux/Mac用户**: 使用 `docker-start.sh`

## 复制到新项目

将整个 `scripts` 目录复制到新项目根目录即可使用。

需要修改的配置:
- `quick-start.py` 中的 `app_port` 和 `init_script`
- `Makefile` 中的端口号
- 其他脚本中的端口号和初始化脚本名称

## 常用命令速查

```bash
# Python脚本 (推荐)
python scripts/quick-start.py

# Makefile (Linux/Mac)
make start      # 启动
make build      # 构建启动
make stop       # 停止
make logs       # 查看日志
make init       # 初始化数据库

# 直接使用 docker-compose
docker-compose up -d                    # 启动
docker-compose up --build -d           # 构建启动
docker-compose down                     # 停止
docker-compose logs -f                  # 查看日志
docker-compose exec app python docker-init.py  # 初始化数据库
```