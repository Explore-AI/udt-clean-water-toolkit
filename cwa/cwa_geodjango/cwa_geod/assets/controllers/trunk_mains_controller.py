from django.contrib.postgres.expressions import ArraySubquery
from cwa_geod.assets.models import TrunkMain, DistributionMain
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
    # items_limit = 100000  # TODO: set default in config
    default_properties = [
        "id",
        "gid",
    ]  # should not include the geometry column as per convention

    def _generate_mains_subqueries(self):
        json_fields = self.get_pipe_json_fields()

        subquery1 = self._generate_touches_subquery(
            self.model.objects.all(), json_fields
        )
        subquery2 = self._generate_touches_subquery(
            DistributionMain.objects.all(), json_fields
        )

        subqueries = {
            "trunk_mains_data": ArraySubquery(subquery1),
            "distribution_mains_data": ArraySubquery(subquery2),
        }

        return subqueries

    def trunk_mains_to_geojson(self, properties=None):
        return self.mains_to_geojson(properties)

    def trunk_mains_to_geojson2(self, properties=None):
        return self.mains_to_geojson2(properties)

    def trunk_mains_to_geodataframe(self, properties=None):
        return self.mains_to_geodataframe(properties)
