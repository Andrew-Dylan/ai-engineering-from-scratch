# 数据管理

> 数据是燃料；管理数据的方式决定你前进的速度。

**类型：** Build　**语言：** Python　**前置知识：** Phase 0，第 01 课　**预计时间：** 约 45 分钟

## 学习目标

- 使用 Hugging Face `datasets` 加载、流式读取和缓存数据集
- 在 CSV、JSON、Parquet 和 Arrow 之间转换并理解取舍
- 使用固定随机种子创建可复现的训练/验证/测试集
- 用 `.gitignore`、Git LFS 或 DVC 管理大型文件

```bash
pip install datasets huggingface_hub
```

```python
from datasets import load_dataset

dataset = load_dataset("imdb")
print(dataset)
print(dataset["train"][0])
```

大数据集可以使用 `streaming=True`，逐行处理而不下载全部内容。常见格式转换如下：

```python
dataset = load_dataset("imdb", split="train")
dataset.to_csv("imdb_train.csv")
dataset.to_json("imdb_train.json")
dataset.to_parquet("imdb_train.parquet")
```

固定 seed 后再划分数据集；测试集必须与训练流程隔离。模型权重和数据集不要直接提交到 Git，应使用缓存、LFS 或 DVC。
