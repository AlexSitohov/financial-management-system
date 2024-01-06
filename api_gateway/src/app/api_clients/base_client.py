import json
from typing import Any

import httpx

from app.core.decorators import http_exc_handler


class BaseHTTPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @http_exc_handler
    async def get(self, endpoint: str, on_404: Any = None, **kwargs) -> dict | Any:
        """
        Выполняет HTTP GET запрос к указанному `endpoint` и возвращает JSON-ответ.

        Args:
            endpoint (str): Оконечная точка (URL) для выполнения GET запроса.
            on_404 (Any, optional): Значение, которое будет возвращено, если получен код ответа 404 (Not Found). По умолчанию None.
            **kwargs: Дополнительные аргументы, передаваемые в метод `client_session.get()`.
        """

        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.get(f"{self.base_url}{endpoint}", **kwargs)

            if response.status_code != 200:
                if response.status_code == 404 and on_404 is not None:
                    return on_404
                else:
                    raise httpx.HTTPStatusError(
                        f"Error getting {endpoint}: {response.status_code} {response.text}",
                        request=response.request,
                        response=response,
                    )
            return response.json()

    @http_exc_handler
    async def get_raw(
        self, endpoint: str, on_404: Any = None, **kwargs
    ) -> httpx.Response:
        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.get(f"{self.base_url}{endpoint}", **kwargs)

            if response.status_code != 200:
                if response.status_code == 404 and on_404 is not None:
                    return on_404
                else:
                    raise httpx.HTTPStatusError(
                        f"Error getting {endpoint}: {response.status_code} {response.text}",
                        request=response.request,
                        response=response,
                    )
            return response

    async def post(self, endpoint: str, **kwargs):
        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.post(f"{self.base_url}{endpoint}", **kwargs)
            return response.json()

    async def post_bytes(self, endpoint: str, **kwargs) -> bytes:
        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.post(f"{self.base_url}{endpoint}", **kwargs)
            return response.content

    async def put(self, endpoint: str, **kwargs):
        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.put(f"{self.base_url}{endpoint}", **kwargs)
            return response.json()

    async def put_bytes(self, endpoint: str, **kwargs) -> bytes:
        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.put(f"{self.base_url}{endpoint}", **kwargs)
            return response.content

    async def delete(self, endpoint: str, **kwargs):
        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.delete(f"{self.base_url}{endpoint}", **kwargs)
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                return response.text
