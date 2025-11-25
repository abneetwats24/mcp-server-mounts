# HR Policy MCP Server

This project provides an MCP server that exposes:

- HR policy documents as MCP resources (from local PDF files).
- Simple math tools (add, subtract, health check) as MCP tools.

Both are composed behind a single MCP endpoint with Keycloak-based authentication,
using the official [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk).

See the other pages in this documentation for setup, architecture, and API details.
