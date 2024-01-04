from fastapi import FastAPI, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
import os

app = FastAPI()

# Секретный ключ для подписи JWT
SECRET_KEY = os.getenv("SECRET_KEY", "secret")

# Алгоритм для подписи JWT
ALGORITHM = os.getenv("ALGORITHM", "HS256")


class JWTBearer(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=False)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        is_valid: bool = False

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            is_valid = True
        except JWTError:
            is_valid = False

        return is_valid


# Middleware для проверки JWT на каждый запрос
class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/users/api/v1/login":
            return await call_next(request)
        await JWTBearer()(request)
        return await call_next(request)
