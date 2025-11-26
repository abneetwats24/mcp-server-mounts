from __future__ import annotations

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

from hr_policy_mcp.server import hr_policy_mcp, policy_service


# Register each policy as a separate MCP resource.


def _register_policy_resource(policy_name: str) -> None:
    uri = f"policy://{policy_name.lower().replace(' ', '-') }"

    @hr_policy_mcp.resource(
        uri=uri,
        name=f"HR Policy - {policy_name}",
        description=f"HR Policy Document: {policy_name}",
        mime_type="text/plain",
    )
    async def _get_policy(ctx: Context[ServerSession, None] | None = None) -> str:
        if ctx is not None:
            await ctx.info(f"Reading HR policy '{policy_name}'")

        try:
            return policy_service.get_policy_content(policy_name)
        except Exception as exc:
            if ctx is not None:
                await ctx.error(f"Failed to read policy '{policy_name}': {exc}")
            raise


for _policy_name in policy_service.get_policy_names():
    _register_policy_resource(_policy_name)
