from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class BaseHttpError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Unexpected exception"

    def __init__(self, status_code: int | None = None, message: str | None = None) -> None:
        self.status_code = status_code or self.status_code
        self.message = message or self.message
        super().__init__()


class ErrorResponse(BaseModel):
    message: str


async def error_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    base_error = BaseHttpError()
    content = ErrorResponse(
        message=getattr(exc, "message", base_error.message),
    ).model_dump()
    return JSONResponse(
        status_code=status_code,
        content=content,
    )


class NotFoundError(BaseHttpError):
    message = "Entity not found"
    status_code = 404


class BadRequestError(BaseHttpError):
    message = "Bad request"
    status_code = 400


class ConflictError(BaseHttpError):
    message = "Conflict / duplicate error"
    status_code = 409
