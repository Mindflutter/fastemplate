from fastapi import APIRouter

from service.views import router as service_router


main_router = APIRouter()
main_router.include_router(service_router, tags=["service"])
