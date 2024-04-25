from cwa_geod.assets.models.pressure_fitting import PressureFitting
from ..serializers import PressureFittingSerializer
from rest_framework import viewsets


class PressureFittingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PressureFitting.objects.all()
    serializer_class = PressureFittingSerializer
    lookup_field = 'gid'