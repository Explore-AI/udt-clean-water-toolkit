from cwageodjango.assets.models import PipeMain
from config.viewsets import BaseModelViewSet, BaseGeoJsonViewSet
from config.filters import BaseFilter
from ..serializers import PipeMainSerializer, PipeMainGeoJsonSerializer


class PipeMainFilter(BaseFilter):

    class Meta:
        model = PipeMain
        fields = ["id", "gid"]


class PipeMainViewSet(BaseModelViewSet):
    queryset = PipeMain.objects.all()
    serializer_class = PipeMainSerializer
    filterset_class = PipeMainFilter
    http_method_names = ["get"]


class PipeMainGeoJsonViewSet(BaseGeoJsonViewSet):
    model = PipeMain
    http_method_names = ["get"]
    serializer_class = PipeMainGeoJsonSerializer
