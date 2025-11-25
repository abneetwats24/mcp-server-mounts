# Auth & Security

This server follows the **simple-auth** pattern from the MCP Python SDK,
with Keycloak as the Authorization Server.

## Keycloak Integration

- Realm discovery URL:
  `http://192.168.10.7:5555/realms/openspace/.well-known/openid-configuration`
- Introspection endpoint (derived from issuer):
  `http://192.168.10.7:5555/realms/openspace/protocol/openid-connect/token/introspect`

## Server-Side Auth

- `src/core/config.py` defines `Settings` with:
  - `OAUTH_ISSUER_URL`
  - `MCP_REQUIRED_SCOPE`
  - `OAUTH_CLIENT_ID` / `OAUTH_CLIENT_SECRET`

- `src/middleware/token_verifier.py` implements `IntrospectionTokenVerifier`:
  - Posts tokens to the introspection endpoint.
  - Optionally authenticates with Keycloak using client credentials.
  - Validates that the token is active and (optionally) bound to this resource.

- `src/main.py` wires `AuthSettings` and the token verifier into `FastMCP`.

## Client Requirements

- MCP clients must:
  - Obtain bearer tokens from Keycloak for the configured client.
  - Include the token in MCP HTTP requests.
  - Request the `mcp:tools` scope (or whatever you configure).
