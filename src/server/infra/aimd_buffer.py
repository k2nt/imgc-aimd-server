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

            print('[AIMD_BUFFER] Checking max latency ...')

            cur_latency = time.perf_counter() - self._start_time
            if self._queue and cur_latency >= max_latency:
                print('[AIMD_BUFFER] (check_max_latency) Buffer timed out, setting signal to flush ...')
                self._can_flush_event.set()
                self._timed_out = True

    async def put(self, data: Any):
        print('[AIMD_BUFFER] Waiting for buffer to flush ...')
        await self._can_put_event.wait()
        
        if not self._queue:
            self._start_time = time.perf_counter()

        self._queue.append(data)

        print(f"[AIMD_BUFFER] (put) Putting item into buffer, buffer utilization is [{len(self._queue)} / {self._capacity}] ...")

        if self._at_capacity():
            print('[AIMD_BUFFER] (put) Buffer is at capacity, setting signal to flush ...')
            self._set_can_flush_event()

    async def flush(self) -> List[Any]:
        print('[AIMD_BUFFER] (flush) Waiting for flush signal ...')
        await self._can_flush_event.wait()
        print(f"[AIMD_BUFFER] (flush) Flush signal received due to {'timed out' if self._timed_out else 'at capacity'}, flushing ...")

        q = self._queue.copy()
        self._queue.clear()

        if self._timed_out:
            self._decrease_capacity()
            print(f"[AIMD_BUFFER] Decreasing capacity, new capacity is {self._capacity}")
        else:
            self._increase_capacity()
            print(f"[AIMD_BUFFER] Increasing capacity, new capacity is {self._capacity}")

        self._set_can_put_event()
        return q
