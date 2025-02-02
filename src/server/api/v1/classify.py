import http

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from server.entity.content import content_ok


router = APIRouter(prefix='/classify', tags=['classify'])


@router.post('/single')
async def classify(file: UploadFile = File(...)):
    file_content = await file.read()
    return JSONResponse(content=content_ok(), status_code=http.HTTPStatus.OK)


@router.post('/buffer')
async def classify_buffer():
    return JSONResponse(content=content_ok(), status_code=http.HTTPStatus.OK)
