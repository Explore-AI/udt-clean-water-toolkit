from config.base_controller import BaseController
from core.models import User
from core.serializers.user_serializer import UserSerializer


class UserController(BaseController):
    queryset = User
    serializer_class = UserSerializer
