import http

from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject

from server.entity.content import content_ok
from server.entity.context import Context
from server.di import DI


router = APIRouter(prefix='/classify', tags=['classify'])


@router.post('/single')
@inject
async def classify(
    ctx: Context = Depends(Provide[DI.context])
):
    print("AAAA", ctx.sla, ctx.server)
    return JSONResponse(content=content_ok(), status_code=http.HTTPStatus.OK)


@router.post('/buffer')
async def classify_buffer():
    return JSONResponse(content=content_ok(), status_code=http.HTTPStatus.OK)
