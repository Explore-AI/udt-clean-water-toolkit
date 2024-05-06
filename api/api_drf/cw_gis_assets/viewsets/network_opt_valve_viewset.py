from cwageodjango.assets.models import NetworkOptValve
from config.viewsets import BaseModelViewSet, BaseGeoJsonViewSet
from config.filters import BaseFilter
from ..serializers import NetworkOptValveSerializer, NetworkOptValveGeoJsonSerializer


class NetworkOptValveFilter(BaseFilter):

    class Meta:
        model = NetworkOptValve
        fields = ["id", "gid"]


class NetworkOptValveViewSet(BaseModelViewSet):
    queryset = NetworkOptValve.objects.all()
    serializer_class = NetworkOptValveSerializer
    filterset_class = NetworkOptValveFilter
    http_method_names = ["get"]

class NetworkOptValveGeoJsonViewSet(BaseGeoJsonViewSet):
    model = NetworkOptValve
    serializer_class = NetworkOptValveGeoJsonSerializer
    http_method_names = ["get"]
