from cwageodjango.assets.models import TrunkMain
from config.viewsets import BaseModelViewSet
from config.filters import BaseFilter
from django.db.models.functions import JSONObject
from django.db.models import JSONField
from django.db.models.expressions import Value
from django.contrib.gis.db.models.functions import AsGeoJSON, Cast
from ..serializers import TrunkMainSerializer, TrunkMainGeoJsonSerializer
from rest_framework.response import Response
import json


class TrunkMainFilter(BaseFilter):

    class Meta:
        model = TrunkMain
        fields = ["id", "gid"]


class TrunkMainViewSet(BaseModelViewSet):
    queryset = TrunkMain.objects.all()
    serializer_class = TrunkMainSerializer
    filterset_class = TrunkMainFilter
    http_method_names = ["get"]

class TrunkMainGeoJsonViewSet(BaseModelViewSet):
    http_method_names = ["get"]
    
    def get_queryset(self):
        """ Define our custom queryset, that returns a GeoJSON and not our model object """
        properties = {"id", "gid"}
        json_properties = dict(zip(properties, properties))
        qs = (
            TrunkMain.objects.values(*properties)
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
    
        
    def list(self, request, *args, **kwargs):
        """ Custom Response for list API calls """
        query_set = self.get_queryset()
        features = [json.dumps(feature) for feature in query_set]
        feature_collection = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": f"EPSG:{27700}"}},
            "features": features,
        }
        return Response(feature_collection, content_type="application/geo+json")
    
        
        
    
