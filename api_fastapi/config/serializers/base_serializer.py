from typing import Any
from pydantic import BaseModel


class BaseSerializer(BaseModel):
    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)

    class Config:
        from_attributes = True
        validate_assignment = True
