from django_filters import rest_framework as filters
from django.db.models import Q
from cwageodjango.utilities.models import DMA
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from cw_utilities.serializers import DmaSerializer


class DmaFilter(BaseFilter):

    search = filters.CharFilter(method="filter_search")

    def filter_search(self, qs, name, value):
        return qs.filter(Q(code__icontains=value) | Q(name__icontains=value))

    class Meta:
        model = DMA
        fields = ["id", "search"]


class DmaViewSet(BaseModelViewSet):
    queryset = DMA.objects.all()
    serializer_class = DmaSerializer
    filterset_class = DmaFilter
    http_method_names = ["get"]

    # def list(self, request):
    #     import pdb

    #     pdb.set_trace()
