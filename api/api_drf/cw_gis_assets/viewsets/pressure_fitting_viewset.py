from cwageodjango.assets.models import PressureFitting
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from ..serializers import PressureFittingSerializer


class PressureFittingFilter(BaseFilter):

    class Meta:
        model = PressureFitting
        fields = ["id", "gid"]


class PressureFittingViewSet(BaseModelViewSet):
    queryset = PressureFitting.objects.all()
    serializer_class = PressureFittingSerializer
    filterset_class = PressureFittingFilter
    http_method_names = ["get"]
