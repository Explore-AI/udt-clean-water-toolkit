from cwageodjango.assets.models import TrunkMain
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from ..serializers import TrunkMainSerializer


class TrunkMainFilter(BaseFilter):

    class Meta:
        model = TrunkMain
        fields = ["id", "gid"]


class TrunkMainViewSet(BaseModelViewSet):
    queryset = TrunkMain.objects.all()
    serializer_class = TrunkMainSerializer
    filterset_class = TrunkMainFilter
    http_method_names = ["get"]
