from __future__ import annotations

"""Token verifier using OAuth 2.0 Token Introspection (RFC 7662).

Adapted from the python-sdk simple-auth example.
"""

import logging
from typing import Any

from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.shared.auth_utils import check_resource_allowed, resource_url_from_server_url
from core.config import get_settings

logger = logging.getLogger(__name__)


class IntrospectionTokenVerifier(TokenVerifier):
    """Verify bearer tokens via an OAuth 2.0 introspection endpoint."""

    def __init__(
        self,
        introspection_endpoint: str,
        server_url: str,
        validate_resource: bool = False,
    ) -> None:
        self.introspection_endpoint = introspection_endpoint
        self.server_url = server_url
        self.validate_resource = validate_resource
        self.resource_url = resource_url_from_server_url(server_url)

    async def verify_token(self, token: str) -> AccessToken | None:  # type: ignore[override]
        """Verify token via the configured introspection endpoint."""
        import httpx

        # Basic SSRF protection as in the example
        if not self.introspection_endpoint.startswith(
            ("https://", "http://localhost", "http://127.0.0.1", "http://192.168." )
        ):
            logger.warning("Rejecting introspection endpoint with unsafe scheme: %s", self.introspection_endpoint)
            return None

        timeout = httpx.Timeout(10.0, connect=5.0)
        limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)

        settings = get_settings()
        client_id = settings.OAUTH_CLIENT_ID
        client_secret = settings.OAUTH_CLIENT_SECRET

        auth = None
        if client_id and client_secret:
            auth = (client_id, client_secret)

        async with httpx.AsyncClient(timeout=timeout, limits=limits, verify=False, auth=auth) as client:
            try:
                response = await client.post(
                    self.introspection_endpoint,
                    data={"token": token},
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                if response.status_code != 200:
                    logger.debug("Token introspection returned status %s", response.status_code)
                    return None

                data = response.json()
                if not data.get("active", False):
                    return None
                
                if self.validate_resource and not self._validate_resource(data):
                    logger.warning("Token resource validation failed. Expected: %s", self.resource_url)
                    return None
                logger.debug("data: %s", data)
                return AccessToken(
                    token=token,
                    client_id=data.get("client_id", "unknown"),
                    scopes=data.get("scope", "").split() if data.get("scope") else [],
                    expires_at=data.get("exp"),
                    resource=data.get("aud")[0] if isinstance(data.get("aud"), list
                                                                ) else data.get("aud") if isinstance(
                                                                    data.get("aud"), str) else None,
                )
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Token introspection failed: %s", exc)
                return None

    def _validate_resource(self, token_data: dict[str, Any]) -> bool:
        if not self.server_url or not self.resource_url:
            return False

        aud: list[str] | str | None = token_data.get("aud")
        if isinstance(aud, list):
            return any(self._is_valid_resource(a) for a in aud)
        if aud:
            return self._is_valid_resource(aud)
        return False

    def _is_valid_resource(self, resource: str) -> bool:
        if not self.resource_url:
            return False
        return check_resource_allowed(requested_resource=self.resource_url, configured_resource=resource)
