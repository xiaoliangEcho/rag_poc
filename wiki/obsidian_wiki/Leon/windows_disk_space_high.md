---
title: WSL 导致 Windows 磁盘占用过高
tags:
  - wsl
  - windows
  - 磁盘
---

# WSL 导致 Windows 磁盘占用过高

## 现象

启用 WSL 后，Windows 系统盘空间占用异常升高。

## 原因

WSL 崩溃会在以下目录产生大量 dump 文件：

```
C:\Users\17128\AppData\Local\Temp\wsl-crashes
```

## 清理方法

- 手动删除 `wsl-crashes` 目录下的 dump 文件
- 删除前建议先 `wsl --shutdown` 关闭 WSL 实例
- 若反复产生大量崩溃转储，说明 WSL 本身存在崩溃问题，可关注 WSL 版本更新或排查发行版问题

## 相关

- [[WSL]] —— WSL 常用命令
