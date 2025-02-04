from typing import List, Tuple

import asyncio
from asyncio import Future

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


router = APIRouter(prefix='/classify', tags=['classify'])


@router.post('/single')
@inject
async def classify(
        image: UploadFile = File(...),
        c: Resnet50Controller = Depends(Provide[DI.resnet50_controller])
):
    if image.content_type not in ['image/jpeg', 'image/png']:
        raise BadRequestException('Invalid image type. Only JPEG and PNG are allowed.')
    
    image_bytes = await image.read()

    try:
        classification = c.classify(image_bytes)
    except Exception as e:
        raise InternalServerErrorException(str(e))

    return response_ok(classification.model_dump())


@router.post('/buffer')
@inject
async def classify_buffer(
        image: UploadFile = File(...),
        buffer: List[Tuple[bytes, Future]] = Depends(Provide[DI.buffer])
):
    if image.content_type not in ['image/jpeg', 'image/png']:
        raise BadRequestException('Invalid image type. Only JPEG and PNG are allowed.')

    image_bytes = await image.read()
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    buffer.append((image_bytes, future))

    # Classification is handled in buffer coroutine
    # See server.job
    classfication: Classification = await future

    return response_ok(data=classfication.model_dump())

    # classification = c.classify(image_bytes)

    # return JSONResponse(
    #     content=content_ok(data=classification.model_dump()), 
    #     status_code=http.HTTPStatus.OK
    # )
