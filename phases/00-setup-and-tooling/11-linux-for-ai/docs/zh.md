# 面向 AI 的 Linux

> 大多数 AI 任务运行在 Linux 上。掌握足够的基础知识，才不会被环境卡住。

**类型：** Learn　**语言：** --　**前置知识：** Phase 0，第 01 课　**预计时间：** 约 30 分钟

Linux 从根目录 `/` 组织文件，没有 Windows 的盘符。常用目录包括 `~/`（个人文件）、`/tmp`（临时文件）、`/usr`（系统程序）、`/etc`（配置）、`/var/log`（日志）和 `/mnt`（挂载卷）。

```bash
pwd
ls -la
cd /path/to/dir
mkdir -p a/b/c
cp -r src/ src-backup/
mv old.txt new.txt
cat file.txt
tail -f log.txt
```

使用 `chmod` 管理权限，使用 `chown` 修改文件所有者；遇到 Permission denied 时先检查路径和权限，不要盲目使用 `sudo`。Ubuntu GPU 机器通常通过 `apt` 安装系统包：

```bash
sudo apt update
sudo apt install -y build-essential git curl wget unzip
```

macOS 与 Linux 的命令和路径存在差异；远程开发时尤其要注意 shell、文件权限、进程管理和 CUDA 驱动。
