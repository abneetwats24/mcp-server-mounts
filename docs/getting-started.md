# Getting Started

## Prerequisites

- Python environment managed by `uv` (recommended) or your own virtualenv.
- Docker and Docker Compose (optional, for containerized deployment).
- Running Keycloak realm at:
  `http://192.168.10.7:5555/realms/openspace`.

## Configuration

Copy `.env.example` to `.env` and adjust values:

```bash
cp .env.example .env
```

Set at least:

```bash
OAUTH_CLIENT_ID=your-mcp-client-id
OAUTH_CLIENT_SECRET=your-mcp-client-secret
MCP_REQUIRED_SCOPE=mcp:tools
OAUTH_ISSUER_URL=http://192.168.10.7:5555/realms/openspace
```

## Run locally with uv

```bash
uv run src/main.py
```

The MCP server will listen on:

```text
http://127.0.0.1:3000/mcp
```

## Run with Docker Compose

```bash
docker compose up --build
```

This builds the image, mounts the project into `/app`, and exposes `3000:3000`.
