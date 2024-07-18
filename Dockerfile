# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 维护者信息
LABEL maintainer="yourname@example.com"

# 设置环境变量以避免交互式安装提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装必要的系统依赖和 Jupyter Notebook
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY . .

# 安装项目依赖和 Jupyter Notebook
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install jupyter

# 设置 Jupyter Notebook 配置
RUN mkdir -p ~/.jupyter && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py

# 暴露 Jupyter Notebook 端口
EXPOSE 3000

# 启动 Jupyter Notebook
CMD ["reflex", "run"]