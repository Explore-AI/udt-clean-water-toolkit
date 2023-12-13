# from config.routers import BaseRouter
from config.routers import BaseRouter
from core.controllers.user_controller import UserController

# router = BaseRouter()


router = BaseRouter(prefix="/user", controller=UserController, tags=["user"])
