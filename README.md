# E-Commerce Platform

基于 Flask + MySQL + Redis 的现代化电商平台，支持容器化部署。

## 系统要求

- Python 3.8+
- MySQL 8.0+
- Redis 7.0+
- Docker & Docker Compose (可选)

## 核心功能

- **用户管理**: 注册、登录、会话管理
- **商品系统**: 商品展示、分类、搜索
- **购物车**: 商品添加、数量管理、持久化存储
- **订单管理**: 订单创建、状态跟踪、历史记录
- **管理后台**: 商品管理、用户管理、订单处理
- **缓存优化**: Redis 缓存提升性能

## 技术架构

| 组件 | 技术栈 | 版本 |
|------|--------|------|
| Web框架 | Flask | 3.0.0 |
| ORM | SQLAlchemy | 3.1.1 |
| 数据库 | MySQL | 8.0 |
| 缓存 | Redis | 7.0 |
| 认证 | Flask-Login | 0.6.3 |
| 数据库驱动 | PyMySQL | latest |

## 快速开始

### 方式一：Docker Compose (推荐)

```bash
# 1. 启动所有服务
docker-compose up -d

# 2. 初始化数据库和示例数据
docker-compose exec app python docker-init.py

# 3. 访问应用
# http://localhost:5000
```

### 方式二：本地开发

```bash
# 1. 安装依赖
pip install -e .

# 2. 配置环境变量 (可选)
export DATABASE_URL="mysql+pymysql://root:password@localhost:3306/ecommerce"
export REDIS_URL="redis://localhost:6379/0"
export SECRET_KEY="your-secret-key"

# 3. 初始化数据库
python reset_database.py

# 4. 启动应用
python run.py
```

## 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `DATABASE_URL` | `mysql+pymysql://root:123456@localhost:3306/ecommerce` | MySQL连接字符串 |
| `REDIS_URL` | `redis://127.0.0.1:6379/0` | Redis连接字符串 |
| `SECRET_KEY` | `your-secret-key-here` | Flask会话密钥 |
| `FLASK_ENV` | `development` | Flask运行环境 |

### 数据库配置

修改 `config.py` 或设置环境变量来配置数据库连接。

## 部署指南

### 生产环境部署

```bash
# 使用生产配置
docker-compose -f docker-compose.prod.yml up -d
```

### 单独构建镜像

```bash
# 构建应用镜像
docker build -t ecommerce-platform:latest .

# 运行容器
docker run -d \
  -p 5000:5000 \
  -e DATABASE_URL="mysql+pymysql://user:pass@host:3306/db" \
  -e REDIS_URL="redis://host:6379/0" \
  ecommerce-platform:latest
```

## 开发指南

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 代码质量检查

```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 类型检查
mypy .
```

### 运行测试

```bash
pytest
```

## 项目结构

```
ecommerce-platform/
├── app/                    # 应用核心代码
│   ├── models/            # 数据模型
│   │   └── __init__.py
│   ├── routes/            # 路由控制器
│   │   ├── admin.py       # 管理后台路由
│   │   ├── auth.py        # 认证路由
│   │   └── main.py        # 主要业务路由
│   ├── static/css/        # 静态资源
│   │   └── style.css
│   ├── templates/         # HTML模板
│   │   ├── admin/         # 管理后台模板
│   │   └── *.html         # 用户界面模板
│   ├── __init__.py        # 应用工厂
│   └── redis_client.py    # Redis客户端
├── scripts/               # 辅助脚本
├── instance/              # 实例配置
├── config.py              # 配置文件
├── run.py                 # 应用入口
├── docker-init.py         # Docker初始化脚本
├── reset_database.py      # 数据库重置脚本
├── add-sample-data.py     # 示例数据脚本
├── pyproject.toml         # 项目配置
├── requirements.txt       # 依赖列表
├── Dockerfile             # Docker镜像构建
├── docker-compose.yml     # 开发环境编排
└── docker-compose.prod.yml # 生产环境编排
```

## 默认账户

- **管理员**: `admin` / `admin123`
- **测试用户**: 通过注册页面创建

## 端口说明

- **应用服务**: 5000
- **MySQL**: 3307 (映射到容器内3306)
- **Redis**: 6379 (容器内部)

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务状态
   - 验证连接字符串和凭据

2. **Redis连接失败**
   - 确认Redis服务运行
   - 检查防火墙设置

3. **Docker构建失败**
   - 清理Docker缓存: `docker system prune`
   - 检查Dockerfile语法

### 日志查看

```bash
# 查看应用日志
docker-compose logs app

# 查看数据库日志
docker-compose logs mysql

# 实时日志
docker-compose logs -f
```

## 许可证

MIT License - 详见 LICENSE 文件