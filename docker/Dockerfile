FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY src/ ./src/
COPY pyproject.toml .

# 创建数据目录
RUN mkdir -p /app/data /app/config

# 设置环境变量
ENV PYTHONPATH=/app
ENV AUTOSIGNIN_DEBUG=false

# 默认命令
CMD ["python", "-m", "src.cli.main", "signin", "--all"]
