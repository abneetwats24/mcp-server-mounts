from __future__ import annotations

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

from math_mcp.server import math_mcp


@math_mcp.tool()
async def add(
    a: float,
    b: float,
    ctx: Context[ServerSession, None] | None = None,
) -> float:
    result = a + b
    if ctx is not None:
        await ctx.debug(f"Adding {a} + {b} = {result}")

    return result


@math_mcp.tool()
async def health(ctx: Context[ServerSession, None] | None = None) -> dict[str, str]:
    """Simple health check for the math MCP server."""

    if ctx is not None:
        await ctx.info("Health check invoked on math_mcp server")

    return {"status": "ok"}


@math_mcp.tool()
async def subtract(
    minuend: float,
    subtrahend: float,
    ctx: Context[ServerSession, None] | None = None,
) -> float:
    result = minuend - subtrahend
    if ctx is not None:
        await ctx.debug(f"Subtracting {subtrahend} from {minuend} = {result}")

    return result
