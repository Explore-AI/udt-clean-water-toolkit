from datetime import datetime
from config.base_serializer import BaseSerializer
from core.models import User


class UserSerializer(BaseSerializer):
    id: int
    is_active: bool
    created_at: datetime
    modified_at: datetime

    class Meta:
        model = User
