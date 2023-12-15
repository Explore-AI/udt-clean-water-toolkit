# from config.routers import BaseRouter
from config.routers import ModelRouter
from core.controllers.user_controller import UserController

# router = BaseRouter()
router = ModelRouter("/core/user", controller=UserController, tags=["user"])
