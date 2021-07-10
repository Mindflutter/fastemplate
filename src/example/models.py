from typing import Optional

from pydantic import BaseModel


class ExamplePayload(BaseModel):
    name: str
    description: Optional[str] = ""


class ExampleResponse(BaseModel):
    example_id: int


class ErrorResponse(BaseModel):
    message: str
