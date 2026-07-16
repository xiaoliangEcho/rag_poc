# mcp_server.py
from mcp.server.fastmcp import FastMCP

# 1. 创建一个名为 "WeatherService" 的 MCP Server
mcp = FastMCP("WeatherService")

# 2. 使用 @mcp.tool() 装饰器将函数注册为 MCP 工具
@mcp.tool()
def get_weather(location: str) -> str:
    """获取指定城市的天气信息"""
    # 这里可以替换为真实的天气 API 请求
    return f"{location} 今天晴，气温 25°C。"

@mcp.tool()
def get_stock_price(stock_name: str) -> str:
    """获取指定股票的最新价格"""
    # 模拟返回数据
    stock_data = {"腾讯": "450.5 HKD", "阿里": "85.2 USD", "苹果公司": "195.3 USD"}
    return f"{stock_name} 的最新价格是 {stock_data.get(stock_name, '未知')}"


# 3. 启动服务。这里使用 stdio 模式，方便本地 Agent 直接通过进程通信调用
if __name__ == "__main__":
    mcp.run(transport="stdio")
