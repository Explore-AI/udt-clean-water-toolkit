from typing import Callable, Optional
from fastapi import APIRouter


class BaseRouter(APIRouter):
    """This is an abstract base class. It should not be instantiated
    directly. It should only be used as an inherited class.
    """
    def __init__(self, *args, **kwargs):
        # print("aaa", args, kwargs)
        super().__init__(*args, **kwargs)


class ModelRouter(BaseRouter):
    # TO DO: add callable type for controller
    def __init__(
        self, url: str, *args, controller: Optional[Callable] = None, **kwargs
    ):
        # https://stackoverflow.com/a/70563827
        self.url = url
        self.controller = controller
        super().__init__(*args, **kwargs)
        self.set_get_route()
        self.set_post_route()
        self.set_delete_route()

    def set_get_route(self):
        kwargs = self.controller().set_get_args()
        set_api_route = super().get(self.url, **kwargs)
        set_api_route(self.controller.list)

    def set_post_route(self):
        kwargs = self.controller().set_post_args()
        set_api_route = super().post(self.url, **kwargs)
        set_api_route(self.controller.create)

    def set_delete_route(self):
        kwargs = self.controller().set_delete_args()
        set_api_route = super().delete(self.url, **kwargs)
        set_api_route(self.controller.destroy)



class RouterUtils:
    # https://stackoverflow.com/a/66472528
    @staticmethod
    def generate_routers(app, url_routers):
        for router in url_routers:
            app.include_router(router[1])
