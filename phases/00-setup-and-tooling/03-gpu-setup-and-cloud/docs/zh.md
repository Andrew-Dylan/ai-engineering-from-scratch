# GPU 配置与云端

> 使用 CPU 学习完全没问题。真正进行训练则需要 GPU。

**类型：** Build
**语言：** Python
**前置知识：** 阶段 0，第 01 课
**预计时间：** 约 45 分钟

## 学习目标

- 使用 `nvidia-smi` 和 PyTorch 的 CUDA API 验证本地 GPU 是否可用
- 在 Google Colab 中配置 T4 GPU，免费进行云端实验
- 对 CPU 和 GPU 上的矩阵乘法进行基准测试，并测量加速效果
- 使用 fp16 经验法则，估算显存能够容纳的最大模型

## 问题

阶段 1～3 中的大多数课程都可以在 CPU 上正常运行。但是，当你开始训练 CNN、Transformer 或 LLM（阶段 4 及以后）时，就需要 GPU 加速。一项在 CPU 上需要 8 小时的训练任务，在 GPU 上可能只需要 10 分钟。

你有三种选择：本地 GPU、云 GPU，或者免费的 Google Colab。

## 核心概念

```text
你可以选择：

1. 本地 NVIDIA GPU
   费用：0 美元（你已经拥有它）
   配置：安装 CUDA 和 cuDNN
   最适合：经常使用、处理大型数据集

2. Google Colab（免费层）
   费用：0 美元
   配置：无需配置
   最适合：快速实验、家中没有 GPU

3. 云 GPU（Lambda、RunPod、Vast.ai）
   费用：每小时 0.20～2.00 美元
   配置：SSH 连接并安装环境
   最适合：正式训练、大型模型
```

## 动手构建

### 选项 1：本地 NVIDIA GPU

检查你的计算机是否安装了 NVIDIA GPU：

> **Mac 用户注意：** 本小节只适用于 NVIDIA GPU。Apple Silicon Mac 没有 CUDA，因此不要在本机运行下面的 `nvidia-smi`，也不要直接调用这段代码中的 `torch.cuda.*`。对应的 MPS 写法见下一小节。

```bash
nvidia-smi
```

安装支持 CUDA 的 PyTorch：

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
```

### 选项 1b：Apple Silicon GPU（MPS）

如果你使用 M 系列芯片的 Mac，PyTorch 会使用 MPS 而不是 CUDA：

```python
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"MPS built: {torch.backends.mps.is_built()}")
print(f"MPS available: {torch.backends.mps.is_available()}")

if torch.backends.mps.is_available():
    device = torch.device("mps")
    print(f"Device: {device}")

    # 新版 PyTorch 可以直接读取 Metal 设备名称。
    if hasattr(torch.backends.mps, "get_name"):
        print(f"GPU: {torch.backends.mps.get_name()}")

    # 这是 Metal 建议的最大工作集，不等同于独立显卡的物理显存。
    if hasattr(torch.mps, "recommended_max_memory"):
        memory_gb = torch.mps.recommended_max_memory() / 1e9
        print(f"Recommended max memory: {memory_gb:.1f} GB")
else:
    print("MPS is unavailable; use CPU instead.")
