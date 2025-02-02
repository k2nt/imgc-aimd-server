from fastapi import APIRouter

from .classify import router as classify_router


router = APIRouter(prefix='/api/v1')

router.include_router(classify_router)
