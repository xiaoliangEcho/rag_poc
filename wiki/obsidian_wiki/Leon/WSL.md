---
title: WSL 常用命令
tags:
  - wsl
  - docker
  - 命令速查
---

# WSL 常用命令

## 启动 Docker 服务（WSL 内）

```bash
sudo service docker start
```

## 发行版管理（Windows 侧 PowerShell / CMD）

```bash
wsl --list -v                            # 列出已安装发行版及状态
wsl --shutdown                           # 关闭所有 WSL 实例
wsl --export <Distro> <file>.tar         # 导出发行版
wsl --import <Distro> <InstallPath> <file>.tar   # 导入发行版
```

## 相关

- [[windows_disk_space_high]] —— WSL 导致磁盘占用过高
- [[How_to_build_llama_cpp]] —— 在 WSL 内编译 llama.cpp
