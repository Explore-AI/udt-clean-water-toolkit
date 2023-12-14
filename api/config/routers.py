from fastapi import APIRouter


class BaseRouter(APIRouter):
    def __init__(self, path: str, controller, *args, **kwargs):
        # https://stackoverflow.com/a/70563827
        self.path = path
        self.controller = controller
        self.router = APIRouter(*args, **kwargs)

    def get(self, path, *args, **kwargs):
        path = path or self.path
        set_api_route = self.router.get(path, *args, **kwargs)

        set_api_route(self.controller.list)


class RouterUtils:
    # https://stackoverflow.com/a/66472528
    @classmethod
    def generate_routers(cls, app, url_routers):
        for router in url_routers:
            # router[1].prefix = router[0]
            app.include_router(router[1].router)
