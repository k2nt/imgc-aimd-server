import asyncio
import time

from starlette.middleware.base import BaseHTTPMiddleware


class AIMDBufferMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
    ):
        super().__init__(app)
        pass


    async def dispatch(self, request, call_next):
        _ = await call_next(request)
