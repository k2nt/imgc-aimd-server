from typing import Any, List

import asyncio
import time


_MAX_BUFFER_CAPACITY = 100
_MIN_BUFFER_CAPACITY = 1


class AIMDBuffer:
    def __init__(
            self,
            max_latency_ms: float,
            init_capacity_num_req: int,
            incr_amt: int,
            decr_fct: float,
    ):
        self._capacity = init_capacity_num_req
        self._incr_amt = incr_amt
        self._decr_fct = decr_fct

        # Will be set on the first insertion
        self._start_time: float = -1

        # Queue here is not bounded by size
        # Manage queue size and blocking at capacity manually
        self._queue: List[Any] = []

        # Events to govern when to flush and when to put data
        self._can_flush_event = asyncio.Event()
        self._can_put_event = asyncio.Event()
        self._can_put_event.set()
        self._timed_out: bool = False

        # Start coroutine to periodically check max latency requirement
        asyncio.create_task(
            self._check_max_latency(max_latency_ms / 1000)
        )

    def _set_can_flush_event(self):
        self._can_flush_event.set()
        self._can_put_event.clear()

    def _set_can_put_event(self):
        self._can_flush_event.clear()
        self._can_put_event.set()
        self._timed_out = False
        self._start_time = -1

    def _at_capacity(self) -> bool:
        return len(self._queue) >= self._capacity
    
    def _increase_capacity(self):
        self._capacity = min(
            self._capacity + self._incr_amt,
            _MAX_BUFFER_CAPACITY
        )

    def _decrease_capacity(self):
        self._capacity = max(
            int(self._capacity * self._decr_fct),
            _MIN_BUFFER_CAPACITY
        )

    async def _check_max_latency(self, max_latency):
        while True:
            await asyncio.sleep(max_latency)

            cur_latency = time.perf_counter() - self._start_time
            if self._queue and cur_latency >= max_latency:
                self._can_flush_event.set()
                self._timed_out = True

    async def put(self, data: Any):
        await self._can_put_event.wait()

        if not self._queue:
            self._start_time = time.perf_counter()

        self._queue.append(data)

        if self._at_capacity():
            self._set_can_flush_event()

    async def flush(self) -> List[Any]:
        await self._can_flush_event.wait()

        q = self._queue.copy()
        self._queue.clear()

        if self._timed_out:
            self._decrease_capacity()
        else:
            self._increase_capacity()

        self._set_can_put_event()
        return q
