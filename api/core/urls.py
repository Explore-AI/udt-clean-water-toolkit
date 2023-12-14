# from config.routers import BaseRouter
from config.routers import BaseRouter
from core.controllers.user_controller import UserController

# router = BaseRouter()
router = BaseRouter(path="/core/user", UserController, tags=["user"])
