---
title: Obsidian MCP Server 接入笔记
tags:
  - obsidian
  - mcp
  - workbuddy
  - llama.cpp
---

# Obsidian MCP Server 接入笔记

> Obsidian 的「Local REST API with MCP」插件（v5+）内置 MCP Server，可直接被外部客户端连接。

## 源码

- [coddingtonbear/obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api) —— A secure REST API and Model Context Protocol (MCP) server for your vault.

## 基本设置

- 在插件设置里把监听地址设为 `127.0.0.1`（默认端口 27123）
- **API Key** 在插件设置页生成并复制；下面配置里的 `Bearer xxx` 需替换为真实 Key

## WorkBuddy 接入

在 `~/.workbuddy/mcp.json` 中配置（传输类型为 Streamable HTTP，URL 以 `/mcp` 结尾）：

```json
{
  "mcpServers": {
    "mcp-obsidian": {
      "type": "http",
      "url": "http://127.0.0.1:27123/mcp",
      "headers": {
        "Authorization": "Bearer xxx"
      }
    }
  }
}
```

> 写入后需在 WorkBuddy 连接器页面信任/启用，并重启 WorkBuddy 生效。

## WSL 内 llama.cpp server 接入

当 MCP 客户端跑在 WSL 里时：

- 把 Obsidian Local REST API 的监听地址改为 WSL 网关地址（如 `172.24.96.1`），而非 `127.0.0.1`
- 需启用 `--ui-mcp-proxy`，并从 UI 设置里使用

## 相关

- [[How_to_build_llama_cpp]] —— llama.cpp 编译
- [[WSL]] —— WSL 常用命令
