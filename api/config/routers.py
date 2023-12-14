from fastapi import APIRouter
import inspect


def Convert(tup, di):
    di = dict(tup)
    return di


class BaseRouter(APIRouter):
    def __init__(self, url: str, controller, *args, **kwargs):
        # https://stackoverflow.com/a/70563827
        self.url = url
        self.controller = controller

        super().__init__(*args, **kwargs)
        self.get(self.url)

    def get(self, url, *args, **kwargs):
        url = url or self.url
        set_api_route = super().get(url)
        # attr = dict(self.controller().get_attr()) | dict(
        #     self.controller.__dict__.items()
        # )
        set_api_route(self.controller.list)


class RouterUtils:
    # https://stackoverflow.com/a/66472528
    @classmethod
    def generate_routers(cls, app, url_routers):
        for router in url_routers:
            app.include_router(router[1])
