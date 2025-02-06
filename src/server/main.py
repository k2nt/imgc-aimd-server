import uvicorn
import logging

from server.bootstrap.app_factory import build_app
from server.bootstrap.context import load_context_from_yaml
from server.infra.logger import LOGGING_CONFIG


def launch():
    ctx = load_context_from_yaml('src/server/ctx.yaml')
    app = build_app(ctx)
    uvicorn.run(
        app, 
        host="localhost", 
        port=ctx.server.port,
        log_config=LOGGING_CONFIG,
    )


if __name__ == "__main__":
    launch()
    