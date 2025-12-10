from __future__ import annotations
import logging

from hr_policy_mcp.server import hr_policy_mcp, policy_service
logger = logging.getLogger(__name__)

# Register each policy as a separate MCP resource.


def _register_policy_resource(policy_name: str) -> None:
    uri = f"policy://{policy_name.lower().replace(' ', '-') }"

    @hr_policy_mcp.resource(
        uri=uri,
        name=f"HR Policy - {policy_name}",
        description=f"HR Policy Document: {policy_name}",
        mime_type="text/plain",
    )
    async def _get_policy() -> str:
        try:
            logger.info(f"Reading { policy_name } policy document")
            return policy_service.get_policy_content(policy_name)
        except Exception as exc:
            logger.error(f"Failed to read policy {policy_name}: {exc}")
            raise


for _policy_name in policy_service.get_policy_names():
    _register_policy_resource(_policy_name)
