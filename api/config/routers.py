from fastapi import APIRouter


class BaseRouter(APIRouter):
    def __init__(self, url: str, controller, *args, **kwargs):
        # https://stackoverflow.com/a/70563827
        self.url = url
        self.controller = controller
        self.router = APIRouter()
        self.get(self.url)

    def get(self, url, *args, **kwargs):
        url = url or self.url
        set_api_route = self.router.get(url)
        set_api_route(self.controller.list)


class RouterUtils:
    # https://stackoverflow.com/a/66472528
    @classmethod
    def generate_routers(cls, app, url_routers):
        for router in url_routers:
            # router[1].prefix = router[0]
            print("gggg")
            print(router[1].__dict__)
            app.include_router(router[1].router)
