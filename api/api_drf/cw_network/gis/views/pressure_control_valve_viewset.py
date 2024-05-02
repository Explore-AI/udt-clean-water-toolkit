from cwageodjango.assets.models.pressure_control_valve import PressureControlValve
from ..serializers import PressureControlValveSerializer
from rest_framework import viewsets


class PressureControlValveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PressureControlValve.objects.all()
    serializer_class = PressureControlValveSerializer
    lookup_field = "gid"
