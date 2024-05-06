from cwageodjango.assets.models import PressureControlValve
from config.viewsets import BaseModelViewSet, BaseGeoJsonViewSet
from config.filters import BaseFilter
from ..serializers import PressureControlValveSerializer, PressureControlValveGeoJsonSerializer


class PressureControlValveFilter(BaseFilter):

    class Meta:
        model = PressureControlValve
        fields = ["id", "gid"]


class PressureControlValveViewSet(BaseModelViewSet):
    queryset = PressureControlValve.objects.all()
    serializer_class = PressureControlValveSerializer
    filterset_class = PressureControlValveFilter
    http_method_names = ["get"]
    

class PressureControlValveGeoJsonViewSet(BaseGeoJsonViewSet):
    model = PressureControlValve
    serializer_class = PressureControlValveGeoJsonSerializer
    http_method_names = ["get"]
