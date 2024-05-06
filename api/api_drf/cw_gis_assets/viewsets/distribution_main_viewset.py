from cwageodjango.assets.models import DistributionMain
from config.viewsets import BaseModelViewSet, BaseGeoJsonViewSet
from config.filters import BaseFilter
from ..serializers import DistributionMainSerializer, DistributionMainGeoJsonSerializer


class DistributionMainFilter(BaseFilter):

    class Meta:
        model = DistributionMain
        fields = ["id", "gid"]


class DistributionMainViewSet(BaseModelViewSet):
    queryset = DistributionMain.objects.all()
    serializer_class = DistributionMainSerializer
    filterset_class = DistributionMainFilter
    http_method_names = ["get"]

class DistributionMainGeoJsonViewSet(BaseGeoJsonViewSet):
    http_method_names = ["get"]
    serializer_class = DistributionMainGeoJsonSerializer
    model = DistributionMain
    