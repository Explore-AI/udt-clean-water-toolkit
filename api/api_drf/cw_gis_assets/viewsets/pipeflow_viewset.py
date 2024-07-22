from django.shortcuts import get_object_or_404
from config.viewsets import BaseModelViewSet
from cwageodjango.waterpipes.models import PipeFlow
from cw_gis_assets.serializers import PipeFlowSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class PipeFlowViewSet(BaseModelViewSet):
    serializer_class = PipeFlowSerializer
    queryset = PipeFlow.objects.all()
    http_method_names = ["get"]

    class Meta:
        model = PipeFlow
        fields = ["pipe_main", "flow_data"]

    def list(self, request, *args, **kwargs):
        sample_size = 10  # Define the number of samples you want to return
        queryset = self.get_queryset()[
            :sample_size
        ]  # Get only the first `sample_size` results
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="flow-data", url_name="flow_data")
    def get_flow_data(self, request, pk=None):
        pipe_flow = get_object_or_404(PipeFlow, pk=pk)
        return Response(pipe_flow.flow_data, status=status.HTTP_200_OK)
