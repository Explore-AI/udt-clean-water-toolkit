from django.contrib.gis.db.models.functions import AsGeoJSON, Cast
from django.db.models.functions import JSONObject
from django.db.models import Value, JSONField
from cleanwater.serializers import GeoDjangoSerializer
from ..models import TrunkMain
from cwa_geod.config.settings import DEFAULT_SRID


class TrunkMainGeoJsonSerializer(GeoDjangoSerializer):
    """Convert trunk_mains data to geojson. See these refs
    for a guide on how the geojson is contructed.

    AsGeoJson query combined with json to build object

    https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/expressions/
    https://postgis.net/docs/ST_AsGeoJSON.html
    https://dakdeniz.medium.com/increase-django-geojson-serialization-performance-7cd8cb66e366
    """

    srid = DEFAULT_SRID
    items_limit = 100000  # set default in cofig
    default_properties = [
        "id",
        "gisid",
        "shape_length",
        "dma_id",
        "dma__code",
    ]  # should not include the geometry column as per convention

    def tw_trunk_mains_to_geojson(self, properties=None):
        """Serialization of db date to GeoJSON.

        Fast (maybe with bigger datasets) serialization into geoson.

        Args:
              properties: a list of model fields
        Returns:
              GeoJSON
        """

        properties = properties or self.default_properties
        properties = set(properties)
        json_properties = dict(zip(properties, properties))

        qs = (
            TrunkMain.objects.values(*properties)
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

        return self.queryset_to_geojson(qs)

    #
    def tw_trunk_mains_to_json2(self, properties=None):
        """Serialization of db date to GeoJSON. Alternate method
        Slighly faster serialization into geoson compared to 1) but
        employs iteration.

        Args:
              properties: a list of model fields
        Returns:
              GeoJSON
        """
        properties = properties or self.default_properties
        properties = set(properties)
        json_properties = dict(zip(properties, properties))

        qs = TrunkMain.objects.values(*properties).annotate(
            properties=JSONObject(**json_properties),
            geometry=AsGeoJSON("geometry", crs=True),
        )
        return self.queryset_to_geojson2(qs)

    # 1) slower serialization into geojson
    # start = datetime.datetime.now()
    # trunk_mains = TrunkMain.objects.all()
    # trunk_mains_data = serialize(
    #     "geojson", trunk_mains, geometry_field="geometry", srid=DEFAULT_SRID
    # )
    # finish = datetime.datetime.now()
    # print(finish - start)
    # trunk_mains_gdf = gpd.read_file(trunk_mains_data)
