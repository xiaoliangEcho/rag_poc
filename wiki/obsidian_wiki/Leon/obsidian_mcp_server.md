1.  restapi source code
	[coddingtonbear/obsidian-local-rest-api: A secure REST API and Model Context Protocol (MCP) server for your vault.](https://github.com/coddingtonbear/obsidian-local-rest-api)

2. set obsidian local REST API listening address: 127.0.0.1

3. For workbuddy
	-  Use the following mcp.json config
		`{
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
`
  
4. For llama cpp server in wsl
	- set obsidian local REST API listening address to wsl gateway(like: 172.24.96.1).
	- need to enable --ui-mcp-proxy and use it from UI setting