# backend\math_agent\llm\mcp_servers.py
from langchain_mcp_adapters.client import MultiServerMCPClient  
from core.config import settings

async def search_web_mcp(question: str) -> str:
    api_key = settings.TAVILY_API
    url = f'https://mcp.tavily.com/mcp/?tavilyApiKey={api_key}'

    client = MultiServerMCPClient(
        {
            "tavily_search":{
                "transport": "streamable_http",
                "url": url
            }
        }
    )

    try: 
        tools = await client.get_tools()
        if not tools:
            return "Error: No tools found on MCP server."
        search_tool = tools[0]
        print(f"[Web Search] Found MCP tool: {search_tool.name}")

        # 4. Call the tool
        # The Tavily tool takes a 'query' argument
        result_str = await search_tool.ainvoke({"query": question})
        print("[Web Search] Received context from MCP.")
        return str(result_str)

    except Exception as e:
        print(f"[Web Search] MCP Error: {e}")
        return f"Web search (MCP) failed: {e}"
