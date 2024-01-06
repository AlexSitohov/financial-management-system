from datetime import datetime, timedelta
from typing import Any

from jose import jwt


class JWTService:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, user_id, user_email) -> str:
        expire = datetime.utcnow() + timedelta(minutes=int(10000))
        return jwt.encode(
            {"user_id": user_id, "user_email": user_email, "exp": expire},
            self.secret_key,
            self.algorithm,
        )

    def extract_info_from_jwt(self, encoded: str) -> dict[str, str | Any]:
        payload = jwt.decode(encoded, self.secret_key, self.algorithm)
        return payload

    def validate_token(self, encoded: str) -> bool:
        try:
            jwt.decode(encoded, self.secret_key, algorithms=[self.algorithm])
            return True
        except Exception:
            return False
