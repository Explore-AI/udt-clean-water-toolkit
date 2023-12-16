from config.controllers import ModelController
from core.models import User
from sqlalchemy import select
from core.serializers.user_serializer import UserSerializer, UserCreateSerializer


class UserController(ModelController):
    Model = User
    # db_query = select(Model).where(Model.first_name == "spongebob")
    serializer_class = UserSerializer
    allowed_methods = ["get", "post"]

    def get_serializer_class(self):
        if self.get_request_method() == "post":
            return UserCreateSerializer
        return self.serializer_class
