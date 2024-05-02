from cwageodjango.assets.models import NetworkMeter
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from ..serializers import NetworkMeterSerializer


class NetworkMeterFilter(BaseFilter):

    class Meta:
        model = NetworkMeter
        fields = ["id", "gid"]


class NetworkMeterViewSet(BaseModelViewSet):
    queryset = NetworkMeter.objects.all()
    serializer_class = NetworkMeterSerializer
    filterset_class = NetworkMeterFilter
    http_method_names = ["get"]
