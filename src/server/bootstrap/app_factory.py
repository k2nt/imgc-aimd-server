import os
import asyncio
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
from server.infra.logger import logger
from server.job import flush_aimd_buffer_job

import server.job as server_job_module
import server.api.v1.classify as api_v1_pkg


def setup_di(ctx: Context):
    di = DI()
    di.init_resources()

    di.aimd_buffer.set_kwargs(
        max_latency_ms=ctx.sla.max_latency_ms,
        init_capacity_num_req=ctx.aimd_buffer.init_capacity_num_req,
        incr_amt=ctx.aimd_buffer.incr_amt,
        decr_fct=ctx.aimd_buffer.decr_fct 
    )

    # Add module paths that requires DI (with respect to `server`)
    modules = [
        server_job_module.__name__
    ]
    # modules = [f"src.{module}" for module in modules]
    
    # Add package paths that requires DI (with respect to `server`)
    # All component modules will be wired with DI
    pkgs = [
        api_v1_pkg.__name__
    ]
    pkgs = [f"src.{pkg}" for pkg in pkgs]

    di.wire(
        modules=modules,
        packages=pkgs,
        from_package='server'
    )


def setup_coroutines():
    asyncio.create_task(flush_aimd_buffer_job())


def setup_logging():
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    tf.get_logger().setLevel(logging.ERROR)
    keras_config.disable_interactive_logging()


def on_startup():
    logger.info('[MAIN] Launching AIMD buffer batch processing coroutine ...')
    setup_coroutines()

    logger.info('[MAIN] Configuring external logging ...')
    setup_logging()


def on_shutdown():
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup()
    yield
    on_shutdown()


def build_app(ctx: Context) -> FastAPI:
    logger.info('[MAIN] Building application ...')
    setup_di(ctx)

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
