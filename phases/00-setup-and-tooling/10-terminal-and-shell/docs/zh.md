# 终端与 Shell

> 终端是 AI 工程师的主要工作场所。先熟悉它。

**类型：** Learn　**语言：** --　**前置知识：** Phase 0，第 01 课　**预计时间：** 约 35 分钟

终端会贯穿训练、GPU 监控、日志查看、远程 SSH 和环境管理。掌握 `cd`、`pwd`、`ls`、`grep`、管道、重定向和历史搜索。

```bash
cd ~/projects/ai-engineering-from-scratch
pwd
ls -la
grep "loss" train.log | wc -l
```

用 `tmux` 保持训练会话：一个窗口运行训练，一个监控 GPU，一个查看日志。断开 SSH 后训练仍会继续。

```bash
tmux new -s training
tmux detach
tmux attach -t training
nvidia-smi
```

使用 `htop`、`nvtop` 和 `nvidia-smi` 观察资源；使用 `ssh`、`scp` 和 `rsync` 在本地与远程机器之间传输文件。对包含空格的路径使用引号，删除前仔细确认目标。
