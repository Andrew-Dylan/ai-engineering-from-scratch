# Jupyter Notebook

> Notebook 是 AI 工程的实验台：先在这里快速原型验证，再把有效成果移入生产代码。

**类型：** Build　**语言：** Python　**前置知识：** Phase 0，第 01 课　**预计时间：** 约 30 分钟

## 学习目标

- 安装并启动 JupyterLab、Jupyter Notebook 或 VS Code Jupyter 扩展
- 使用 `%timeit`、`%%time` 和 `%matplotlib inline` 进行计时与可视化
- 区分 Notebook 与脚本，实践“Notebook 中探索、脚本中交付”
- 避免乱序执行、隐藏状态和内存泄漏等常见问题

Notebook 由代码单元和 Markdown 单元组成。所有单元共享同一个 Python kernel，因此变量会在单元之间保留；这既方便探索，也容易因为乱序执行造成隐蔽错误。完成实验后应重启 kernel 并从头运行，确认结果可复现。

```bash
pip install jupyterlab
jupyter lab
```

常用快捷键：`Shift+Enter` 运行当前单元，`A/B` 在上方/下方插入单元，`DD` 删除单元，`M` 转为 Markdown，`Y` 转为代码，`Z` 撤销单元操作。

Notebook 适合探索数据、可视化和交互式实验；脚本适合测试、部署、定时运行和版本控制。不要把只在当前 kernel 状态下有效的 Notebook 当成生产程序。
