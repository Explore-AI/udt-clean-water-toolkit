from cwageodjango.assets.models import NetworkOptValve
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from ..serializers import NetworkOptValveSerializer


class NetworkOptValveFilter(BaseFilter):

    class Meta:
        model = NetworkOptValve
        fields = ["id", "gid"]


class NetworkOptValveViewSet(BaseModelViewSet):
    queryset = NetworkOptValve.objects.all()
    serializer_class = NetworkOptValveSerializer
    filterset_class = NetworkOptValveFilter
    http_method_names = ["get"]
