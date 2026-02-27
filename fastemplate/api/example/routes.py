from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from fastemplate.api.common.errors import BadRequestError, ConflictError, NotFoundError
from fastemplate.api.common.models import Tags
from fastemplate.api.example.dependencies import example_service_dep
from fastemplate.api.example.models import (
    CreateExamplePayload,
    CreateExampleResponse,
    ExampleItem,
    GetExamplesResponse,
)
from fastemplate.common.errors import DatabaseError
from fastemplate.repositories.models import CreateExampleDTO
from fastemplate.services.example import ExampleService

example_router = APIRouter(tags=[Tags.example], prefix="/example")


@example_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_example(
    service: Annotated[ExampleService, Depends(example_service_dep)],
    payload: CreateExamplePayload,
) -> CreateExampleResponse:
    try:
        example_id = await service.create_example(CreateExampleDTO(name=payload.name, description=payload.description))
    except DatabaseError as err:
        raise ConflictError(message=err.message) from err
    return CreateExampleResponse(id=example_id)


@example_router.get("/{example_id}")
async def get_example(
    service: Annotated[ExampleService, Depends(example_service_dep)],
    example_id: int,
) -> ExampleItem:
    result = await service.get_example_by_id(example_id)
    if not result:
        raise NotFoundError(message=f"Example id {example_id} not found")
    return ExampleItem.model_validate(result)


@example_router.get("/")
async def get_examples(
    service: Annotated[ExampleService, Depends(example_service_dep)],
    limit: Annotated[int, Query(le=1000)] = 20,
    page: int = 1,
) -> GetExamplesResponse:
    result = await service.get_examples(limit=limit, page=page)
    return GetExamplesResponse(items=[ExampleItem.model_validate(dto) for dto in result.items], total=result.total)


@example_router.put("/{example_id}")
async def update_example(
    service: Annotated[ExampleService, Depends(example_service_dep)],
    example_id: int,
    payload: CreateExamplePayload,
) -> ExampleItem:
    dto = CreateExampleDTO(name=payload.name, description=payload.description)
    try:
        result = await service.update_example(example_id, dto)
    except DatabaseError as err:
        raise BadRequestError(message=err.message) from err
    if not result:
        raise NotFoundError(message=f"Example id {example_id} not found")
    return ExampleItem.model_validate(result)


@example_router.delete("/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example(
    service: Annotated[ExampleService, Depends(example_service_dep)],
    example_id: int,
) -> None:
    deleted = await service.delete_example(example_id)
    if not deleted:
        raise NotFoundError(message=f"Example id {example_id} not found")
