from typing import Annotated

from fastapi import Depends

from fastemplate.api.common.dependencies import engine_dep
from fastemplate.repositories.engine import Engine
from fastemplate.repositories.example_repository import ExampleRepository
from fastemplate.services.example import ExampleService


async def example_repository_dep(engine: Annotated[Engine, Depends(engine_dep)]) -> ExampleRepository:
    return ExampleRepository(engine=engine)


async def example_service_dep(
    example_repository: Annotated[ExampleRepository, Depends(example_repository_dep)],
) -> ExampleService:
    return ExampleService(example_repository=example_repository)
