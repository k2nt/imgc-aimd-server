import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.api.router import router
from server.di import DI


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


app = FastAPI(lifespan=lifespan)
app.include_router(router)


def launch():
    uvicorn.run(app, host="localhost", port=3000)


if __name__ == "__main__":
    launch()
    