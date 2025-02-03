import os
import logging

import tensorflow as tf
import keras.api.config as keras_config
from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.api.router import router
from server.api.schema import bad_http_exception_handler
from server.api.middleware.buffer import AIMDBufferMiddleware
from server.bootstrap.di import DI
from server.bootstrap.context import Context


def on_startup():
    di = DI()
    di.init_resources()
    di.wire(
        modules=['src.server.main', 'src.server.api.v1.classify']
    )

    tf.get_logger().setLevel(logging.ERROR)
    keras_config.disable_interactive_logging()


def on_shutdown():
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup()
    yield
    on_shutdown()


def build_app(ctx: Context) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    app.exception_handler(bad_http_exception_handler)
    app.add_middleware(
        AIMDBufferMiddleware, 
        max_latency_ms=ctx.sla.max_latency_ms,
        init_capacity_num_req=ctx.aimd_buffer.init_capacity_num_req,
        incr_amt=ctx.aimd_buffer.incr_amt,
        decr_fct=ctx.aimd_buffer.decr_fct,
    )
    return app

