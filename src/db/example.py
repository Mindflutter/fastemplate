from sqlalchemy import String, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from db.database import db
from db.model_base import Base
from example.models import ExampleCreateResponse, ExamplePayload


class Example(Base):  # type: ignore
    __tablename__ = "example"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str | None] = mapped_column(String(1024))

    @classmethod
    async def check_example_exists(cls, session: AsyncSession, example_id: int) -> None:
        # check if item exists in the db
        check_query = select(1).where(Example.id == example_id)
        results = await session.execute(check_query)
        # NoResultFound will be raised here if item does not exist
        results.one()

    @classmethod
    async def create(cls, payload: ExamplePayload) -> ExampleCreateResponse:
        example = Example(name=payload.name, description=payload.description)
        async with db.session_maker() as session:
            session.add(example)
            await session.commit()
        return ExampleCreateResponse(example_id=example.id)

    @classmethod
    async def get(cls, example_id: int):  # type: ignore
        async with db.session_maker() as session:
            query = select(Example).where(Example.id == example_id)
            results = await session.execute(query)
            (result,) = results.one()
            return result

    @classmethod
    async def update(cls, example_id: int, payload: ExamplePayload) -> None:
        async with db.session_maker() as session:
            await cls.check_example_exists(session, example_id)
            query = (
                update(Example)
                .where(Example.id == example_id)
                .values(name=payload.name, description=payload.description)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, example_id: int) -> None:
        async with db.session_maker() as session:
            await cls.check_example_exists(session, example_id)
            query = delete(Example).where(Example.id == example_id)
            await session.execute(query)
            await session.commit()
