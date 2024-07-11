创建一个 Docker 镜像，包含你需要的 Python 包，并配置好 Jupyter Notebook 服务器。以下是一个示例 `Dockerfile` 和运行容器的步骤。

### 示例 `Dockerfile`

```Dockerfile
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
EXPOSE 8888

# 启动 Jupyter Notebook
CMD ["jupyter", "notebook", "--allow-root", "--no-browser", "--ip=0.0.0.0", "--port=8888"]
```

### 步骤

1. **创建 `requirements.txt`**

   请确保你有一个 `requirements.txt` 文件，列出了你的项目所有的依赖。你可以使用以下命令生成它：

   ```sh
   pip freeze > requirements.txt
   ```

2. **创建 `Dockerfile`**

   在你的项目根目录下创建一个名为 `Dockerfile` 的文件，并添加上面的内容。

3. **构建 Docker 镜像**

   在 `Dockerfile` 所在目录下运行以下命令来构建镜像：

   ```sh
   docker build -t my-jupyter-notebook .
   ```

4. **运行 Docker 容器**

   使用构建好的镜像启动一个容器，并将端口 8888 映射到本地：

   ```sh
   docker run -it -p 8888:8888 my-jupyter-notebook
   ```

### 访问 Jupyter Notebook

运行容器后，你可以在浏览器中访问以下 URL 来使用 Jupyter Notebook：

```
http://localhost:8888
```

### 解释

1. **基础镜像**：我们使用 `python:3.9-slim` 作为基础镜像，它是一个轻量级的 Python 镜像。

2. **安装系统依赖和 Jupyter Notebook**：
   - 安装 `build-essential` 和 `curl` 作为系统依赖。
   - 安装 `jupyter` 包。

3. **复制项目文件**：我们将当前目录的所有内容复制到镜像中的 `/app` 目录。

4. **安装依赖**：使用 `pip` 安装项目的依赖和 Jupyter Notebook。

5. **配置 Jupyter Notebook**：设置 Jupyter Notebook 的配置以允许外部访问，并禁用 token 认证。

6. **暴露端口**：暴露 Jupyter Notebook 默认使用的 8888 端口。

7. **启动 Jupyter Notebook**：使用 `CMD` 指令启动 Jupyter Notebook 服务器。

### 使用 Docker Compose（可选）

如果你有更多的服务需要运行，可以使用 Docker Compose 来管理多个容器。以下是一个简单的示例 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  jupyter:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - .:/app
```

使用 Docker Compose 启动服务：

```sh
docker-compose up
```

这样，你就可以在本地浏览器中访问 Jupyter Notebook，并使用 Docker 镜像中的 Python 环境了。