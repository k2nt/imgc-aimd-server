from typing import List, Tuple

import asyncio

from fastapi import APIRouter, File, UploadFile, Depends
from dependency_injector.wiring import Provide, inject

from server.bootstrap.di import DI
from server.api.schema import (
    response_ok, 
    BadRequestException, 
    InternalServerErrorException
)
from server.api.controller.imgc import Resnet50Controller
from server.domain.entity.imgc import Classification
from server.domain.entity.aimd_buffer import AIMDBufferItem
from server.infra.aimd_buffer import AIMDBuffer


router = APIRouter(prefix='/classify', tags=['classify'])


@router.post('/single')
@inject
async def classify(
        image: UploadFile = File(...),
        c: Resnet50Controller = Depends(Provide[DI.resnet50_controller])
):
    if image.content_type not in ['image/jpeg', 'image/png']:
        raise BadRequestException('Invalid image type. Only JPEG and PNG are allowed.')
    
    try:
        image_bytes = await image.read()
        classification = c.classify(image_bytes)
    except Exception as e:
        raise InternalServerErrorException(str(e))

    return response_ok(classification.model_dump())


@router.post('/buffer')
@inject
async def classify_buffer(
        image: UploadFile = File(...),
        buffer: AIMDBuffer = Depends(Provide[DI.aimd_buffer])
):
    if image.content_type not in ['image/jpeg', 'image/png']:
        raise BadRequestException('Invalid image type. Only JPEG and PNG are allowed.')

    try:
        image_bytes = await image.read()

        loop = asyncio.get_running_loop()
        result_ticket = loop.create_future()
        await buffer.put(AIMDBufferItem(data=image_bytes, result_ticket=result_ticket))

        # Actual classification managed in buffer coroutine
        classification: Classification = await result_ticket
    except Exception as e:
        raise InternalServerErrorException(str(e))

    return response_ok(data = classification.model_dump())
