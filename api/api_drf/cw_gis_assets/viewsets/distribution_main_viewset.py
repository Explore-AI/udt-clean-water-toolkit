from cwageodjango.assets.models import DistributionMain
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from ..serializers import DistributionMainSerializer


class DistributionMainFilter(BaseFilter):

    class Meta:
        model = DistributionMain
        fields = ["id", "gid"]


class DistributionMainViewSet(BaseModelViewSet):
    queryset = DistributionMain.objects.all()
    serializer_class = DistributionMainSerializer
    filterset_class = DistributionMainFilter
    http_method_names = ["get"]
