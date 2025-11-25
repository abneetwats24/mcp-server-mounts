from __future__ import annotations

import logging
from pathlib import Path

from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP

from core.config import get_settings
from hr_policy_mcp import hr_policy_mcp  # registers HR policy resources
from math_mcp import math_mcp            # registers math tools
from middleware.token_verifier import IntrospectionTokenVerifier


def setup_logging() -> None:
    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "server.log"

    handlers = [
        logging.StreamHandler(),
        logging.FileHandler(log_file),
    ]

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
    )


def create_server() -> FastMCP:
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

    main_server = FastMCP(
        "Main-MCP-Server",
        host=host,
        port=port,
        token_verifier=token_verifier,
        auth=AuthSettings(
            issuer_url=str(settings.OAUTH_ISSUER_URL),
            required_scopes=[settings.MCP_REQUIRED_SCOPE],
            resource_server_url=server_url,
        ),
    )

    main_server.mount(hr_policy_mcp, prefix="hr")
    main_server.mount(math_mcp, prefix="math")

    return main_server


def run() -> None:
    setup_logging()
    server = create_server()
    server.run(transport="streamable-http")


if __name__ == "__main__":
    run()
