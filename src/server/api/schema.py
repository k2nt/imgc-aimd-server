from typing import Any, Dict, Optional

from pydantic import BaseModel


class BaseContent(BaseModel):
    """Base content.py schema."""
    message: str
    data: Optional[Dict[str, Any]] = {}


def content(message: str, data: Optional[Any] = None) -> Dict[str, Any]:
    return BaseContent(message=message, data=data).model_dump(exclude_none=True)


def content_ok(data: Optional[Any] = None) -> Dict[str, Any]:
    return content(message="ok", data=data)


def content_bad_request(data: Optional[Any] = None) -> Dict[str, Any]:
    return content(message="bad_request", data=data)


def content_not_found(data: Optional[Any] = None) -> Dict[str, Any]:
    return content(message="not_found", data=data)


def content_internal_error(data: Optional[Any] = None) -> Dict[str, Any]:
    return content(message="internal_error", data=data)
