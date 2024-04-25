from cwa_geod.assets.models.trunk_main import TrunkMain
from rest_framework import viewsets 
from ..serializers import TrunkMainSerializer

class TrunkMainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrunkMain.objects.all()
    serializer_class = TrunkMainSerializer
    lookup_field = 'gid'