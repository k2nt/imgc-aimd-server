import sys
import asyncio
import logging

import tensorflow as tf
import keras.api.config as keras_config
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from server.api.router import router
from server.api.schema import bad_http_exception_handler
from server.api.middleware.buffer import AIMDBufferMiddleware
from server.bootstrap.di import DI
from server.bootstrap.context import Context
from server.job import aimd_buffer_batch_processing

import server.job as server_job_module
import server.api.v1.classify as api_v1_pkg

from dependency_injector.wiring import Provide, inject


def setup_di():
    di = DI()
    di.init_resources()

    # Add module paths that requires DI (with respect to `server`)
    modules = [
        server_job_module.__name__
    ]
    modules = [f"src.{module}" for module in modules]
    
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
    asyncio.create_task(aimd_buffer_batch_processing())


def setup_logging():
    tf.get_logger().setLevel(logging.ERROR)
    keras_config.disable_interactive_logging()


def on_startup():
    print('Setting up dependency injection ...')
    setup_di()

    print('Launching AIMD buffer batch processing coroutine ...')
    setup_coroutines()

    print('Configuring logging ...')
    setup_logging()


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
