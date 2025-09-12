#!/usr/bin/env python3
"""MCP server for running Advent of Code solutions in Docker.

Currently supports Python solutions. It writes provided source code to a
temporary directory, mounts that directory inside a Docker container and
runs the program. If an input file path is supplied it will be copied into
the temporary directory so the code can access it by its basename.
"""

import os
import shutil
import subprocess
import tempfile
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AocDockerServer")

@mcp.tool()
def run_solution(language: str, code: str, input_path: Optional[str] = None) -> str:
    """Run an Advent of Code solution inside Docker and return stdout.

    Args:
        language: Programming language of the solution. Only ``"python"`` is
            supported currently.
        code: Source code to execute.
        input_path: Optional path to a local input file. If provided, the file
            will be copied into the execution directory and available inside the
            container by its basename.

    Returns:
        The stdout produced by the program, or an error message if execution
        fails.
    """
    lang = language.lower()
    if lang != "python":
        return "Error: only python language is supported at the moment."

    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "solution.py")
        with open(src_file, "w", encoding="utf-8") as f:
            f.write(code)

        if input_path:
            shutil.copy(input_path, os.path.join(tmpdir, os.path.basename(input_path)))

        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{tmpdir}:/workspace",
            "-w",
            "/workspace",
            "python:3",
            "python",
            "solution.py",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Execution failed:\n{result.stderr}"
        return result.stdout

if __name__ == "__main__":
    mcp.run()
