from typing import List

import asyncio

from dependency_injector.wiring import Provide, inject

from server.bootstrap.di import DI
from server.api.controller.imgc import Resnet50Controller
from server.domain.entity.aimd_buffer import AIMDBufferItem
from server.infra.aimd_buffer import AIMDBuffer
from server.infra.logger import logger


@inject
async def flush_aimd_buffer_job(
        c: Resnet50Controller = Provide[DI.resnet50_controller],
        buffer: AIMDBuffer = Provide[DI.aimd_buffer]
):
    while True:
        logger.debug('[FLUSH_AIMD_BUFFER_JOB] Waiting for buffer flush ...')
        items: List[AIMDBufferItem] = await buffer.flush()
        logger.debug(f"[FLUSH_AIMD_BUFFER_JOB] Buffer flushed with bath size {len(items)} ...")

        classifications = c.classify_batch(item.data for item in items)
        for i, item in enumerate(items):
            item.result_ticket.set_result(classifications[i])
