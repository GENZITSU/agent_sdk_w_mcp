import asyncio
import logging
import os
import subprocess
import sys
import time

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServerSse
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)



async def main() -> None:
    # pw_command = "npx playwright@latest run-server --port 8931"
    # pw_server = MCPServerStdio(
    #     name="Playwright MCP Server",
    #     params={"command": pw_command.split(" ")[0], "args": pw_command.split(" ")[1:]},
    # )

    pw_server = MCPServerSse(
        name="playwright Server",
        params={
            "url": "http://localhost:3001/sse",
        },
    )

    sse_server = MCPServerSse(
        name="sse Python Server",
        params={
            "url": "http://localhost:8000/sse",
        },
    )

    async with pw_server as pw, sse_server as sse:
        trace_id = gen_trace_id()
        print(f"View trace: https://platform.openai.com/traces/{trace_id}\n")

        with trace(workflow_name="Multi-MCP Server Demo Workflow", trace_id=trace_id):
            agent = Agent(
                name="OpenAI Agent w/ MCP Servers",
                instructions="Use the tools to access the internet.",
                mcp_servers=[pw, sse],
            )
            prompt = input("Enter a prompt (MCP servers (playwright-mcp, sse) are available): ")
            result = await Runner.run(starting_agent=agent, input=prompt)
            print(result.final_output)

            message = "What's the secret word?"
            print(f"\n\nRunning: {message}")
            result = await Runner.run(starting_agent=agent, input=message)
            print(result.final_output)


if __name__ == "__main__":
    try:
        # Run `uv run server.py` to start the SSE server
        process = subprocess.Popen(
            [
                "node",
                "dist/index.js",
            ],
        )
        time.sleep(5)

    except Exception as e:
        print(f"Error starting playwright server: {e}")
        sys.exit(1)

    try:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        server_file = os.path.join(this_dir, "server.py")

        print("Starting SSE server at http://localhost:8000/sse ...")

        # Run `uv run server.py` to start the SSE server
        process = subprocess.Popen(["uv", "run", server_file])
        # Give it 3 seconds to start
        time.sleep(5)

        print("SSE server started. Running example...\n\n")
    except Exception as e:
        print(f"Error starting SSE server: {e}")
        sys.exit(1)

    asyncio.run(main())
