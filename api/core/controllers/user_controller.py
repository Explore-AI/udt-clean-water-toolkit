from config.base_controllers import ModelController
from core.models import User
from core.serializers.user_serializer import UserSerializer


class UserController(ModelController):
    queryset = User
    serializer_class = UserSerializer
