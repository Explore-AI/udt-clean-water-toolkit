from cwa_geod.assets.models.distribution_main import DistributionMain
from ..serializers import DistributionMainSerializer
from rest_framework import viewsets


class DistributionMainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DistributionMain.objects.all()
    serializer_class = DistributionMainSerializer
    lookup_field = 'gid'
