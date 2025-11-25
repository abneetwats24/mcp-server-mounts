# Architecture

## High-Level Components

- **Main MCP Server (`src/main.py`)**
  - Composite `FastMCP` server.
  - Mounts:
    - `hr_policy_mcp` under prefix `hr`.
    - `math_mcp` under prefix `math`.
  - Configures auth via `AuthSettings` and `IntrospectionTokenVerifier`.

- **HR Policy MCP (`src/hr_policy_mcp/`)**
  - `server.py`: creates `hr_policy_mcp` FastMCP instance and a `PolicyService`.
  - `services/policy_service.py`: loads PDF policies and provides read access.
  - `resources/policies.py`: registers one MCP resource per policy with Context logging.

- **Math MCP (`src/math_mcp/`)**
  - `server.py`: creates `math_mcp` FastMCP instance.
  - `tools/basic.py`: math tools (`add`, `subtract`, `health`) with Context logging.

- **Middleware (`src/middleware/`)**
  - `token_verifier.py`: `IntrospectionTokenVerifier` that calls Keycloak's
    token introspection endpoint and validates bearer tokens.

- **Config (`src/core/config.py`)**
  - `Settings(BaseSettings)`: central config for host, port, issuer, scope,
    and client credentials, loaded from env and `.env`.

## Request Flow

1. MCP client connects to `http://127.0.0.1:3000/mcp` (streamable-http).
2. Client sends a request with a bearer token.
3. `FastMCP` uses `IntrospectionTokenVerifier` to introspect the token
   against Keycloak.
4. If valid and scopes match, the tool/resource call is routed to either:
   - HR resources (`hr` prefix).
   - Math tools (`math` prefix).
5. Tools/resources emit Context logs back to the client and standard logs
   go to stdout and `logs/server.log`.
