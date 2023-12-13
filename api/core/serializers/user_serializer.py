from config.base_serializer import BaseSerializer


class User(BaseSerializer):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
