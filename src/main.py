from __future__ import annotations

import logging
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from core.config import get_settings
from hr_policy_mcp.server import hr_policy_mcp  # registers HR policy resources
from math_mcp.server import math_mcp            # registers math tools
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

def setup_logging() -> None:
    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "server.log"

    handlers = [
        logging.StreamHandler(),
        logging.FileHandler(log_file),
    ]

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
    )


def create_server() -> FastMCP:
    hr_policy_mcp.settings.streamable_http_path = "/"
    math_mcp.settings.streamable_http_path = "/"
    # Mount the servers
    main_server = Starlette(
        routes=[
            Mount("/hr-policy", app=hr_policy_mcp.streamable_http_app()),
            Mount("/math", app=math_mcp.streamable_http_app()),
        ]
    )
    return main_server


def run() -> None:
    setup_logging()
    server = create_server()
    # Run the Starlette app using Uvicorn programmatically
    uvicorn.run(server, host="0.0.0.0", port=3000, log_level="debug")

if __name__ == "__main__":
    run()
