import os

from dataclasses import dataclass


@dataclass
class JWTSettings:
    secret_key: str = os.environ["JWT_SECRET_KEY"]
    algorithm: str = os.environ["JWT_ALGORITHM"]


DOMAIN_MAPPER = {
    "users": os.environ["USERS_SERVICE_URL"],
    "transactions": os.environ["TRANSACTIONS_SERVICE_URL"],
}

jwt_settings = JWTSettings()
