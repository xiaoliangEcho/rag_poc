from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# --- 1. 定义工具 (Tools) ---
@tool
def get_current_time(query: str) -> str:
    """当你需要知道当前时间时调用此工具"""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- 2. 配置本地大模型 ---
llm = ChatOpenAI(
    model="qwen2.5-3b",
    base_url="http://localhost:8001/v1",
    api_key="sk-no-key-required",
    temperature=0,
    max_tokens=256
)

# --- 3. 构建支持记忆的 Agent ---
tools = [get_current_time]

# 核心：引入 MemorySaver 作为状态存档（Thread），用于管理连续的对话上下文
memory = MemorySaver()

# 创建带有记忆功能的 ReAct Agent
agent_executor = create_react_agent(
    llm, 
    tools, 
    checkpointer=memory  # 绑定记忆模块
)

# --- 4. 连续对话主循环 ---
if __name__ == "__main__":
    print("🤖 本地 Agent 已启动！(输入 'exit' 退出)")
    
    # 为当前对话分配一个唯一的 Thread ID，用于隔离不同的对话上下文
    config = {"configurable": {"thread_id": "user-session-1"}}
    
    while True:
        user_input = input("\n👤 你: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 再见！")
            break
            
        # 将用户输入和历史记录一起发送给 Agent
        inputs = {"messages": [("user", user_input)]}
        
        print("🤖 Agent: ", end="")
        final_response = ""
        
        # 流式输出 Agent 的思考与回复
        for event in agent_executor.stream(inputs, config=config, stream_mode="values"):
            if event["messages"]:
                last_msg = event["messages"][-1]
                # 只打印 AI 的最终回复，过滤掉工具调用的中间过程
                if last_msg.type == "ai" and last_msg.content:
                    # 避免重复打印
                    if last_msg.content != final_response:
                        final_response = last_msg.content
                        print(final_response)
