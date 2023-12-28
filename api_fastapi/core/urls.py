# from config.routers import BaseRouter
from config.routers import ModelRouter
from core.controllers.user_controller import UserController


router = ModelRouter("/user", controller=UserController, prefix="/core", tags=["user"])
