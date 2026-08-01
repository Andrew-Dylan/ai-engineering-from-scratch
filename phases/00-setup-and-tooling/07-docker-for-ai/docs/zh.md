# 用 Docker 进行 AI 开发

> 容器让“在我的机器上能运行”成为过去。

**类型：** Build　**语言：** Docker　**前置知识：** Phase 0，第 01、03 课　**预计时间：** 约 60 分钟

## 学习目标

- 从 Dockerfile 构建包含 CUDA、PyTorch 和 AI 库的 GPU 镜像
- 挂载数据卷，让模型、数据集和代码在重建容器后仍然存在
- 配置 NVIDIA Container Toolkit，把 GPU 暴露给容器
- 使用 Docker Compose 编排推理服务器和向量数据库等服务

镜像是只读模板，容器是镜像的运行实例，Dockerfile 是构建说明，volume 是持久化存储，Compose 用 YAML 定义多容器应用。Docker 共享宿主机内核，但隔离运行时、库和系统工具。

典型容器包括开发容器（编辑器、Jupyter、调试工具）、训练容器（训练脚本和依赖）以及推理容器（小镜像、快速启动）。GPU 容器仍然需要宿主机驱动和 NVIDIA Container Toolkit。

```dockerfile
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install torch
WORKDIR /app
COPY . .
CMD ["python3", "main.py"]
```

使用 `docker build -t ai-app .` 构建，使用 `docker run --gpus all ai-app` 运行。模型和数据应通过 `-v` 挂载，而不是写入临时容器层。
