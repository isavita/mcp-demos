# MCP Demos

This repository hosts example MCP servers and scripts for experimenting with the
Model Context Protocol using Mistral's SDK.

## Advent of Code Docker server

`local-mcps/mcp_servers/aoc_server.py` implements a simple MCP server that can
run Advent of Code solutions inside a Docker container. It exposes a single
`run_solution` tool which accepts:

- `language` – programming language of the solution (currently only `python`).
- `code` – source code to execute.
- `input_path` – optional path to an input file that will be copied into the
  container and made available to the program.

The server writes the code to a temporary directory, mounts it inside a Python
Docker image and returns the program's stdout. This provides an isolated
execution environment suitable for evaluating puzzle solutions.
