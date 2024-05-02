from cwageodjango.assets.models.hydrant import Hydrant
from ..serializers import HydrantSerializer
from rest_framework import viewsets


class HydrantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hydrant.objects.all()
    serializer_class = HydrantSerializer
    lookup_field = "gid"
