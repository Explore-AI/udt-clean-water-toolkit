from rest_framework import viewsets
from cwa_geod.assets.models.chamber import Chamber
from ..serializers import ChamberSerializer

class ChamberViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Chamber.objects.all()
    serializer_class = ChamberSerializer
    lookup_field = 'gid'