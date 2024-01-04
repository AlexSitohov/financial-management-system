from enum import Enum

from pydantic import BaseModel


class MethodEnum(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    patch = "PATCH"
    delete = "DELETE"
    head = "HEAD"
    options = "OPTIONS"


class RequestDTO(BaseModel):
    method: MethodEnum
    url: str
    data: bytes | None
    cookies: dict | None
