from cwageodjango.assets.models import OperationalSite
from config.viewsets import BaseModelViewSet, BaseGeoJsonViewSet
from config.filters import BaseFilter
from ..serializers import OperationalSiteSerializer, OperationalSiteGeoJsonSerializer


class OperationalSiteFilter(BaseFilter):

    class Meta:
        model = OperationalSite
        fields = ["id", "gid"]


class OperationalSiteViewSet(BaseModelViewSet):
    queryset = OperationalSite.objects.all()
    serializer_class = OperationalSiteSerializer
    filterset_class = OperationalSiteFilter
    http_method_names = ["get"]
    

class OperationalSiteGeoJsonViewSet(BaseGeoJsonViewSet):
    model = OperationalSite
    serializer_class = OperationalSiteGeoJsonSerializer
    http_method_names = ["get"]
