from cwageodjango.assets.models import TrunkMain
from config.viewsets import BaseModelViewSet, BaseGeoJsonViewSet
from config.filters import BaseFilter
from ..serializers import TrunkMainSerializer, TrunkMainGeoJsonSerializer


class TrunkMainFilter(BaseFilter):

    class Meta:
        model = TrunkMain
        fields = ["id", "gid"]


class TrunkMainViewSet(BaseModelViewSet):
    queryset = TrunkMain.objects.all()
    serializer_class = TrunkMainSerializer
    filterset_class = TrunkMainFilter
    http_method_names = ["get"]


class TrunkMainGeoJsonViewSet(BaseGeoJsonViewSet):
    http_method_names = ["get"]
    serializer_class = TrunkMainGeoJsonSerializer
    model = TrunkMain
