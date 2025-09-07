#!/usr/bin/env python3

"""MCP server that executes code inside Docker containers."""

import subprocess
from typing import Dict

from mcp.server.fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP("CodeExecutor")

# Map supported languages to Docker images
IMAGE_MAP: Dict[str, str] = {
    "python": "python:3.11-alpine",
}

@mcp.tool()
def run_code(language: str, program: str) -> str:
    """Run a code snippet in a Docker container.

    Args:
        language: Programming language of the snippet.
        program: The code to execute.

    Returns:
        Combined stdout and stderr from the execution.
    """
    image = IMAGE_MAP.get(language.lower())
    if not image:
        return f"Unsupported language: {language}"

    cmd = [
        "docker", "run", "--rm",
        "--network", "none",
        "--memory", "128m",
        "--cpus", "1",
        "-i",
        image,
        "python", "-c", program,
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except FileNotFoundError:
        return "Docker is not available on this system."
    except subprocess.SubprocessError as exc:
        return f"Failed to run container: {exc}"

    output = result.stdout or ""
    if result.stderr:
        output += ("\n" if output else "") + result.stderr
    return output

if __name__ == "__main__":
    mcp.run()
