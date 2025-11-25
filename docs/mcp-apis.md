# MCP APIs

## HR Policy Resources

- **Resource URI format**: `policy://<policy-name>`
  - Derived from PDF filenames in `static/dev/policy_files/`.
  - Example: `leave_policy.pdf` → `policy://leave-policy`.

- **Behavior**:
  - Returns `text/plain` content extracted from the PDF.
  - Logs via:
    - MCP `Context` (`ctx.info`, `ctx.error`).
    - Standard logging (`PolicyService` logger).

## Math Tools

- **add(a: float, b: float)**
  - Returns `a + b`.
  - Logs via MCP `Context.debug`.

- **subtract(minuend: float, subtrahend: float)**
  - Returns `minuend - subtrahend`.
  - Logs via MCP `Context.debug`.

- **health()**
  - Returns `{"status": "ok"}`.
  - Logs via MCP `Context.info`.

## Health & Monitoring

- Use the `health` tool to verify the math MCP server is reachable and
  authenticated.
- Check `logs/server.log` for server-side issues, including policy loading
  and PDF parsing errors.
