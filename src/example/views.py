import logging

from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, NoResultFound

from db.example import Example
from example.models import (
    DUPLICATE_RESPONSE,
    NOT_FOUND_RESPONSE,
    ExampleCreateResponse,
    ExampleGetResponse,
    ExamplePayload,
)

router = APIRouter(prefix="/example")
logger = logging.getLogger(__name__)


@router.post("/", status_code=201, response_model=ExampleCreateResponse, responses={409: DUPLICATE_RESPONSE})
async def create_example(example_payload: ExamplePayload) -> ExampleCreateResponse | JSONResponse:
    try:
        result = await Example.create(example_payload)
        return result
    except IntegrityError:
        logger.error(f"Name {example_payload.name} already exists")
        return JSONResponse(status_code=409, content={"message": f"Name {example_payload.name} already exists"})


@router.get("/{example_id}", response_model=ExampleGetResponse, responses={404: NOT_FOUND_RESPONSE})
async def get_example(example_id: int = Path(None, gt=0)) -> ExampleGetResponse | JSONResponse:
    try:
        result = await Example.get(example_id)
        return ExampleGetResponse.from_orm(result)
    except NoResultFound:
        logger.error(f"Example id {example_id} not found")
        return JSONResponse(status_code=404, content={"message": f"Example id {example_id} not found"})


@router.put("/{example_id}", responses={404: NOT_FOUND_RESPONSE})
async def update_example(example_payload: ExamplePayload, example_id: int = Path(None, gt=0)) -> JSONResponse:
    try:
        await Example.update(example_id, example_payload)
    except NoResultFound:
        logger.error(f"Example id {example_id} not found")
        return JSONResponse(status_code=404, content={"message": f"Example id {example_id} not found"})


@router.delete("/{example_id}", responses={404: NOT_FOUND_RESPONSE})
async def delete_example(example_id: int = Path(None, gt=0)) -> JSONResponse:
    try:
        await Example.delete(example_id)
    except NoResultFound:
        logger.error(f"Example id {example_id} not found")
        return JSONResponse(status_code=404, content={"message": f"Example id {example_id} not found"})
