from django_filters import rest_framework as filters
from django.db.models import Q, JSONField
from cwageodjango.waterpipes.models import PipeFlow
from config.filters import BaseFilter
from config.viewsets import BaseModelViewSet
from cw_gis_assets.serializers import PipeFlowSerializer
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import serializers


class PipeFlowFilter(BaseFilter):
    tag = filters.CharFilter(field_name="pipe_main__tag", lookup_expr="icontains")
    ids = filters.BaseInFilter(field_name="pipe_main__id", lookup_expr="in")
    flow_data_timestamp = filters.CharFilter(method="filter_flow_data_timestamp")
    dmas = filters.CharFilter(
        field_name="pipe_main__dmas__code", lookup_expr="icontains"
    )

    class Meta:
        model = PipeFlow
        fields = ["pipe_main", "flow_data", "ids", "tag", "flow_data_timestamp", "dmas"]
        filter_overrides = {
            JSONField: {
                "filter_class": filters.CharFilter,
            },
        }

    def filter_flow_data_timestamp(self, queryset, name, value):
        filter_condition = Q()
        for obj in queryset:
            try:
                data = json.loads(obj.flow_data)
                if value in data:
                    filter_condition |= Q(pk=obj.pk)
            except json.JSONDecodeError:
                continue
        return queryset.filter(filter_condition)


class PipeFlowViewSet(BaseModelViewSet):
    queryset = PipeFlow.objects.all()
    serializer_class = PipeFlowSerializer
    filterset_class = PipeFlowFilter
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        ids = request.query_params.getlist("ids")
        timestamp = request.query_params.get("flow_data_timestamp")
        queryset = self.filter_queryset(self.get_queryset())

        if timestamp:
            filtered_results = []
            for obj in queryset:
                try:
                    data = json.loads(obj.flow_data)
                    value = data.get(timestamp)
                    if value is not None:
                        filtered_results.append({obj.pipe_main.id: value})
                except json.JSONDecodeError:
                    continue

            if filtered_results:
                return Response(filtered_results, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "Timestamp not found for the given IDs."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
