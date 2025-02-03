import http

from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject

from server.api.schema import content_ok
from server.domain.entity.context import Context
from server.di import DI


router = APIRouter(prefix='/classify', tags=['classify'])


@router.post('/single')
async def classify():
    return JSONResponse(content=content_ok(), status_code=http.HTTPStatus.OK)


@router.post('/buffer')
async def classify_buffer():
    return JSONResponse(content=content_ok(), status_code=http.HTTPStatus.OK)
