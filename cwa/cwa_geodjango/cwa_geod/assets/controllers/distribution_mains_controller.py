from django.contrib.gis.db.models.functions import AsGeoJSON, Cast
from django.db.models.functions import JSONObject
from django.db.models import Value, JSONField
from cleanwater.controllers import GeoDjangoController
from ..models import DistributionMain
from cwa_geod.config.settings import DEFAULT_SRID


class DistributionMainsController(GeoDjangoController):
    """Convert distribution_mains data to GeoJson. Please look into
    structore of GeoJson object. Also, see these refs
    for a guide on how the GeoJson is contructed.

    AsGeoJson query combined with json to build object

    https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/expressions/
    https://postgis.net/docs/ST_AsGeoJSON.html
    https://dakdeniz.medium.com/increase-django-geojson-serialization-performance-7cd8cb66e366
    """

    model = DistributionMain
    srid = DEFAULT_SRID
    items_limit = 2000000  # set default in cofig
    default_properties = [
        "id",
        "gisid",
        "shape_length",
        "dma_id",
        "dma__code",
    ]  # should not include the geometry column as per convention

    def get_geometry_queryset(self, properties=None):
        properties = properties or self.default_properties
        properties = set(properties)
        json_properties = dict(zip(properties, properties))

        qs = (
            self.model.objects.values(*properties)
            .annotate(
                geojson=JSONObject(
                    properties=JSONObject(**json_properties),
                    type=Value("Feature"),
                    geometry=Cast(
                        AsGeoJSON("geometry", crs=True),
                        output_field=JSONField(),
                    ),
                ),
            )
            .values_list("geojson", flat=True)
        )
        return qs

    def distribution_mains_to_geojson(self, properties=None):
        """Serialization of db data to GeoJSON.

        Fast (maybe with bigger datasets) serialization into geoson.

        Params:
              properties: list (optional). A list of model fields
        Returns:
              geoJSON: geoJSON object
        """

        qs = self.get_geometry_queryset(properties)
        return self.queryset_to_geojson(qs)
