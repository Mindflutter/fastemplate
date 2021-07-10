from sqlalchemy import Column, Integer, String, select

from db import Base
from db.database import db
from example.models import ExamplePayload, ExampleResponse


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

    @classmethod
    async def create(cls, payload: ExamplePayload):
        example = Example(name=payload.name, description=payload.description)
        async with db.session_maker() as session:
            session.add(example)
            await session.commit()
        return ExampleResponse(example_id=example.id)

    @classmethod
    async def get(cls, example_id: int):
        async with db.session_maker() as session:
            query = select(Example).where(Example.id == example_id)
            results = await session.execute(query)
            (result,) = results.one()
            return result
