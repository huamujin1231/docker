# 电商平台

基于Flask + MySQL + Redis的完整电商平台

## 功能特性

- 用户注册/登录系统
- 商品浏览和搜索
- 购物车管理
- 订单系统
- 管理员后台
- Redis缓存优化

## 快速启动

1. **安装依赖**
```bash
# 基础依赖
pip install -e .

# 或者开发环境（包含测试和代码质量工具）
pip install -e ".[dev]"
```

2. **配置数据库**
- 修改 `config.py` 中的MySQL密码
- 运行数据库初始化：
```bash
python reset_database.py
```

3. **启动应用**
```bash
python run.py
```

4. **访问应用**
- 应用地址：http://127.0.0.1:5000
- 管理员账号：admin / admin123

## Docker部署

**使用Docker Compose一键部署：**

```bash
# 构建并启动所有服务
docker-compose up -d

# 初始化数据库
docker-compose exec app python docker-init.py

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

**单独构建镜像：**

```bash
# 构建镜像
docker build -t ecommerce-platform .

# 运行容器（需要先启动MySQL和Redis）
docker run -p 5000:5000 ecommerce-platform
```

## 技术栈

- **后端**：Flask + SQLAlchemy
- **数据库**：MySQL 8.0
- **缓存**：Redis
- **前端**：HTML + CSS + JavaScript

## 项目结构

```
ecommerce/
├── app/
│   ├── models/          # 数据库模型
│   ├── routes/          # 路由控制器
│   ├── templates/       # HTML模板
│   └── static/css/      # 样式文件
├── config.py           # 配置文件
├── run.py             # 应用入口
├── init_db.py         # SQLite初始化（备用）
└── reset_database.py  # MySQL数据库重置
```