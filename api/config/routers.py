from fastapi import APIRouter


class BaseRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ModelRouter(BaseRouter):
    def __init__(self, url: str, controller, *args, **kwargs):
        # https://stackoverflow.com/a/70563827
        self.url = url
        self.controller = controller

        super().__init__(*args, **kwargs)
        self._get()

    def _get(self, *args, **kwargs):
        set_api_route = super().get(self.url, *args, **kwargs)
        # attr = dict(self.controller().get_attr()) | dict(
        #     self.controller.__dict__.items()
        # )
        set_api_route(self.controller.list_data)


class RouterUtils:
    # https://stackoverflow.com/a/66472528
    @staticmethod
    def generate_routers(app, url_routers):
        for router in url_routers:
            app.include_router(router[1])
