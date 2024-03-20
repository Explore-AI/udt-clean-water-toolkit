from cwa_geod.assets.models import *
from cwa_geod.core.constants import DEFAULT_SRID
from .mains_controller import MainsController


class TrunkMainsController(MainsController):
    """Convert trunk_mains data to Queryset or GeoJSON.

    Refs on how the GeoJSON is constructed.
    AsGeoJson query combined with json to build object
    https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/expressions/
    https://postgis.net/docs/ST_AsGeoJSON.html
    https://dakdeniz.medium.com/increase-django-geojson-serialization-performance-7cd8cb66e366
    """

    model = TrunkMain
    srid = DEFAULT_SRID
    # items_limit = 100000  # TODO: set default in config
    WITHIN_DISTANCE = 0.5
    default_properties = [
        "id",
        "gid",
    ]  # should not include the geometry column as per convention

    def trunk_mains_to_geojson(self, properties=None):
        return self.mains_to_geojson(properties)

    def trunk_mains_to_geojson2(self, properties=None):
        return self.mains_to_geojson2(properties)

    def trunk_mains_to_geodataframe(self, properties=None):
        return self.mains_to_geodataframe(properties)

    # 1) slower serialization into geojson
    # start = datetime.datetime.now()
    # trunk_mains = TrunkMain.objects.all()
    # trunk_mains_data = serialize(
    #     "geojson", trunk_mains, geometry_field="geometry", srid=DEFAULT_SRID
    # )
    # finish = datetime.datetime.now()
    # print(finish - start)
    # trunk_mains_gdf = gpd.read_file(trunk_mains_data)
