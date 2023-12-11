from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class BaseModel(models.Model):

    id = fields.IntField(pk=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ["id"]
