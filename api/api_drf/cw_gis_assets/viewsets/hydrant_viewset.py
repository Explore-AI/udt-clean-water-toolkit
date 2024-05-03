from cwageodjango.assets.models import Hydrant
from config.viewsets import BaseModelViewSet, BaseGeoJsonViewSet
from config.filters import BaseFilter
from ..serializers import HydrantSerializer, HydrantGeoJsonSerializer


class HydrantFilter(BaseFilter):

    class Meta:
        model = Hydrant
        fields = ["id", "gid"]


class HydrantViewSet(BaseModelViewSet):
    queryset = Hydrant.objects.all()
    serializer_class = HydrantSerializer
    filterset_class = HydrantFilter
    http_method_names = ["get"]

class HydrantGeoJsonViewSet(BaseGeoJsonViewSet): 
    model = Hydrant
    serializer_class = HydrantGeoJsonSerializer
    http_method_names = ["get"]