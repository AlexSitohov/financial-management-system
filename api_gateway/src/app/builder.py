from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api_clients._providers import provide_users_client
from app.handlers.providers import provide_bff_handler


class Application:
    def __init__(self, ):
        self.app = self._setup_app()
        self.create_clients()

    def _setup_app(self):
        return FastAPI(
            title="Api gateway service",
            docs_url="/api_gateway/api/swagger",
            openapi_url="/api_gateway/api/openapi.json",
            default_response_class=ORJSONResponse,
        )

    def create_clients(self):
        self.users_client = provide_users_client()

    def add_other_services(self):
        bff_handler = provide_bff_handler()

        self.app.add_route(
            "/{tail:path}", bff_handler.reroute_to_appropriate_service, methods=["GET", "POST", "PUT", "DELETE"]
        )

    def build_application(self) -> FastAPI:
        self.add_other_services()
        return self.app
