import logging
import os
from fastapi import FastAPI

from app.core.config import db_config
from app.dblayer.connection import get_mongo_client
from app.handlers.v1.zxc import zxc_router
from app.repositories.providers import (
    provide_zxc_repository,
    provide_zxc_repository_stub,
)


class Application:
    def __init__(self):
        self.app = self._setup_app()
        self._configure_logging()

    @staticmethod
    def _setup_app() -> FastAPI:
        return FastAPI(
            title="zxc API",
            docs_url="/zxc/api/docs",
            redoc_url="/zxc/api/redoc",
            openapi_url="/zxc/api/openapi.json",
        )

    def _connect_to_mongo(self):
        self.mongo_client = get_mongo_client(db_config)

    def _create_repositories(self):
        self.zxc_repository = lambda: provide_zxc_repository(self.mongo_client)

    def _override_dependencies(self):
        self.app.dependency_overrides[provide_zxc_repository_stub] = self.zxc_repository

    def _add_routes(self):
        self.app.include_router(zxc_router)

    @staticmethod
    def _configure_logging():
        FORMAT = "%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s"
        LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
        logging.basicConfig(level=LEVEL, format=FORMAT)

    def build_application(self):
        self._connect_to_mongo()
        self._create_repositories()
        self._override_dependencies()
        self._add_routes()
        self._configure_logging()

        return self.app
