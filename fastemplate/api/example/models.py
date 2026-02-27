import datetime as dt

from pydantic import BaseModel, Field


class CreateExamplePayload(BaseModel):
    name: str = Field(max_length=30)
    description: str | None = Field(max_length=1024, default=None)


class CreateExampleResponse(BaseModel, from_attributes=True):
    id: int


class ExampleItem(BaseModel, from_attributes=True):
    id: int
    name: str
    description: str | None
    created_at: dt.datetime
    updated_at: dt.datetime


class GetExamplesResponse(BaseModel):
    items: list[ExampleItem]
    total: int
