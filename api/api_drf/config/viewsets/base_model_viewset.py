from rest_framework import viewsets
from django_filters import rest_framework as filters
from config.filters.base_filter import BaseFilter
from django.contrib.gis.db import models
from django.db.models.functions import JSONObject
from django.db.models import JSONField
from django.db.models.expressions import Value
from django.contrib.gis.db.models.functions import AsGeoJSON, Cast
from rest_framework import renderers


class BaseModelViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BaseFilter
    renderer_classes = [renderers.JSONRenderer]
    handler500 = "rest_framework.exceptions.server_error"


class BaseGeoJsonViewSet(BaseModelViewSet):
    model: models.Model = None
    serializer_class = None
    http_method_names = ["get"]
    properties = {"id", "gid"}

    def get_queryset(self):
        if self.model is None:
            raise NotImplementedError("A model must be specified for the ViewSet")
        json_properties = dict(zip(self.properties, self.properties))
        qs = (
            self.model.objects.values(*self.properties)
            .annotate(
                geojson=JSONObject(
                    properties=JSONObject(**json_properties),
                    type=Value("Feature"),
                    geometry=Cast(AsGeoJSON("geometry", crs=True), JSONField()),
                ),
            )
            .values_list("geojson", flat=True)
        )
        return qs
