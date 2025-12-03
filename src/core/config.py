from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment.

    This centralizes server and auth configuration so we don't hardcode
    host/port/issuer/scope in multiple places.
    """

    # Pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # MCP server
    MCP_HOST: str = "127.0.0.1"
    MCP_PORT: int = 3000
    MCP_PATH: str = "" #/.well-known/oauth-protected-resource/MCP_PATH
    MATH_MCP_PATH: str = "/math"
    HR_POLICY_MCP_PATH: str = "/hr-policy"

    # Auth / Keycloak
    OAUTH_ISSUER_URL: AnyHttpUrl = AnyHttpUrl(
        "http://192.168.10.7:5555/realms/openspace"  # default realm
    )
    MCP_REQUIRED_SCOPE: str = "mcp:tools"

    OAUTH_CLIENT_ID: Optional[str] = None
    OAUTH_CLIENT_SECRET: Optional[str] = None

    @property
    def server_url(self) -> str:
        return f"http://{self.MCP_HOST}:{self.MCP_PORT}{self.MCP_PATH}"

    @property
    def math_server_url(self) -> str:
        return f"http://{self.MCP_HOST}:{self.MCP_PORT}{self.MATH_MCP_PATH}"
    
    @property
    def hr_policy_server_url(self) -> str:
        return f"http://{self.MCP_HOST}:{self.MCP_PORT}{self.HR_POLICY_MCP_PATH}"

    @property
    def introspection_endpoint(self) -> str:
        # For Keycloak: <issuer>/protocol/openid-connect/token/introspect
        issuer = str(self.OAUTH_ISSUER_URL).rstrip("/")
        return f"{issuer}/protocol/openid-connect/token/introspect"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
