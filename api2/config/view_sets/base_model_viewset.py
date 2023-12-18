from rest_framework import viewsets
from django_filters import rest_framework as filters
from config.filters.base_filter import BaseFilter
from config.filters.base_filter_backend import BaseFilterBackend
from config.lib.auth import get_azure_user_from_token
from rest_framework.exceptions import APIException
from rest_framework import renderers


class BaseModelViewSet(viewsets.ModelViewSet):
    filter_backends = (BaseFilterBackend,)
    filterset_class = BaseFilter
    renderer_classes = [renderers.JSONRenderer]
    handler500 = "rest_framework.exceptions.server_error"

    def __init__(self, *args, **kwargs):
        self.user_data = None
        self.user = None
        super(BaseModelViewSet, self).__init__(*args, **kwargs)
