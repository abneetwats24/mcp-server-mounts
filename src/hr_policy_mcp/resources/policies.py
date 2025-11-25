from __future__ import annotations

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

from hr_policy_mcp.server import hr_policy_mcp, policy_service


# Register each policy as a separate MCP resource.
for _policy_name in policy_service.get_policy_names():
    uri = f"policy://{_policy_name.lower().replace(' ', '-')}"

    @hr_policy_mcp.resource(
        uri=uri,
        name=f"HR Policy - {_policy_name}",
        description=f"HR Policy Document: {_policy_name}",
        mime_type="text/plain",
    )
    async def _get_policy(
        policy_name: str = _policy_name,
        ctx: Context[ServerSession, None] | None = None,
    ) -> str:
        if ctx is not None:
            await ctx.info(f"Reading HR policy '{policy_name}'")

        try:
            return policy_service.get_policy_content(policy_name)
        except Exception as exc:
            if ctx is not None:
                await ctx.error(f"Failed to read policy '{policy_name}': {exc}")
            raise
