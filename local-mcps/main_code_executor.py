#!/usr/bin/env python

import asyncio
import os
from pathlib import Path

from mistralai import Mistral
from mistralai.extra.run.context import RunContext
from mcp import StdioServerParameters
from mistralai.extra.mcp.stdio import MCPClientSTDIO
from mistralai.types import BaseModel

# Set the current working directory and model to use
cwd = Path(__file__).parent
MODEL = "mistral-medium-latest"

async def main():
    # Initialize the Mistral client with your API key
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key)

    # Define parameters for the local MCP server
    server_params = StdioServerParameters(
        command="python",
        args=[str((cwd / "mcp_servers/code_executor_server.py").resolve())],
        env=None,
    )

    # Create an agent capable of executing code
    code_agent = client.beta.agents.create(
        model=MODEL,
        name="code executor",
        instructions="You can execute code snippets using the run_code tool.",
        description="",
    )

    class CodeResult(BaseModel):
        stdout: str

    # Create a run context for the agent
    async with RunContext(
        agent_id=code_agent.id,
        output_format=CodeResult,
        continue_on_fn_error=True,
    ) as run_ctx:
        # Register the MCP client with the run context
        mcp_client = MCPClientSTDIO(stdio_params=server_params)
        await run_ctx.register_mcp_client(mcp_client=mcp_client)

        # Run the agent with a query
        run_result = await client.beta.conversations.run_async(
            run_ctx=run_ctx,
            inputs="Run the following Python code and return its output: print('Hello from container')",
        )

        # Print the results
        print("All run entries:")
        for entry in run_result.output_entries:
            print(f"{entry}")
            print()
        print(f"Final model: {run_result.output_as_model}")

if __name__ == "__main__":
    asyncio.run(main())
