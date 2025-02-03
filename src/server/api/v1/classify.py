import http

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject

from server.di import DI
from server.api.schema import content_ok
from server.domain.entity.context import Context
from server.service.imgc import Resnet50Service


router = APIRouter(prefix='/classify', tags=['classify'])


@router.post('/single')
@inject
async def classify(
        image: UploadFile = File(...),
        svc: Resnet50Service = Depends(Provide[DI.resnet50_service])
):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image type. Only JPEG and PNG are allowed.")
    
    image_bytes = await image.read()
    classification = svc.classify(image_bytes)

    return JSONResponse(
        content=content_ok(data=classification.model_dump()), 
        status_code=http.HTTPStatus.OK
    )


@router.post('/buffer')
async def classify_buffer():
    return JSONResponse(content=content_ok(), status_code=http.HTTPStatus.OK)
