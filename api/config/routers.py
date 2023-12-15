from typing import Callable, Optional
from fastapi import APIRouter


class BaseRouter(APIRouter):
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
        self.get_list()

    def get_list(self):
        kwargs = self.controller().set_get_args()
        set_api_route = super().get(self.url, *query_params, **kwargs)
        # attr = dict(self.controller().get_attr()) | dict(
        #     self.controller.__dict__.items()
        # )
        set_api_route(self.controller.list)


class RouterUtils:
    # https://stackoverflow.com/a/66472528
    @staticmethod
    def generate_routers(app, url_routers):
        for router in url_routers:
            app.include_router(router[1])
