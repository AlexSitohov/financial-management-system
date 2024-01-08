from fastapi import FastAPI

from app.builder import Application


def get_app() -> FastAPI:
    application = Application()
    return application.build_application()


app: FastAPI = get_app()
