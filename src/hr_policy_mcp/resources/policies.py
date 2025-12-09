from __future__ import annotations
import logging


from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

from hr_policy_mcp.server import hr_policy_mcp, policy_service


# Register each policy as a separate MCP resource.
logger = logging.getLogger(__name__)


@hr_policy_mcp.resource(
        uri="policy://opportune-posh-policy",
        name="HR Policy - Opportune Posh Policy",
        description=f"HR Policy Document: Opportune Posh Policy",
        mime_type="text/plain",
    )
async def get_policy(ctx: Context[ServerSession, None] | None = None) -> str:
    if ctx is not None:
        await ctx.info(f"Reading HR policy Opportune Posh Policy")
        logger.info(f"Reading HR policy Opportune Posh Policy")

    try:
        return policy_service.get_policy_content("Opportune Posh Policy")
    except Exception as exc:
        if ctx is not None:
            await ctx.error(f"Failed to read policy Opportune Posh Policy: {exc}")
            logger.error(f"Failed to read policy Opportune Posh Policy: {exc}")
        raise

@hr_policy_mcp.resource("greeting://{name}")
async def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


@hr_policy_mcp.prompt()
async def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    return f"Write a {style} greeting for someone named {name}."

@hr_policy_mcp.tool()
async def health(ctx: Context[ServerSession, None] | None = None) -> dict[str, str]:
    """Simple health check for the math MCP server."""

    if ctx is not None:
        await ctx.info("Health check invoked on math_mcp server")

    return {"status": "ok"}