from django_filters import rest_framework as filters
from django.db.models import Q, F, JSONField
from cwageodjango.waterpipes.models import PipeFlow
from config.filters import BaseFilter
from config.viewsets import BaseModelViewSet
from cw_gis_assets.serializers import PipeFlowSerializer
import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import serializers


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
        filter_condition = Q()
        for obj in queryset:
            try:
                # Parse the JSON string into a Python dictionary
                data = json.loads(obj.flow_data)
                # Check if the specific timestamp key exists in the dictionary
                if value in data:
                    filter_condition |= Q(pk=obj.pk)
            except json.JSONDecodeError:
                continue

        # Apply the filter condition to the queryset
        return queryset.filter(filter_condition)


class PipeFlowViewSet(BaseModelViewSet):
    queryset = PipeFlow.objects.all()
    # for obj in PipeFlow.objects.all()[:2]:
    #     data = json.loads(obj.flow_data)
    #     print(f"JSON Loaded: {data.get('2024-07-17T23:15:00')}")
    serializer_class = PipeFlowSerializer
    filterset_class = PipeFlowFilter
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        # Get the filter parameters
        ids = request.query_params.getlist("ids")
        timestamp = request.query_params.get("flow_data_timestamp")

        # Apply filters based on `ids` and `flow_data_timestamp`
        queryset = self.filter_queryset(self.get_queryset())

        if timestamp:
            filtered_results = []
            for obj in queryset:
                try:
                    data = json.loads(obj.flow_data)
                    value = data.get(timestamp)
                    if value is not None:
                        # Collect results with specific timestamp values
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

        # If no timestamp is provided, return the filtered queryset as usual
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
