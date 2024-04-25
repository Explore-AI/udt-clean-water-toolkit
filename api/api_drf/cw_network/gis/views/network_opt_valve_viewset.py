from cwa_geod.assets.models.network_opt_valve import NetworkOptValve
from ..serializers import NetworkOptValveSerializer
from rest_framework import viewsets


class NetworkOptValveViewSet(viewsets.ModelViewSet):
    queryset = NetworkOptValve.objects.all()
    serializer_class = NetworkOptValveSerializer
    lookup_field = 'gid'