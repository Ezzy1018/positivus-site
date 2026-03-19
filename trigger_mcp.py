import asyncio
import sys
import json
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "figma-developer-mcp",
            f"--figma-api-key={os.environ.get('FIGMA_API_KEY', '')}",
            "--json",
        ],
    )

    print("Starting Figma Code-to-Canvas MCP Bridge...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("Connected to Figma MCP Server. Requesting code-to-canvas capture...")

            # Request the generate_figma_design tool
            try:
                result = await session.call_tool(
                    "generate_figma_design",
                    {
                        "url": "http://localhost:8080/index.html",
                        "destinationFileUrl": "https://www.figma.com/design/s9hXBJXnZZGbIPuL7etZfL/Positivus-Landing-Page-Design",
                    },
                )
                print(f"Capture Session Initiated: {result}")
            except Exception as e:
                print(f"Error executing MCP tool: {e}")


if __name__ == "__main__":
    asyncio.run(main())
