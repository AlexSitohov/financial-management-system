import logging

from jose import jwt
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from pydantic import ValidationError

from app.core import config
from app.models.users_model import UsersModel
from app.services.jwt_service import JWTService


class NoJWTHandler:
    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service
        self.logger = logging.getLogger(__name__)

    async def login(self, request: Request) -> Response:
        url = config.DOMAIN_MAPPER["users"]
        body = await request.json()
        try:
            user = UsersModel.LOGIN(**body)

        except ValidationError:
            return Response(status_code=400)

        async with AsyncClient(timeout=600) as client:
            response = await client.post(f"{url}/users/api/v1/login", json=user.dict())
        if response.status_code != 200:
            return Response(content=response.text, status_code=response.status_code)
        response_json = response.json()

        access_token = self.jwt_service.create_access_token(
            user_id=response_json["_id"], user_email=response_json["email"]
        )

        return JSONResponse(content={"access_token": access_token})

    async def registration(self, request: Request) -> Response:
        url = config.DOMAIN_MAPPER["users"]
        body = await request.json()
        try:
            user = UsersModel.REGISTRATION(**body)

        except ValidationError:
            return Response(status_code=400)

        async with AsyncClient(timeout=600) as client:
            response = await client.post(
                f"{url}/users/api/v1/registration", json=user.dict()
            )
        if response.status_code != 200:
            return Response(content=response.text, status_code=response.status_code)
        response_json = response.json()

        return JSONResponse(content=response_json)
