---
title: 编译 llama.cpp（纯 CPU）
tags:
  - llama.cpp
  - 编译
  - LLM
  - Qwen
---

# 编译 llama.cpp（纯 CPU）

> 在 WSL/Linux 下从源码编译 llama.cpp，纯 CPU 推理，并下载 Qwen3-4B 量化模型。

## 前提

- 已安装 `cmake`、`wget`、`gcc/g++`、`make`
- 在 WSL 环境中运行（参考 [[WSL]]）

## 拉取源码

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp/
```

## 编译

```bash
mkdir build && cd build
# 纯 CPU 编译，开启当前 CPU 架构的指令集优化（能稍微提升一点纯 CPU 的推理速度）
cmake .. -DLLAMA_NATIVE=ON
cmake --build . --config Release -j$(nproc)
```

## UI 包下载失败处理

> 构建后若 UI 包自动下载失败，手动下载并放回 `tools/ui/dist`，再重新编译。

```bash
wget https://github.com/ggml-org/llama.cpp/releases/download/b10068/llama-b10068-ui.tar.gz
tar -xvzf llama-b10068-ui.tar.gz
ls tools/ui/
mv llama-b10068 tools/ui/dist
ls tools/ui/dist/

cd build/
cmake --build . --config Release -j$(nproc)
```

## 下载模型

```bash
# Qwen3-4B Q4_K_M 量化版 GGUF（从 hf-mirror 镜像下载）
wget https://hf-mirror.com/Qwen/Qwen3-4B-GGUF/resolve/main/Qwen3-4B-Q4_K_M.gguf
```

## 相关

- [[obsidian_mcp_server]] —— 在 WSL 内用 llama.cpp server 接 Obsidian MCP
- [[WSL]] —— WSL 常用命令
