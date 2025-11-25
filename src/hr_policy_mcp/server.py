from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from hr_policy_mcp.services.policy_service import PolicyService

hr_policy_mcp = FastMCP("HR-Policy-MCP-Server")


def create_policy_service() -> PolicyService:
    """Create and return the shared PolicyService instance."""

    policy_dir = Path(__file__).resolve().parents[2] / "static" / "dev" / "policy_files"
    return PolicyService(policy_dir)


policy_service = create_policy_service()


def run() -> None:
    """Run the HR policy MCP server over streamable-http (standalone)."""

    hr_policy_mcp.run(transport="streamable-http")


if __name__ == "__main__":
    run()
