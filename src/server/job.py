from typing import List, Tuple

import time
import asyncio
from asyncio import Future
from dependency_injector.wiring import Provide, inject

from server.bootstrap.di import DI
from server.api.controller.imgc import Resnet50Controller


@inject
async def aimd_buffer_batch_processing(
        c: Resnet50Controller = Provide[DI.resnet50_controller],
        buffer: List[Tuple[bytes, Future]] = Provide[DI.buffer]
):
    pass
    # print("c", type(c))
    # print("buffer", type(buffer))
    # while True:
    #     if len(buffer) == 3:
    #         image_bytes_list = [data[0] for data in buffer]
            

    #         classifications = c.classify_batch(image_bytes_list)

    #         for i, data in enumerate(buffer):
    #             data[1].set_result(classifications[i])

    #         buffer = []
