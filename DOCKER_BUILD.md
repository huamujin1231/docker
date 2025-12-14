# Docker 多架构镜像构建和发布指南

## 概述

本指南介绍如何构建和发布支持多架构（AMD64 和 ARM64）的 Docker 镜像。

## 前置要求

1. **Docker Desktop** 或 **Docker Engine** (20.10+)
2. **Docker Buildx** 插件
3. **Docker Hub** 账号

## 1. 启用 Docker Buildx

```bash
# 检查 buildx 是否可用
docker buildx version

# 创建新的 builder 实例
docker buildx create --name multiarch-builder --use

# 启动 builder
docker buildx inspect --bootstrap
```

## 2. 登录 Docker Hub

```bash
docker login
# 输入用户名和密码
```

## 3. 构建多架构镜像

### 方法一：直接构建并推送

```bash
# 构建并推送多架构镜像
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag your-username/ecommerce-app:latest \
  --tag your-username/ecommerce-app:v1.0.0 \
  --push .
```

### 方法二：使用 Makefile（推荐）

创建 `Makefile.docker`：

```makefile
# Docker 镜像构建配置
DOCKER_USERNAME ?= your-username
IMAGE_NAME = ecommerce-app
VERSION ?= latest
PLATFORMS = linux/amd64,linux/arm64

.PHONY: build-multi push-multi build-local

# 构建多架构镜像并推送
build-multi:
	docker buildx build \
		--platform $(PLATFORMS) \
		--tag $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION) \
		--tag $(DOCKER_USERNAME)/$(IMAGE_NAME):latest \
		--push .

# 仅构建本地架构（用于测试）
build-local:
	docker build -t $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION) .

# 推送已构建的镜像
push:
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):latest

# 清理 builder
clean:
	docker buildx rm multiarch-builder
```

使用方法：
```bash
# 设置你的 Docker Hub 用户名
export DOCKER_USERNAME=your-username

# 构建并推送多架构镜像
make -f Makefile.docker build-multi

# 或指定版本
make -f Makefile.docker build-multi VERSION=v1.0.0
```

## 4. 使用 GitHub Actions 自动构建

创建 `.github/workflows/docker-build.yml`：

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: your-username/ecommerce-app

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Docker Hub
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## 5. 验证多架构镜像

```bash
# 检查镜像支持的架构
docker buildx imagetools inspect your-username/ecommerce-app:latest

# 输出示例：
# Name:      docker.io/your-username/ecommerce-app:latest
# MediaType: application/vnd.docker.distribution.manifest.list.v2+json
# Digest:    sha256:abc123...
# 
# Manifests:
#   Name:      docker.io/your-username/ecommerce-app:latest@sha256:def456...
#   MediaType: application/vnd.docker.distribution.manifest.v2+json
#   Platform:  linux/amd64
# 
#   Name:      docker.io/your-username/ecommerce-app:latest@sha256:ghi789...
#   MediaType: application/vnd.docker.distribution.manifest.v2+json
#   Platform:  linux/arm64
```

## 6. 测试不同架构

```bash
# 在 AMD64 系统上测试 ARM64 镜像
docker run --platform linux/arm64 your-username/ecommerce-app:latest

# 在 ARM64 系统上测试 AMD64 镜像
docker run --platform linux/amd64 your-username/ecommerce-app:latest
```

## 7. 优化 Dockerfile 以支持多架构

```dockerfile
# 使用多阶段构建优化镜像大小
FROM python:3.11-slim as base

# 设置架构相关的变量
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "Building on $BUILDPLATFORM, targeting $TARGETPLATFORM"

WORKDIR /app

# 复制依赖文件
COPY pyproject.toml .

# 安装依赖
RUN pip install --no-cache-dir -e .

# 生产阶段
FROM base as production

# 复制应用代码
COPY app/ ./app/
COPY config.py run.py docker-init.py add-sample-data.py ./

# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 5000
CMD ["python", "run.py"]
```

## 8. 常用命令速查

```bash
# 创建 builder
docker buildx create --name multiarch --use

# 构建多架构镜像
docker buildx build --platform linux/amd64,linux/arm64 -t username/app:tag --push .

# 检查镜像架构
docker buildx imagetools inspect username/app:tag

# 删除 builder
docker buildx rm multiarch

# 查看可用平台
docker buildx ls
```

## 9. 故障排查

### 构建失败
```bash
# 查看详细日志
docker buildx build --platform linux/amd64,linux/arm64 -t username/app:tag --push . --progress=plain

# 单独构建每个架构
docker buildx build --platform linux/amd64 -t username/app:amd64 --load .
docker buildx build --platform linux/arm64 -t username/app:arm64 --load .
```

### 推送失败
```bash
# 检查登录状态
docker info | grep Username

# 重新登录
docker logout
docker login
```

## 10. 最佳实践

1. **使用标签管理版本**：
   ```bash
   docker buildx build \
     --platform linux/amd64,linux/arm64 \
     --tag username/app:latest \
     --tag username/app:v1.0.0 \
     --tag username/app:stable \
     --push .
   ```

2. **利用缓存加速构建**：
   ```bash
   docker buildx build \
     --platform linux/amd64,linux/arm64 \
     --cache-from type=registry,ref=username/app:cache \
     --cache-to type=registry,ref=username/app:cache,mode=max \
     --push .
   ```

3. **使用 .dockerignore 减少构建上下文**：
   ```
   .git
   .github
   node_modules
   __pycache__
   *.pyc
   .env
   README.md
   ```

这样就可以构建和发布支持多架构的 Docker 镜像了！