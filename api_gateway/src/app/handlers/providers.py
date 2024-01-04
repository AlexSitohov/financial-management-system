from app.handlers.bff_handler import BFFHandler
from app.handlers.no_jwt_handler import NoJWTHandler
from app.services.jwt_service import JWTService


def provide_bff_handler():
    return BFFHandler()


def provide_no_jwt_handler(jwt_service: JWTService) -> NoJWTHandler:
    return NoJWTHandler(
        jwt_service,
    )
