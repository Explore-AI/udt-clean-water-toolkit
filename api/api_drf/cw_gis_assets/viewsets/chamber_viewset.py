from cwageodjango.assets.models import Chamber
from config.viewsets import BaseModelViewSet, BaseGeoJsonViewSet
from config.filters import BaseFilter
from ..serializers import ChamberSerializer, ChamberGeoJsonSerializer


class ChamberFilter(BaseFilter):

    class Meta:
        model = Chamber
        fields = ["id", "gid"]


class ChamberViewSet(BaseModelViewSet):
    queryset = Chamber.objects.all()
    serializer_class = ChamberSerializer
    filterset_class = ChamberFilter
    http_method_names = ["get"]
    

class ChamberGeoJsonViewSet(BaseGeoJsonViewSet):
    model = Chamber
    serializer_class = ChamberGeoJsonSerializer
    http_method_names = ["get"]
    
