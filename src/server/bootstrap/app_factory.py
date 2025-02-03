from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.api.router import router
from server.api.middleware.buffer import AIMDBufferMiddleware
from server.bootstrap.di import DI
from server.bootstrap.context import Context


def on_startup():
    di = DI()
    di.init_resources()
    di.wire(
        modules=['src.server.main', 'src.server.api.v1.classify']
    )


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
    app.add_middleware(
        AIMDBufferMiddleware, 
        init_capacity=ctx.sla.init_buffer_size_num_req,
    )
    return app

