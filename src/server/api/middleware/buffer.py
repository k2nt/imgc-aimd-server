import asyncio
import time

from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AIMDBufferMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            max_latency_ms: float,
            init_capacity_num_req: int,
            incr_amt: int,
            decr_fct: float,
    ):
        super().__init__(app)
        pass


    async def dispatch(self, req: Request, call_next):
        print("Middleware before request")
        resp = await call_next(req)
        print("Middleware after request")
        return resp
