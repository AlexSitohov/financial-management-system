import json
import logging
from functools import wraps

import httpx

from app.core import exceptions

logger = logging.getLogger(__name__)


def http_exc_handler(func) -> callable:
    """
    Декоратор для обработки исключений httpx.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result

        except httpx.HTTPStatusError as e:
            response = e.response
            status_code = response.status_code
            details = response.text
            try:
                message = response.json()
            except json.decoder.JSONDecodeError:
                message = None

            match status_code:
                case 400:
                    raise exceptions.BadRequestException(details=details, message=message)
                case 403:
                    raise exceptions.NoPermissionException(details=details, message=message)
                case 404:
                    raise exceptions.NotFoundException(details=details, message=message)
                case _:
                    raise exceptions.UnexpectedServerException(details=details, message=message)
            # Обработка других кодов ошибок

        except httpx.ConnectError as e:
            logger.exception("Ошибка подключения к сервису: %s", e)
            raise exceptions.ServiceUnavailableException(
                details=str(e),
            )

    return wrapper
