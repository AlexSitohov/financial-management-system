import logging

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core import exceptions


def jwt_exception_handler(request, exc: exceptions.JWTException) -> JSONResponse:
    msg = {"Message": "This token is not valid", "Details": exc.details}
    logging.error(msg)

    return JSONResponse(
        status_code=403,
        content={
            "Message": exc.message,
            "Code": exc.code,
        },
    )


def no_permission_exception_handler(
    request, exc: exceptions.NoPermissionException
) -> JSONResponse:
    msg = {
        "Message": f"User has no permission to access {request.url.path}",
        "Details": exc.details,
    }
    logging.error(msg)

    return JSONResponse(
        status_code=403,
        content={
            "Message": exc.message,
            "Code": exc.code,
        },
    )


def not_authorized_exception_handler(
    request, exc: exceptions.NotAuthorizedException
) -> JSONResponse:
    msg = {
        "Message": f"User {request.headers['x-telematix-login']} has not authorized",
        "Details": exc.details,
    }
    logging.info(msg)
    return JSONResponse(
        status_code=403,
        content={
            "Message": exc.message,
            "Code": exc.code,
        },
    )


def bad_request_exception_handler(
    request, exc: exceptions.BadRequestException
) -> JSONResponse:
    msg = {"Message": exc.message, "Details": exc.details}
    logging.error(msg)

    return JSONResponse(
        status_code=400,
        content={
            "Message": exc.message,
            "Code": exc.code,
        },
    )


def conflict_exception_handler(
    request, exc: exceptions.ConflictException
) -> JSONResponse:
    msg = {"Message": exc.message, "Details": exc.details}
    logging.error(msg)

    return JSONResponse(
        status_code=409,
        content={
            "Message": exc.message,
            "Code": exc.code,
        },
    )


def not_found_exception_handler(
    request, exc: exceptions.NotFoundException
) -> JSONResponse:
    msg = {"Message": exc.message, "Details": exc.details}
    logging.error(msg)

    return JSONResponse(
        status_code=404,
        content={
            "Message": exc.message,
            "Code": exc.code,
        },
    )


def no_internal_service_exception_handler(
    request, exc: exceptions.NoInternalServiceException
) -> JSONResponse:
    msg = {"Message": exc.message, "Details": exc.details}
    logging.error(msg)

    return JSONResponse(
        status_code=404,
        content={
            "Message": exc.message,
            "Code": exc.code,
        },
    )


def unexpected_server_exception_handler(
    request, exc: exceptions.UnexpectedServerException
) -> JSONResponse:
    msg = {"Message": exc.message, "Details": exc.details}
    logging.error(msg)

    return JSONResponse(
        status_code=500,
        content={
            "Message": exc.message,
            "Code": exc.code,
        },
    )


def service_unavailable_exception_handler(
    request, exc: exceptions.ServiceUnavailableException
) -> JSONResponse:
    msg = {"Message": exc.message, "Details": exc.details}
    logging.error(msg)

    return JSONResponse(
        status_code=503,
        content={
            "Message": exc.message,
            "Code": exc.code,
        },
    )


def request_validation_error_exception_handler(
    request, exc: RequestValidationError
) -> JSONResponse:
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"])
        message = error["msg"]
        errors.append({"field": field, "message": message})

    return bad_request_exception_handler(
        request, exceptions.BadRequestException(details=errors)
    )
