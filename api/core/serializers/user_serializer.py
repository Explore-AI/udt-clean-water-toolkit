from typing import Optional
from datetime import datetime
from pydantic import Field
from config.base_serializer import BaseSerializer
from core.models import User


class UserSerializer(BaseSerializer):
    id: int = Field(frozen=True)
    is_active: bool = Field(frozen=True)
    created_at: datetime = Field(frozen=True)
    modified_at: datetime = Field(frozen=True)

    class Meta:
        model = User
