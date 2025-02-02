import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.server.api.router import router


def on_startup():
    pass


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
