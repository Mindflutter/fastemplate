from fastemplate.repositories.example_repository import ExampleRepository
from fastemplate.repositories.models import CreateExampleDTO, ExampleDTO, GetExamplesResult


class ExampleService:
    def __init__(self, example_repository: ExampleRepository) -> None:
        self._repository = example_repository

    async def create_example(self, dto: CreateExampleDTO) -> int:
        return await self._repository.create_example(dto)

    async def get_example_by_id(self, example_id: int) -> ExampleDTO | None:
        return await self._repository.get_example_by_id(example_id)

    async def get_examples(self, limit: int, page: int) -> GetExamplesResult:
        return await self._repository.get_examples(limit=limit, page=page)

    async def update_example(self, example_id: int, dto: CreateExampleDTO) -> ExampleDTO | None:
        return await self._repository.update_example(example_id=example_id, dto=dto)

    async def delete_example(self, example_id: int) -> bool:
        return await self._repository.delete_example(example_id)
