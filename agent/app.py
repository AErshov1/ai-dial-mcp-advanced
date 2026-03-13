import asyncio
import json
import os

from agent.clients.custom_mcp_client import CustomMCPClient
from agent.clients.mcp_client import MCPClient
from agent.clients.dial_client import DialClient
from agent.models.message import Message, Role

API_KEY = os.getenv("DIAL_API_KEY")
DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com"


async def main():
    # TODO:
    # 1. Take a look what applies DialClient
    # 2. Create empty list where you save tools from MCP Servers later
    # 3. Create empty dict where where key is str (tool name) and value is instance of MCPClient or gustomMCPClient
    # 4. Create UMS MCPClient, url is `http://localhost:8006/mcp` (use static method create and don't forget that its asyncg
    # 5. Collect tools and dict [tool name, mcp client]
    # 6. Do steps 4 and 5 for `https://remote.mcpservers.org/fetch/mcp`
    # 7. Create DialClient, endpoint is `https://ai-proxy.lab.epam.com`
    # 8. Create array with Messages and add there System message with simple instructions for LLM that it should help to handle user request
    # 9. Create simple console chat (as we done in previous tasks)
    async with await CustomMCPClient.create('http://localhost:8000/mcp') as mcp_client:
        tools = await mcp_client.get_tools()
        print(f"=> User Management Tools: {tools}")

        fetch_mcp_client = await MCPClient.create("https://remote.mcpservers.org/fetch/mcp")
        fetch_tools = await fetch_mcp_client.get_tools()
        print(f"=> Fetch Tools: {fetch_tools}")

        tool_map: dict[str, CustomMCPClient] = {}
        for t in tools:
            tool_map[t["function"]["name"]] = mcp_client
        for t in fetch_tools:
            tool_map[t["function"]["name"]] = fetch_mcp_client

        all_tools = tools + fetch_tools
        dial_client = DialClient(
            api_key=API_KEY,
            endpoint=DIAL_ENDPOINT,
            tools=all_tools,
            tool_name_client_map=tool_map
        )

        chat_history: list[Message] = [
            Message(role=Role.SYSTEM,
                    content="You are a helpful assistant that can use tools to manage user profiles.")
        ]

        while True:
            user_input = input("👤: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                print("Exiting chat.")
                break

            if user_input:
                chat_history.append(
                    Message(role=Role.USER, content=user_input))

                response_message = await dial_client.get_completion(chat_history)
                chat_history.append(response_message)


if __name__ == "__main__":
    asyncio.run(main())


# Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him
