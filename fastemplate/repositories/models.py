import datetime as dt
from dataclasses import dataclass


@dataclass
class CreateExampleDTO:
    name: str
    description: str | None = None


@dataclass
class ExampleDTO:
    id: int
    name: str
    description: str | None
    created_at: dt.datetime
    updated_at: dt.datetime


@dataclass
class GetExamplesResult:
    items: list[ExampleDTO]
    total: int
