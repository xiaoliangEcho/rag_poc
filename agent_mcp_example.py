# agent_mcp_example.py
import asyncio
import json
import requests
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

# 1. 定义一个函数，用于调用本地 llama-server 的 OpenAI 兼容接口
def call_llama_server(messages, tools=None):
    url = "http://127.0.0.1:8001/v1/chat/completions"
    payload = {
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    # 如果提供了工具，则加入 payload
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]
    else:
        print(f"调用 LLM 失败: {response.text}")
        return None

async def main():
    # 2. 配置 MCP Server 的启动参数 (确保 mcp_server.py 在同级目录下)
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    print("正在连接 MCP Server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化会话
            await session.initialize()
            
            # 获取 MCP Server 提供的所有工具
            tools_response = await session.list_tools()
            mcp_tools = tools_response.tools
            print(f"成功获取到 {len(mcp_tools)} 个 MCP 工具。")

            # 3. 将 MCP 工具转换为 OpenAI Function Calling 格式
            openai_tools = []
            for tool in mcp_tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })

            # 4. 构造对话历史
            messages = [
                {"role": "system", "content": "你是一个智能助手，可以根据用户需求调用合适的工具。"},
                # {"role": "user", "content": "帮我查一下上海今天的天气怎么样？"}
                {"role": "user", "content": "苹果公司的股价是多少？"}
            ]

            print("\n--- 开始测试 Agent 调用 MCP 工具 ---")
            print(f"用户提问: {messages[-1]['content']}")

            # 5. 第一次调用 LLM (让模型决定是否需要调用工具)
            assistant_message = call_llama_server(messages, tools=openai_tools)
            if not assistant_message:
                print(f"call_llama_server return null")
                return

            # 6. 检查模型是否决定调用工具
            if "tool_calls" in assistant_message and assistant_message["tool_calls"]:
                tool_call = assistant_message["tool_calls"][0]
                function_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]
                
                print(f"\n模型决定调用工具: {function_name}")
                print(f"参数: {arguments}")

                # 7. 通过 MCP 协议执行工具
                try:
                    args_dict = json.loads(arguments)
                    # 调用 MCP 工具
                    tool_result = await session.call_tool(function_name, arguments=args_dict)
                    # 提取工具返回的文本内容
                    result_text = tool_result.content[0].text if tool_result.content else "无结果"
                    print(f"工具执行结果: {result_text}")

                    # 8. 将工具结果反馈给模型，生成最终回答
                    messages.append(assistant_message) # 记录模型的调用指令
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result_text
                    })

                    # 再次调用 LLM 生成最终回复
                    final_message = call_llama_server(messages)
                    if final_message:
                        print(f"\nAgent 最终回复: {final_message['content']}")
                except Exception as e:
                    print(f"执行工具时出错: {e}")
            else:
                # 如果模型没有调用工具，直接输出回复
                print(f"\nAgent 直接回复: {assistant_message['content']}")

if __name__ == "__main__":
    asyncio.run(main())