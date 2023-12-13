from pydantic import BaseModel


class BaseSerializer(BaseModel):
    class Config:
        orm_mode = True
