"""Check PyTorch accelerator support and compare matrix multiplication speed.

Lesson: phases/00-setup-and-tooling/03-gpu-setup-and-cloud/docs/en.md
Supports NVIDIA CUDA and Apple Silicon MPS devices.
The benchmark is a quick environment check, not a rigorous performance test.
"""

import statistics
import time


def synchronize(torch, device):
    """Wait for queued accelerator operations to finish."""
    if device.type == "cuda":
        torch.cuda.synchronize()
    elif device.type == "mps" and hasattr(torch.mps, "synchronize"):
        torch.mps.synchronize()


def benchmark_matmul(torch, a, b, device, warmup=2, repeats=5):
    """Return the median matrix multiplication time after warm-up runs."""
    for _ in range(warmup):
        _ = a @ b
    synchronize(torch, device)

    timings = []
    for _ in range(repeats):
        start = time.perf_counter()
        _ = a @ b
        synchronize(torch, device)
        timings.append(time.perf_counter() - start)

    return statistics.median(timings)


def check_gpu():
    try:
        import torch
    except ImportError:
        print("PyTorch not installed. Run: pip install torch")
        return

    print("=== GPU Check ===\n")
    print(f"PyTorch version: {torch.__version__}")
    cuda_available = torch.cuda.is_available()
    mps_available = bool(getattr(torch.backends, "mps", None)) and torch.backends.mps.is_available()

    print(f"CUDA available: {cuda_available}")
    print(f"MPS available: {mps_available}")

    device = None
    device_label = None
    props = None

    if cuda_available:
        device = torch.device("cuda")
        device_label = f"CUDA GPU: {torch.cuda.get_device_name(0)}"
        print(f"CUDA version: {torch.version.cuda}")
        print(f"CUDA device count: {torch.cuda.device_count()}")

        props = torch.cuda.get_device_properties(0)
        print(f"Memory: {props.total_memory / 1e9:.1f} GB")
        print(f"Compute capability: {props.major}.{props.minor}")
    elif mps_available:
        device = torch.device("mps")
        device_label = "Apple Silicon GPU: MPS"
        print(f"MPS built: {torch.backends.mps.is_built()}")
    else:
        print("\nNo GPU detected. That's fine for most lessons.")
        print("For GPU-heavy lessons, use Google Colab (free).")
        return

    print(f"Device: {device_label}")

    print("\n=== CPU vs GPU Benchmark ===\n")
    size = 2000

    a = torch.randn(size, size)
    b = torch.randn(size, size)

    cpu_time = benchmark_matmul(torch, a, b, torch.device("cpu"))
    print(f"CPU matrix multiply ({size}x{size}): {cpu_time:.3f}s")

    a_accelerator = a.to(device)
    b_accelerator = b.to(device)
    gpu_time = benchmark_matmul(torch, a_accelerator, b_accelerator, device)
    print(f"Accelerator matrix multiply ({size}x{size}): {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time / gpu_time:.1f}x")

    if props is not None:
        vram_gb = props.total_memory / 1e9
        params_fp16 = vram_gb * 1e9 / 2
        params_billions = params_fp16 / 1e9
        print(f"\nTheoretical fp16 weight capacity: ~{params_billions:.1f}B parameters")
        print("Actual usable model size is smaller due to runtime and activation memory.")
    else:
        print("\nApple Silicon uses unified memory, so there is no CUDA-style VRAM estimate here.")


if __name__ == "__main__":
    check_gpu()
