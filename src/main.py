from __future__ import annotations

import logging
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from core.config import get_settings
from hr_policy_mcp.server import hr_policy_mcp  # registers HR policy resources
from math_mcp.server import math_mcp            # registers math tools
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager, AsyncExitStack

def setup_logging() -> None:
    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "server.log"

    handlers = [
        logging.StreamHandler(),
        logging.FileHandler(log_file),
    ]

    logging.basicConfig(
        level=get_settings().LOG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
    )


@asynccontextmanager
async def combined_lifespan(app: Starlette):
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(hr_policy_mcp.session_manager.run())
        await stack.enter_async_context(math_mcp.session_manager.run())
        yield

def create_server() -> Starlette:
    hr_policy_mcp.settings.streamable_http_path = "/hr-policy"
    math_mcp.settings.streamable_http_path = "/math"
    # Mount the servers
    main_server = Starlette(
        routes=[
            Mount("/hr-policy", app=hr_policy_mcp.streamable_http_app()),
            Mount("/math", app=math_mcp.streamable_http_app()),
        ],
        lifespan=combined_lifespan,
    )
    main_server = CORSMiddleware(
        main_server,
        allow_origins=["*"],  # Configure appropriately for production
        allow_methods=["GET", "POST", "DELETE"],  # MCP streamable HTTP methods
        expose_headers=["Mcp-Session-Id"],
    )
    return main_server


def run() -> None:
    setup_logging()
    server = create_server()
    # Run the Starlette app using Uvicorn programmatically
    uvicorn.run(server, host="0.0.0.0", port=3000, log_level="debug")

if __name__ == "__main__":
    run()
