from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api_clients.providers import provide_users_client
from app.handlers.providers import provide_bff_handler, provide_no_jwt_handler
from app.services.providers import provide_jwt_service

from app.middlewares.jwt import jwt_middleware


class Application:
    def __init__(
        self,
    ):
        self.app = self._setup_app()
        self.create_clients()
        self.create_services()

    @staticmethod
    def _setup_app():
        return FastAPI(
            title="Api gateway service",
            docs_url="/api_gateway/api/swagger",
            openapi_url="/api_gateway/api/openapi.json",
            default_response_class=ORJSONResponse,
        )

    def create_clients(self):
        self.users_client = provide_users_client()

    def create_services(self):
        self.jwt_service = provide_jwt_service()

    def create_middleware(self):
        self.app.middleware("http")(jwt_middleware)

    def add_other_services(self):
        bff_handler = provide_bff_handler()
        jwt_service = provide_jwt_service()
        no_jwt_handler = provide_no_jwt_handler(jwt_service)
        self.app.add_route(
            "/users/api/v1/registration", no_jwt_handler.registration, methods=["POST"]
        )
        self.app.add_route(
            "/users/api/v1/login", no_jwt_handler.login, methods=["POST"]
        )

        self.app.add_route(
            "/{tail:path}",
            bff_handler.reroute_to_appropriate_service,
            methods=["GET", "POST", "PUT", "DELETE"],
        )

    def build_application(self) -> FastAPI:
        self.create_middleware()
        self.add_other_services()
        return self.app
