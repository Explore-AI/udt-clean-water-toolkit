from tortoise.contrib.pydantic import pydantic_model_creator
from config.base_model import BaseModel


class BaseSerializer:
    pydantic_model_creator(self.Meta.model, name="BaseModel")
