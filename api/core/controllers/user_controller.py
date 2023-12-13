from config.base_controllers import ModelController
from core.models import User
from sqlalchemy import select
from core.serializers.user_serializer import UserSerializer


class UserController(ModelController):
    Model = User
    # query = select(User).where(User.email == "fsdfsd@gdgd.com")
    serializer_class = UserSerializer
