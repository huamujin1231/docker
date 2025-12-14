# 部署说明

## 快速开始

使用以下命令一键部署应用：

```bash
# 1. 下载配置文件
curl -O https://raw.githubusercontent.com/your-repo/ecommerce/main/docker-compose.prod.yml

# 2. 启动服务
docker compose -f docker-compose.prod.yml up -d

# 3. 等待 30 秒，然后初始化数据库
docker compose -f docker-compose.prod.yml exec app python docker-init.py
docker compose -f docker-compose.prod.yml exec app python add-sample-data.py

# 4. 访问 http://localhost:5000
```

## 完整部署步骤

### 1. 拉取镜像

```bash
docker pull huamujin1231/ecommerce-app:latest
docker pull mysql:8.0
docker pull redis:7-alpine
```

### 2. 使用 docker-compose 启动

```bash
docker compose -f docker-compose.prod.yml up -d
```

### 3. 初始化数据库

等待服务启动（约30秒），然后初始化数据库：

```bash
# 创建数据库表结构
docker compose -f docker-compose.prod.yml exec app python docker-init.py

# 添加示例数据（可选）
docker compose -f docker-compose.prod.yml exec app python add-sample-data.py
```

示例数据包括：
- 5个商品分类
- 10个示例商品
- 管理员账号：`admin` / `admin123`

### 4. 访问应用

应用将在 http://localhost:5000 运行

### 5. 查看日志

```bash
docker compose -f docker-compose.prod.yml logs -f app
```

### 6. 停止服务

```bash
docker compose -f docker-compose.prod.yml down
```

## 架构支持

该镜像支持以下架构：
- ✅ linux/amd64 (x86_64)
- ✅ linux/arm64 (ARM64/Apple Silicon)

Docker 会自动拉取适合您系统的镜像。

## 环境变量配置

如需修改配置，可以创建 `.env` 文件：

```env
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://ecommerce:password@mysql:3306/ecommerce
REDIS_URL=redis://redis:6379/0
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=ecommerce
MYSQL_USER=ecommerce
MYSQL_PASSWORD=password
```

然后使用：
```bash
docker compose -f docker-compose.prod.yml --env-file .env up -d
```

## 数据持久化

数据会自动保存在 Docker volumes 中：
- `mysql_data` - MySQL 数据
- `redis_data` - Redis 数据

## 数据库访问

Docker MySQL 映射到本地端口 **3307**，可以使用 Navicat 或其他工具连接：

- **主机**：`localhost`
- **端口**：`3307`
- **用户名**：`ecommerce`
- **密码**：`password`
- **数据库**：`ecommerce`

注意：使用 3307 端口是为了避免与本地 MySQL（端口 3306）冲突。

## 数据库管理

### 重建数据库（删除所有数据）

如果需要完全重置数据库：

```bash
# 1. 停止并删除所有容器和数据卷
docker compose -f docker-compose.prod.yml down -v

# 2. 重新启动服务
docker compose -f docker-compose.prod.yml up -d

# 3. 等待 30 秒后初始化数据库
docker compose -f docker-compose.prod.yml exec app python docker-init.py
docker compose -f docker-compose.prod.yml exec app python add-sample-data.py
```

### 验证数据

```bash
# 查看商品数据
docker compose -f docker-compose.prod.yml exec mysql mysql -uecommerce -ppassword ecommerce -e "SELECT id, name, price FROM products LIMIT 5;"

# 进入 MySQL 控制台
docker compose -f docker-compose.prod.yml exec mysql mysql -uecommerce -ppassword ecommerce
```

## 故障排查

### 应用无法连接数据库
等待 MySQL 完全启动（约 30 秒），然后重启应用：
```bash
docker compose -f docker-compose.prod.yml restart app
```

### 查看所有服务状态
```bash
docker compose -f docker-compose.prod.yml ps
```
