import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from db.models import Example
from example.models import ErrorResponse, ExamplePayload, ExampleResponse

router = APIRouter(prefix="/example")
logger = logging.getLogger(__name__)


@router.post("/", response_model=ExampleResponse, responses={409: {"model": ErrorResponse}})
async def example_post(example_payload: ExamplePayload):
    try:
        result = await Example.create(example_payload)
        return result
    except IntegrityError:
        logger.error(f"Name {example_payload.name} already exists")
        return JSONResponse(status_code=409, content={"message": f"Name {example_payload.name} already exists"})


@router.get("/{example_id}")
async def example_get(example_id: int):
    result = await Example.get(example_id)
    return result
