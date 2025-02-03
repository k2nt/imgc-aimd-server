import asyncio
import time

from starlette.middleware.base import BaseHTTPMiddleware


class AIMDBufferMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            init_capacity: int,
            max_latency_ms: float,
    ):
        super().__init__(app)

        self._MAX_LATENCY_MS = max_latency_ms
        self._capacity = init_capacity

        # Semaphore to limit buffer size below capacity
        self._semaphore = asyncio.Semaphore(self._capacity)

        # Initially empty buffer
        self._start_time = -1

        # Multiplicative decrease amount
        # Based on Clipper paper, a 10% mult dec amount is sufficient 
        #   because true buffer size doesn't fluctuate very much
        self._mult_dec_amt = 0.9
        # Additive increase amount
        self._add_inc_amt = 1

    async def dispatch(self, request, call_next):
        if self._s == 0:
            self._start_time = time.perf_counter()

        async with self._semaphore:
            _ = call_next(request)

        latency_ms = (time.perf_counter() - self._start_time) * 1000
        if latency_ms > self._MAX_LATENCY_MS:
            self._capacity = max(1, int(self._size * self._mult_dec_amt))
        else:
            self._capacity += self._add_inc_amt

        self._semaphore = asyncio.Semaphore(self._capacity)
