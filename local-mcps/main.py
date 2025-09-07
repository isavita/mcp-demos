#!/usr/bin/env python

import asyncio
import os 

from mistralai import Mistral
from mistralai.extra.run.context import RunContext
from mcp import StdioServerParameters
from mistralai.extra.mcp.stdio import MCPClientSTDIO
from pathlib import Path

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
        args=[str((cwd / "mcp_servers/stdio_server.py").resolve())],
        env=None,
    )

    # Create an agent to tell the weather
    weather_agent = client.beta.agents.create(
        model=MODEL,
        name="weather teller",
        instructions="You are able to tell the weather.",
        description="",
    )

        # Define the expected output format for weather results
    class WeatherResult(BaseModel):
        user: str
        location: str
        temperature: float

    # Create a run context for the agent
    async with RunContext(
        agent_id=weather_agent.id,
        output_format=WeatherResult,
        continue_on_fn_error=True,
    ) as run_ctx:
        import random
        # Register a function to get a random location for a user, it will be an available tool
        @run_ctx.register_func
        def get_location(name: str) -> str:
            """Function to get location of a user.

            Args:
                name: name of the user.
            """
            return random.choice(["Witham", "Toronto", "Plovdiv", "Southend-on-sea"])

        # Create and register an MCP client with the run context
        mcp_client = MCPClientSTDIO(stdio_params=server_params)
        await run_ctx.register_mcp_client(mcp_client=mcp_client)
        
        # Run the agent with a query
        run_result = await client.beta.conversations.run_async(
            run_ctx=run_ctx,
            inputs="Tell me the weather in John's location currently.",
        )

        # Print the results
        print("All run entries:")
        for entry in run_result.output_entries:
            print(f"{entry}")
            print()
        print(f"Final model: {run_result.output_as_model}")

if __name__ == "__main__":
    asyncio.run(main())
