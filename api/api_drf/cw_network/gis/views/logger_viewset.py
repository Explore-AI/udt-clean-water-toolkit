from cwageodjango.assets.models.logger import Logger
from ..serializers import LoggerSerializer
from rest_framework import viewsets


class LoggerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer
    lookup_field = "gid"
