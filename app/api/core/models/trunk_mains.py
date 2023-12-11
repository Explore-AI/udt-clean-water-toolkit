from tortoise.models import Model
from tortoise import fields


class TrunkMains(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.name
