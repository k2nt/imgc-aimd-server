import http

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject

from server.bootstrap.di import DI
from server.api.schema import content_ok
from server.api.controller.imgc import Resnet50Controller


router = APIRouter(prefix='/classify', tags=['classify'])


@router.post('/single')
@inject
async def classify(
        image: UploadFile = File(...),
        c: Resnet50Controller = Depends(Provide[DI.resnet50_controller])
):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=http.HTTPStatus.BAD_REQUEST, 
            detail="Invalid image type. Only JPEG and PNG are allowed."
        )
    
    image_bytes = await image.read()
    classification = c.classify(image_bytes)

    return JSONResponse(
        content=content_ok(data=classification.model_dump()), 
        status_code=http.HTTPStatus.OK
    )


@router.post('/buffer')
async def classify_buffer(
        image: UploadFile = File(...),
        c: Resnet50Controller = Depends(Provide[DI.resnet50_controller])
):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=http.HTTPStatus.BAD_REQUEST, 
            detail="Invalid image type. Only JPEG and PNG are allowed."
        )

    image_bytes = await image.read()
    classification = c.classify(image_bytes)

    return JSONResponse(
        content=content_ok(data=classification.model_dump()), 
        status_code=http.HTTPStatus.OK
    )
