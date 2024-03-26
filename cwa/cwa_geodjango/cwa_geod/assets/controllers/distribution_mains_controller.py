from django.contrib.postgres.expressions import ArraySubquery
from cwa_geod.assets.models import TrunkMain, DistributionMain
from .mains_controller import MainsController


class DistributionMainsController(MainsController):
    """Convert distribution mains data to a Queryset or GeoJSON."""

    model = DistributionMain
    default_properties = [
        "id",
        "gid",
    ]  # should not include the geometry column as per convention

    def _generate_mains_subqueries(self):
        json_fields = self.get_pipe_json_fields()

        dist_main_intersection_subquery = self._generate_touches_subquery(
            self.model.objects.all(), json_fields
        )

        trunk_main_intersection_subquery = self._generate_touches_subquery(
            TrunkMain.objects.all(), json_fields
        )

        subqueries = {
            "trunk_mains_data": ArraySubquery(dist_main_intersection_subquery),
            "distribution_mains_data": ArraySubquery(trunk_main_intersection_subquery),
        }

        return subqueries

    def distribution_mains_to_geojson(self, properties=None):
        return self.mains_to_geojson(properties)

    def distribution_mains_to_geojson2(self, properties=None):
        return self.mains_to_geojson2(properties)

    def distribution_mains_to_geodataframe(self, properties=None):
        return self.mains_to_geodataframe(properties)
