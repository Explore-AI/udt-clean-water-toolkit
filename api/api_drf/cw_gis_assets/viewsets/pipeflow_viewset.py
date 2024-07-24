from django_filters import rest_framework as filters
from django.db.models import JSONField
from cwageodjango.waterpipes.models import PipeFlow
from config.filters import BaseFilter
from config.viewsets import BaseModelViewSet
from cwageodjango.waterpipes.models import PipeFlow
from cw_gis_assets.serializers import PipeFlowSerializer


class PipeFlowFilter(BaseFilter):
    tag = filters.CharFilter(field_name="pipe_main__tag", lookup_expr="icontains")
    ids = filters.BaseInFilter(field_name="pipe_main__id", lookup_expr="in")
    flow_data_timestamp = filters.CharFilter(method="filter_flow_data_timestamp")

    class Meta:
        model = PipeFlow
        fields = ["pipe_main", "flow_data", "ids", "tag", "flow_data_timestamp"]
        filter_overrides = {
            JSONField: {
                "filter_class": filters.CharFilter,
            },
        }

    def filter_flow_data_timestamp(self, queryset, name, value):
        lookup_value = value
        return queryset.filter(flow_data__contains=lookup_value)


class PipeFlowViewSet(BaseModelViewSet):
    queryset = PipeFlow.objects.all()
    serializer_class = PipeFlowSerializer
    filterset_class = PipeFlowFilter
    http_method_names = ["get"]
