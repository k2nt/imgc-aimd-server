from typing import Any
from dataclasses import dataclass

import asyncio


@dataclass(init=True)
class AIMDBufferItem:
    data: Any
    result_ticket: asyncio.Future
