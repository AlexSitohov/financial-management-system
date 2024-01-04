from app.core.config import jwt_settings
from app.services.jwt_service import JWTService


def provide_jwt_service() -> JWTService:
    return JWTService(
        secret_key=jwt_settings.secret_key,
        algorithm=jwt_settings.algorithm,
    )
