from __future__ import annotations

from mcp.server.fastmcp import FastMCP

__all__ = ["math_mcp", "run"]

math_mcp = FastMCP("Math-Utility-MCP")


def run() -> None:
    """Run the math MCP server over streamable-http (standalone)."""

    math_mcp.run(transport="streamable-http")


if __name__ == "__main__":
    run()
