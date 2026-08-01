# 调试与性能分析

> 最糟糕的 AI bug 不会崩溃：它们悄悄用垃圾数据训练，却给你一条漂亮的 loss 曲线。

**类型：** Build　**语言：** Python　**前置知识：** 第 1 课（开发环境）、基本 PyTorch 知识　**预计时间：** 约 60 分钟

## 学习目标

- 使用条件断点和调试输出检查张量形状、dtype 与 NaN
- 使用 `cProfile`、`line_profiler` 和 `tracemalloc` 找到瓶颈
- 检测形状不匹配、NaN loss、数据泄漏和设备错误
- 使用 TensorBoard 查看 loss、权重直方图和梯度分布

调试应从三层开始：普通 Python（断点、日志、性能和内存）、张量操作（形状、dtype、设备、NaN/Inf），以及训练动态（loss、梯度和激活值）。大多数 AI bug 出现在前两层。

```python
def debug_print(name, tensor):
    print(f"{name}: shape={tensor.shape}, dtype={tensor.dtype}, "
          f"device={tensor.device}, min={tensor.min().item():.4f}, "
          f"max={tensor.max().item():.4f}, has_nan={tensor.isnan().any().item()}")
```

在可疑位置使用 `breakpoint()`，检查 `outputs.shape`、`loss.item()`、NaN 数量和梯度。性能问题先测量再优化：区分数据加载、前向、反向和 GPU 同步时间。使用 TensorBoard 观察曲线时，同时检查数据、设备和梯度是否合理。

```bash
tensorboard --logdir runs
```

重点排查：输入与标签是否错位、训练/验证数据是否泄漏、张量是否位于同一设备、loss 是否突然变成 NaN，以及是否忘记 `detach()`。
