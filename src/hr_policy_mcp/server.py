from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from hr_policy_mcp.services.policy_service import PolicyService
from middleware.token_verifier import IntrospectionTokenVerifier
from core.config import get_settings
from mcp.server.auth.settings import AuthSettings


def create_hr_policy_mcp_server() -> FastMCP:
    settings = get_settings()
    host = settings.MCP_HOST
    port = settings.MCP_PORT
    server_url = settings.server_url

    # Configure token introspection against your Keycloak realm
    token_verifier = IntrospectionTokenVerifier(
        introspection_endpoint=settings.introspection_endpoint,
        server_url=server_url,
        validate_resource=False,
    )

    hr_policy_mcp = FastMCP("HR-Policy-MCP-Server",
            json_response=True,
            host=host,
            port=port,
            token_verifier=token_verifier,
            auth=AuthSettings(
                issuer_url=str(settings.OAUTH_ISSUER_URL),
                required_scopes=[settings.MCP_REQUIRED_SCOPE],
                resource_server_url=server_url,
            ),
        )
    
    return hr_policy_mcp 
    

def create_policy_service() -> PolicyService:
    """Create and return the shared PolicyService instance."""

    policy_dir = Path(__file__).resolve().parents[2] / "static" / "dev" / "policy_files"
    return PolicyService(policy_dir)


policy_service = create_policy_service()
hr_policy_mcp = create_hr_policy_mcp_server()

def run() -> None:
    """Run the HR policy MCP server over streamable-http (standalone)."""
    hr_policy_mcp.run(transport="streamable-http")


if __name__ == "__main__":
    run()
