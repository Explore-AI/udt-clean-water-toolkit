from rest_framework import viewsets
from config.filters.base_filter import BaseFilter

# from config.filters.base_filter_backend import BaseFilterBackend
from rest_framework import renderers


class BaseModelViewSet(viewsets.ModelViewSet):
    #    filter_backends = (BaseFilterBackend,)
    filterset_class = BaseFilter
    renderer_classes = [renderers.JSONRenderer]
    handler500 = "rest_framework.exceptions.server_error"
