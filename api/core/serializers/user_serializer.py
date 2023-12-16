from typing import Optional, Union
from datetime import datetime
from pydantic import Field
from config.serializers import BaseSerializer
from core.models import User


class UserSerializer(BaseSerializer):
    id: Union[int, None] = None
    is_active: Union[int, None] = None
    first_name: Union[str, None] = None
    created_at: Union[datetime, None] = None
    modified_at: Union[datetime, None] = None

    class Meta:
        model = User


class UserCreateSerializer(UserSerializer):
    # id: int = Field(frozen=True)
    first_name: str = Field(...)
    # created_at: datetime = Field(frozen=True)
    # modified_at: datetime = Field(frozen=True)

    class Meta:
        model = User