```

进行基准测试时，将张量移动到 `mps` 设备；如果 `torch.mps.synchronize()` 可用，还需要调用它来同步计算。

#### CUDA 到 MPS 的替换速查

不能简单地把所有 `torch.cuda` 字符串替换成 `torch.mps`，因为两个后端的 API 并非完全一一对应。常见替换方式如下：

| CUDA 写法 | Apple Silicon / MPS 写法 | 说明 |
|-----------|--------------------------|------|
| `torch.cuda.is_available()` | `torch.backends.mps.is_available()` | 检查 MPS 当前是否可用 |
| `torch.device("cuda")` | `torch.device("mps")` | 创建 MPS 设备对象 |
| `tensor.to("cuda")` | `tensor.to("mps")` | 把张量移动到 Apple GPU |
| `model.to("cuda")` | `model.to("mps")` | 把模型移动到 Apple GPU |
| `torch.cuda.synchronize()` | `torch.mps.synchronize()` | 等待异步 GPU 运算完成；旧版 PyTorch 应先用 `hasattr` 检查 |
| `torch.cuda.get_device_name(0)` | `torch.backends.mps.get_name()` | 新版 PyTorch 可用；旧版可以直接显示 `Apple Silicon GPU (MPS)` |
| `torch.version.cuda` | 没有直接对应项 | MPS 使用 macOS 的 Metal，不安装 CUDA；可检查 `torch.__version__` 和 `torch.backends.mps.is_built()` |
| `torch.cuda.get_device_properties(0).total_memory` | `torch.mps.recommended_max_memory()` | 返回 Metal 建议的最大工作集，并非独立 VRAM；Apple Silicon 使用统一内存 |

### 选项 2：Google Colab

1. 打开 [colab.research.google.com](https://colab.research.google.com)
2. 依次选择 Runtime > Change runtime type > T4 GPU
3. 运行 `!nvidia-smi` 进行验证

你可以把本课程的 Notebook 直接上传到 Colab。

### 选项 3：云 GPU

对于 Lambda Labs、RunPod 或 Vast.ai：

> **Mac 用户注意：** 下面的 `torch.cuda.*` 是在远程 NVIDIA 云服务器上执行的，不是在你的 Mac 本机执行。Mac 只负责通过 SSH 连接服务器，因此这里不需要替换为 MPS。

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### 没有 GPU？没问题

大多数课程都可以在 CPU 上运行。需要 GPU 的课程会明确说明，并附上 Colab 链接。

下面这段是 CUDA/CPU 二选一的通用代码；如果直接在 Apple Silicon Mac 上运行，它不会选择 MPS，而是会退回 CPU：

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using: {device}")
```

在 Apple Silicon 上，应使用下面的三后端选择逻辑。它会优先选择 NVIDIA CUDA，其次选择 Apple MPS，最后退回 CPU：

```python
if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print(f"Using: {device}")
```

## 动手构建：GPU 与 CPU 基准测试

```python
import torch
import time

size = 5000

a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)

start = time.time()
c_cpu = a_cpu @ b_cpu
cpu_time = time.time() - start
print(f"CPU: {cpu_time:.3f}s")

if torch.cuda.is_available():
    a_gpu = a_cpu.to("cuda")
    b_gpu = b_cpu.to("cuda")

    torch.cuda.synchronize()
    start = time.time()
    c_gpu = a_gpu @ b_gpu
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU: {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")
```

> **Mac 用户注意：** 上面的基准测试分支只适用于 NVIDIA CUDA。你的 Mac 应运行下面的 MPS 分支。这里除了把设备名改成 `mps`，还要把 `torch.cuda.synchronize()` 改成 `torch.mps.synchronize()`。

对于 Apple Silicon，使用 `mps` 设备，并在调用同步函数之前检查它是否存在：

```python
if torch.backends.mps.is_available():
    a_gpu = a_cpu.to("mps")
    b_gpu = b_cpu.to("mps")

    if hasattr(torch.mps, "synchronize"):
        torch.mps.synchronize()
    start = time.time()
    c_gpu = a_gpu @ b_gpu
    if hasattr(torch.mps, "synchronize"):
        torch.mps.synchronize()
    gpu_time = time.time() - start
    print(f"MPS: {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")
```

## 练习

1. 运行上面的基准测试，比较 CPU 与 GPU 的运行时间
2. 如果你没有 GPU，请在 Google Colab 上运行测试并比较结果
3. 查看你的 GPU 有多少显存，并估算能够容纳的最大模型（经验法则：使用 fp16 时，每个参数需要 2 字节）

## 关键术语

| 术语 | 人们通常怎么说 | 它的实际含义 |
|------|----------------|--------------|
| CUDA | “GPU 编程” | NVIDIA 的并行计算平台，使你能够在 GPU 上运行代码 |
| VRAM | “GPU 内存” | GPU 上的显存，与系统内存相互独立；它会限制模型大小 |
| fp16 | “半精度” | 16 位浮点数；在精度损失很小的情况下，内存用量只有 fp32 的一半 |
| Tensor Core | “高速矩阵硬件” | 专门用于矩阵乘法的 GPU 核心，速度比普通核心快 4～8 倍 |
