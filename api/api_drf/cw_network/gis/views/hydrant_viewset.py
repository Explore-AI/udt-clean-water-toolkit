from cwa_geod.assets.models.hydrant import Hydrant
from ..serializers import HydrantSerializer
from rest_framework import viewsets


class HydrantViewSet(viewsets.ModelViewSet):
    queryset = Hydrant.objects.all()
    serializer_class = HydrantSerializer
    lookup_field = 'gid'