from typing import Any, Dict, Optional

import http

from pydantic import BaseModel
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class BaseContent(BaseModel):
    code: str
    data: Dict[str, Any]


class BadHTTPException(HTTPException):
    def __init__(self, code: str, error: str, status_code: int):
        detail = {'code': code, 'data': {'error': error}}
        super().__init__(status_code=status_code, detail=detail)


async def bad_http_exception_handler(_: Request, exc: BadHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


class BadRequestException(BadHTTPException):
    def __init__(self, error: str = ''):
        super().__init__(
            code='bad_request',
            error=error,
            status_code=http.HTTPStatus.BAD_REQUEST
        )


class InternalServerErrorException(BadHTTPException):
    def __init__(self, error: str = ''):
        super().__init__(
            code='internal_server_error', 
            error=error, 
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR
        )


def response_ok(data: Optional[Dict[str, Any]]) -> JSONResponse:
    return JSONResponse(content=data, status_code=http.HTTPStatus.OK)
