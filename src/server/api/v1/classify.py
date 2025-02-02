import http

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from server.entity.content import content_ok


router = APIRouter(prefix='/classify', tags=['classify'])


@router.post('/single')
async def classify():
    return JSONResponse(content=content_ok(), status_code=http.HTTPStatus.OK)


@router.post('/buffer', status_code=http.HTTPStatus.OK)
async def classify_buffer():
    return JSONResponse(content=content_ok(), status_code=http.HTTPStatus.OK)
