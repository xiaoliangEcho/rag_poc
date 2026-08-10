---
title: C 语言学习 MOC
tags:
  - C
  - 学习MOC
  - 汇编
---

# C 语言学习 MOC

> 记录 C 语言学习过程中遇到的知识点。**大主题**拆成独立原子笔记（见下面索引，可被任意笔记反链）；**零碎小点**先记在末尾「速记区」，长大后再提升为独立笔记。

## 指令

- [[lea 指令]] —— 只算地址不访存，常被编译器用来做简单数学
- [[cltq 指令]] —— 32 位下标符号扩展为 64 位（对应 Intel `cdqe`）
- [[mov 指令后缀]] —— AT&T 语法 b/w/l/q 对应字节大小

## 寄存器

- [[RIP 寄存器]] —— 指令指针（IP → EIP → RIP）

## 安全 / 链接

- [[endbr64]] —— CET 防范 ROP 攻击
- [[PLT 过程链接表]] —— Procedure Linkage Table

## 内存模型

- [[x86 内存到内存限制]] —— 硬件不支持内存到内存直接传送

## 工具

- [[GNU binutils 工具集]] —— ar / strings / strip / nm / size / readelf / objdump / ldd

## 速记区

> 太小、还不够独立成篇的知识点先记在这里，长大后提升为上面的独立笔记。

- （待补充）

## 相关

- [[WSL]] / [[How_to_build_llama_cpp]] —— 实践环境
