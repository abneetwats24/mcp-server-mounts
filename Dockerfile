FROM ghcr.io/astral-sh/uv:python3.13-slim

WORKDIR /app

# Copy project metadata first for efficient layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (without editable project install)
RUN uv sync --frozen --no-install-project

# Copy application source
COPY src ./src
COPY README.md LICENSE ./

ENV PYTHONPATH=/app/src

EXPOSE 3000

# Run the composite MCP server (HR policies + math) over streamable-http
CMD ["uv", "run", "src/main.py"]

