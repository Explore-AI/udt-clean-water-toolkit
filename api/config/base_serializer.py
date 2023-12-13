from pydantic import BaseModel


class BaseSerializer(BaseModel):
    class Config:
        from_attributes = True
