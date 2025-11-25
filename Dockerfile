FROM python:3.13-slim

WORKDIR /app

# Install system deps and uv (clean install inside container)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

# Copy project metadata first for efficient layer caching
COPY pyproject.toml uv.lock ./

# Install Python dependencies into the container env (no project install)
RUN uv sync --frozen --no-install-project

# Copy application source and ancillary files
COPY src ./src
COPY README.md LICENSE ./

ENV PYTHONPATH=/app/src

EXPOSE 3000

# Run the composite MCP server (HR policies + math) over streamable-http
CMD ["uv", "run", "src/main.py"]

