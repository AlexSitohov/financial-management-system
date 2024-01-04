from dataclasses import dataclass


class ApiException(Exception):
    pass


@dataclass
class BadRequestException(ApiException):
    message: str = "Неверные данные запроса"
    code: str = "B001"
    details: list | str | None = None


@dataclass
class NotAuthorizedException(ApiException):
    message: str = "Не авторизован"
    code: str = "B002"
    details: str | None = None


@dataclass
class JWTException(ApiException):
    message: str = "Ошибка токена"
    code: str = "B003"
    details: str | None = None


@dataclass
class ConflictException(ApiException):
    message: str = "Конфликт данных"
    code: str = "B004"
    details: str | None = None


@dataclass
class NotFoundException(ApiException):
    message: str = "Данные не найдены"
    code: str = "B005"
    details: str | None = None


@dataclass
class NoInternalServiceException(ApiException):
    message: str = "Внутренний сервис не найден"
    code: str = "B006"
    details: str | None = None


@dataclass
class NoPermissionException(ApiException):
    message: str = "Нет прав на выполнение операции"
    code: str = "P001"
    details: str | None = None


@dataclass
class UnexpectedServerException(ApiException):
    message: str = "Непредвиденная ошибка сервера"
    code: str = "S001"
    details: str | None = None


@dataclass
class ServiceUnavailableException(ApiException):
    message: str = "Один из сервисов временно недоступен"
    code: str = "S002"
    details: str | None = None
