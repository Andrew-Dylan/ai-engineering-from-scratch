# Python 环境

> 依赖地狱确实存在；虚拟环境是解决办法。

**类型：** Build　**语言：** Shell　**前置知识：** Phase 0，第 01 课　**预计时间：** 约 30 分钟

## 学习目标

- 使用 `uv`、`venv` 或 `conda` 创建隔离环境
- 编写带可选依赖组的 `pyproject.toml` 并生成 lockfile
- 排查全局安装、混用 pip/conda 和 CUDA 版本不匹配
- 为依赖互相冲突的不同阶段设计独立环境

每个项目都应拥有自己的环境，避免 PyTorch、JAX、TensorFlow 或 CUDA 绑定相互覆盖。

推荐使用 `uv`：

```bash
uv python install 3.12
cd your-project
uv venv
source .venv/bin/activate
uv pip install torch numpy
```

也可以用 Python 内置的 `venv`：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

使用 `pyproject.toml` 固定项目依赖，使用 lockfile 保证协作者和 CI 安装相同版本。不要把不同 CUDA 构建或全局 pip 安装混在一起。
