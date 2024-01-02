from typing import Optional

from pydantic import BaseModel, Field


class ExamplePayload(BaseModel):
    name: str = Field(title="Example name", max_length=20)
    description: Optional[str] = Field(title="Example description", max_length=1024, default="")


class ExampleCreateResponse(BaseModel):
    example_id: int


# this maps to Example DB model
class ExampleGetResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    message: str


class OkResponse(BaseModel):
    message: str


NOT_FOUND_RESPONSE = {"model": ErrorResponse, "description": "Item was not found"}
DUPLICATE_RESPONSE = {"model": ErrorResponse, "description": "Item already exists"}
OK_RESPONSE = {"model": OkResponse, "description": "Success"}
