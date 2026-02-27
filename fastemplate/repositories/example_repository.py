from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError

from fastemplate.common.errors import DatabaseError
from fastemplate.repositories.base import BaseRepository
from fastemplate.repositories.models import CreateExampleDTO, ExampleDTO, GetExamplesResult
from fastemplate.repositories.tables import example_tbl


class ExampleRepository(BaseRepository):
    async def create_example(self, dto: CreateExampleDTO) -> int:
        query = insert(example_tbl).values(name=dto.name, description=dto.description).returning(example_tbl.c.id)
        try:
            async with self._engine.get_connection() as conn:
                result = await conn.execute(query)
        except IntegrityError as err:
            raise DatabaseError(message=str(err.orig)) from err
        return int(result.scalar_one())

    async def get_example_by_id(self, example_id: int) -> ExampleDTO | None:
        query = select(example_tbl).where(example_tbl.c.id == example_id)
        async with self._engine.get_connection() as conn:
            result = await conn.execute(query)
            row = result.mappings().first()
        return ExampleDTO(**row) if row else None

    async def get_examples(self, limit: int, page: int) -> GetExamplesResult:
        offset = (page - 1) * limit
        query = select(example_tbl).order_by(example_tbl.c.id.desc()).limit(limit).offset(offset)
        total_query = select(func.count()).select_from(example_tbl)

        async with self._engine.get_connection() as conn:
            items = await conn.execute(query)
            total = (await conn.execute(total_query)).scalar_one()

        return GetExamplesResult(items=[ExampleDTO(**row) for row in items.mappings()], total=total)

    async def update_example(self, example_id: int, dto: CreateExampleDTO) -> ExampleDTO | None:
        query = (
            update(example_tbl)
            .values(name=dto.name, description=dto.description)
            .where(example_tbl.c.id == example_id)
            .returning(example_tbl)
        )
        try:
            async with self._engine.get_connection() as conn:
                result = await conn.execute(query)
                row = result.mappings().first()
        except IntegrityError as err:
            raise DatabaseError(message=str(err.orig)) from err
        return ExampleDTO(**row) if row else None

    async def delete_example(self, example_id: int) -> bool:
        query = delete(example_tbl).where(example_tbl.c.id == example_id)
        async with self._engine.get_connection() as conn:
            result = await conn.execute(query)
        return result.rowcount > 0
