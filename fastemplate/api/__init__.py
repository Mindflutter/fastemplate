from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from fastemplate.api.example import example_router

main_router = APIRouter()


async def healthcheck(_request: Request) -> Response:
    return Response()


main_router.include_router(example_router)
