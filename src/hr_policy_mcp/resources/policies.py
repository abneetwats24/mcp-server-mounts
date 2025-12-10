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
async def get_policy() -> str:
    logger.info(f"Reading HR policy Opportune Posh Policy")

    try:
        return policy_service.get_policy_content("Opportune Posh Policy")
    except Exception as exc:
        logger.error(f"Failed to read policy Opportune Posh Policy: {exc}")
        raise

@hr_policy_mcp.resource("greeting://{name}", 
                        name="Personalized Greeting", 
                        description="Get a personalized greeting")
async def get_greeting(name) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
