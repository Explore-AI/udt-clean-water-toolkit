from config.viewsets import BaseModelViewSet
from cwageodjango.waterpipes.models import PipeFlow
from cw_gis_assets.serializers import PipeFlowSerializer


class PipeFlowViewSet(BaseModelViewSet):
    serializer_class = PipeFlowSerializer
    queryset = PipeFlow.objects.all()
    http_method_names = ["get"]

    # pipe_main_id = self.request.query_params.get("pipe_main_id", None)

    # if pipe_main_id is not None:
    #     try:
    #         # Filter by pipe_main_id
    #         queryset = queryset.filter(pipe_main=pipe_main_id)
    #     except ValueError:
    #         # Handle the case where pipe_main_id is not valid
    #         queryset = PipeFlow.objects.none()

    # return queryset
