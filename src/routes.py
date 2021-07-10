from fastapi import APIRouter

from example.views import router as example_router
from service.views import router as service_router

main_router = APIRouter()
main_router.include_router(service_router, tags=["service"])
main_router.include_router(example_router, tags=["example"])
