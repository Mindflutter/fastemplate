from enum import StrEnum


class Tags(StrEnum):
    example = "Example"


tags_metadata = [
    {
        "name": Tags.example,
        "description": "Example API",
    },
]
