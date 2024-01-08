import os
from typing import Callable

from fastapi import Request
from jose import jwt
from starlette.responses import JSONResponse

from app.services.providers import provide_jwt_service

# Секретный ключ для подписи JWT
SECRET_KEY = os.getenv("SECRET_KEY", "secret")

# Алгоритм для подписи JWT
ALGORITHM = os.getenv("ALGORITHM", "HS256")

jwt_service = provide_jwt_service()


async def jwt_middleware(request: Request, call_next: Callable):
    if request.url.path == "/users/api/v1/login":
        return await call_next(request)
    elif request.url.path == "/users/api/v1/registration":
        return await call_next(request)

    # Извлекаем токен из заголовков
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        return JSONResponse(
            content="Отсутствует заголовок Authorization", status_code=401
        )

    try:
        token = authorization.split(" ")[1]
        payload = jwt_service.extract_info_from_jwt(token)

        # Заполняем request.state данными из JWT
        request.state.user_id = payload.get("user_id")
        request.state.user_email = payload.get("user_email")

    except KeyError:
        return JSONResponse(
            content="JWT не содержит необходимых полей", status_code=401
        )
    except jwt.exceptions.InvalidSignatureError:
        return JSONResponse(content="Ошибка проверки подписи", status_code=401)
    except jwt.ExpiredSignatureError:
        return JSONResponse(content="Просроченная подпись", status_code=401)
    except jwt.exceptions.InvalidTokenError:
        return JSONResponse(content="Недействительный JWT", status_code=401)
    except Exception as e:
        # Логгирование исключения может помочь при отладке
        print(f"Unexpected error: {e}")
        return JSONResponse(content="Произошла неожиданная ошибка", status_code=500)

    # Выполняем следующий запрос в обработчике
    return await call_next(request)
