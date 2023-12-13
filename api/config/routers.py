from fastapi import APIRouter


class BaseRouter(APIRouter):
    def __init__(self, controller=None, *args, **kwargs):
        self.controller = controller
        super().__init__(*args, **kwargs)


class RouterUtils:
    # https://stackoverflow.com/a/66472528
    @classmethod
    def generate_routers(cls, app, url_routes):
        for route in url_routes:
            full_url = f"{route[0]}{route[1].prefix}"
            route[1].prefix = full_url
            app.include_router(route[1])


# from collections import namedtuple

# Route = namedtuple("Route", ["url", "mapping", "name", "detail", "initkwargs"])
# DynamicRoute = namedtuple("DynamicRoute", ["url", "name", "detail", "initkwargs"])


# class BaseRouter():
#     routes = [
#         # List route.
#         Route(
#             url=r"^{prefix}{trailing_slash}$",
#             mapping={"get": "list", "post": "create"},
#             name="{basename}-list",
#             detail=False,
#             initkwargs={"suffix": "List"},
#         ),
#         # Dynamically generated list routes. Generated using
#         # @action(detail=False) decorator on methods of the viewset.
#         DynamicRoute(
#             url=r"^{prefix}/{url_path}{trailing_slash}$",
#             name="{basename}-{url_name}",
#             detail=False,
#             initkwargs={},
#         ),
#         # Detail route.
#         Route(
#             url=r"^{prefix}/{lookup}{trailing_slash}$",
#             mapping={
#                 "get": "retrieve",
#                 "put": "update",
#                 "patch": "partial_update",
#                 "delete": "destroy",
#             },
#             name="{basename}-detail",
#             detail=True,
#             initkwargs={"suffix": "Instance"},
#         ),
#         # Dynamically generated detail routes. Generated using
#         # @action(detail=True) decorator on methods of the viewset.
#         DynamicRoute(
#             url=r"^{prefix}/{lookup}/{url_path}{trailing_slash}$",
#             name="{basename}-{url_name}",
#             detail=True,
#             initkwargs={},
#         ),
#     ]

#     def __init__(self):
#         self.registry = []

#     def register(self, prefix, viewset, basename=None):
#         if basename is None:
#             basename = self.get_default_basename(viewset)

#         if self.is_already_registered(basename):
#             msg = (
#                 f'Router with basename "{basename}" is already registered. '
#                 f'Please provide a unique basename for viewset "{viewset}"'
#             )
#             raise Exception("Improperly configured route.")

#         self.registry.append((prefix, viewset, basename))

#         # invalidate the urls cache
#         if hasattr(self, "_urls"):
#             del self._urls

#     def is_already_registered(self, new_basename):
#         """
#         Check if `basename` is already registered
#         """
#         return any(
#             basename == new_basename for _prefix, _viewset, basename in self.registry
#         )

#     def get_default_basename(self, viewset):
#         """
#         If `basename` is not specified, attempt to automatically determine
#         it from the viewset.
#         """
#         raise NotImplementedError("get_default_basename must be overridden")

#     def get_urls(self):
#         """
#         Return a list of URL patterns, given the registered viewsets.
#         """
#         raise NotImplementedError("get_urls must be overridden")

#     @property
#     def urls(self):
#         if not hasattr(self, "_urls"):
#             self._urls = self.get_urls()
#         return self._urls
