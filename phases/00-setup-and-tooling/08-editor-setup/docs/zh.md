# 编辑器配置

> 编辑器是你的副驾驶。一次配置好，让它真正承担工作，而不是制造阻力。

**类型：** Build　**语言：** --　**前置知识：** Phase 0，第 01 课　**预计时间：** 约 20 分钟

推荐使用 VS Code，并安装 Python、Pylance、Jupyter、GitLens、Remote SSH、Debugpy、Black Formatter 和 Ruff 扩展。

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension charliermarsh.ruff
```

启用保存时格式化、类型检查和 lint；使用 Remote SSH 在远程 GPU 机器上像编辑本地文件一样开发。Cursor、Windsurf 和 Neovim 也可以使用，但应优先保证 Python 环境、终端、Git 和调试流程稳定。
