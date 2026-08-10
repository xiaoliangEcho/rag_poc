---
title: mov 指令后缀（AT&T 语法）
tags:
  - 汇编
  - x86-64
  - AT&T语法
---

# mov 指令后缀含义（AT&T 语法）

在 AT&T 语法中，`mov` 指令必须带后缀，用来明确操作数的大小：

| 后缀 | 全称 | 数据大小 | C 语言对应类型 |
|---|---|---|---|
| `movb` | Move **Byte** | 1 字节（8 位） | `char` |
| `movw` | Move **Word** | 2 字节（16 位） | `short` |
| `movl` | Move **Long** | 4 字节（32 位） | `int` |
| `movq` | Move **Quadword** | 8 字节（64 位） | `long` / 指针 |

## 相关

- [[cltq 指令]] —— 操作数大小相关
- [[x86 内存到内存限制]]
- [[learning_c]] —— C 语言学习 MOC
