from cwa_geod.assets.models.operational_site import OperationalSite
from ..serializers import OperationalSiteSerializer
from rest_framework import viewsets


class OperationalSiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OperationalSite.objects.all()
    serializer_class = OperationalSiteSerializer
    lookup_field = 'gid'