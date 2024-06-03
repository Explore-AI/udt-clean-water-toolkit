from cwageodjango.utilities.models import DMA
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from cw_utilities.serializers import DmaSerializer


# class TrunkMainFilter(BaseFilter):

#     class Meta:
#         model = TrunkMain
#         fields = ["id", "gid"]


class DmaViewSet(BaseModelViewSet):
    queryset = DMA.objects.all()
    serializer_class = DmaSerializer
    # filterset_class = TrunkMainFilter
    http_method_names = ["get"]
