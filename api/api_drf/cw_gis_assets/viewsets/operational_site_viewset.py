from cwageodjango.assets.models import OperationalSite
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from ..serializers import OperationalSiteSerializer


class OperationalSiteFilter(BaseFilter):

    class Meta:
        model = OperationalSite
        fields = ["id", "gid"]


class OperationalSiteViewSet(BaseModelViewSet):
    queryset = OperationalSite.objects.all()
    serializer_class = OperationalSiteSerializer
    filterset_class = OperationalSiteFilter
    http_method_names = ["get"]
