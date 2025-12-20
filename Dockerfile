FROM python:3.11-slim

WORKDIR /app

# 复制项目文件
COPY pyproject.toml .
COPY app/ ./app/
COPY config.py .
COPY run.py .
COPY reset_database.py .
COPY docker-init.py .
COPY add-sample-data.py .

# 安装Python依赖（使用纯Python驱动）
RUN pip install --no-cache-dir -e .

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 5000

CMD ["python", "run.py"]