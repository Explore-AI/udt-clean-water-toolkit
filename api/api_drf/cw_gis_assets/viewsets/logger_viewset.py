from cwageodjango.assets.models import Logger
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from ..serializers import LoggerSerializer


class LoggerFilter(BaseFilter):

    class Meta:
        model = Logger
        fields = ["id", "gid"]


class LoggerViewSet(BaseModelViewSet):
    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer
    filterset_class = LoggerFilter
    http_method_names = ["get"]
