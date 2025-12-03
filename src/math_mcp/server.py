from __future__ import annotations

from mcp.server.fastmcp import FastMCP

__all__ = ["math_mcp", "run"]

from middleware.token_verifier import IntrospectionTokenVerifier
from core.config import get_settings
from mcp.server.auth.settings import AuthSettings

def create_math_mcp_server() -> FastMCP:
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

    math_mcp = FastMCP("Math-Utility-MCP",
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
    
    return math_mcp

math_mcp = create_math_mcp_server()

def run() -> None:
    """Run the math MCP server over streamable-http (standalone)."""

    math_mcp.run(transport="streamable-http")


if __name__ == "__main__":
    run()
