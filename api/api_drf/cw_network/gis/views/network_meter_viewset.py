from cwa_geod.assets.models.network_meter import NetworkMeter
from ..serializers import NetworkMeterSerializer
from rest_framework import viewsets


class NetworkMeterViewSet(viewsets.ModelViewSet):
    queryset = NetworkMeter.objects.all()
    serializer_class = NetworkMeterSerializer
    lookup_field = 'gid'
