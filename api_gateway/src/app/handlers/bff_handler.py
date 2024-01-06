import logging
from typing import Union, Any

import httpx
from fastapi import Request
from httpx import Response
from starlette.responses import JSONResponse, Response as FastAPIResponse

from app.core import exceptions
from app.core.config import DOMAIN_MAPPER
from app.core.decorators import http_exc_handler
from app.models.request_model import RequestDTO


class BFFHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def execute(self, request: Request) -> JSONResponse:
        constructed_url, service_name = await self.map_request_url(str(request.url))
        self.logger.info("Созданный URL-адрес: %s", constructed_url)
        if constructed_url is None:
            raise exceptions.NoInternalServiceException(message=str(request.url))

        body = None
        if request.headers.get("Content-Length") is not None:
            body = await request.body()

        headers = await self.constructed_headers(request)
        request_dto = RequestDTO(
            method=request.method,
            url=constructed_url,
            data=body,
            cookies=request.cookies,
            headers=headers,
        )
        return await self._make_request(request_dto)

    async def _make_request(self, request: RequestDTO) -> JSONResponse:
        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.request(**request.model_dump())

            return await self.convert_client_response_to_server_response(response)

    @http_exc_handler
    async def reroute_to_appropriate_service(
        self, request: Request
    ) -> JSONResponse | Response:
        # Извлечь только путь и строку запроса из URL
        path_with_query = request.url.path
        if request.url.query:
            path_with_query += "?" + request.url.query

        try:
            return await self.execute(request)
        except exceptions.NoInternalServiceException as e:
            self.logger.exception("Запрашиваемый сервис не найден: %s", e.message)
            return Response(status_code=404)

    @staticmethod
    async def constructed_headers(request: Request) -> dict[str, Any]:
        constructed_headers = dict(request.headers)
        constructed_headers["host"] = constructed_headers["host"].replace("_", "-")
        constructed_headers["user-id"] = request.state.user_id
        constructed_headers["user-email"] = request.state.user_email

        return constructed_headers

    @staticmethod
    async def map_request_url(url: str):
        new_url = None
        destination_service_name = None

        for service_name in DOMAIN_MAPPER:
            if service_name in url:
                index = url.find(service_name)
                new_url = DOMAIN_MAPPER[service_name] + url[index - 1 : :]
                destination_service_name = service_name
                break

        return new_url, destination_service_name

    async def convert_client_response_to_server_response(
        self,
        client_response: Response,
    ) -> Union[JSONResponse, FastAPIResponse]:
        content_type = client_response.headers.get("content-type", "")
        body = client_response.read()
        headers = client_response.headers
        status_code = client_response.status_code

        response_method = response_mapper.get(content_type, _default_response)
        return response_method(body, status_code, headers)


def _json_response(
    body: bytes, status_code: int, headers: dict[str, str]
) -> FastAPIResponse:
    return FastAPIResponse(content=body, status_code=status_code, headers=headers)


def _default_response(
    body: bytes, status_code: int, headers: dict[str, str]
) -> FastAPIResponse:
    return FastAPIResponse(
        content=body.decode("utf-8") if isinstance(body, bytes) else body,
        status_code=status_code,
        headers=headers,
    )


response_mapper = {"application/json": _json_response}
