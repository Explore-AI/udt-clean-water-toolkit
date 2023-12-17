from typing import Optional, Union
from datetime import datetime
from pydantic import Field, EmailStr
from config.serializers import BaseSerializer
from core.models import User


class UserSerializer(BaseSerializer):
    id: Union[int, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    is_active: Union[int, None] = None
    created_at: Union[datetime, None] = None
    modified_at: Union[datetime, None] = None

    class Meta:
        model = User


class UserCreateSerializer(UserSerializer):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)

    class Meta:
        model = User
