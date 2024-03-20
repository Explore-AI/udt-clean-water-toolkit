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
        json_fields = self.get_json_fields()

        subquery1 = self._generate_touches_subquery(
            self.model.objects.all(), json_fields
        )

        subquery2 = self._generate_touches_subquery(
            TrunkMain.objects.all(), json_fields
        )

        subqueries = {
            "trunk_mains_data": ArraySubquery(subquery1),
            "distribution_mains_data": ArraySubquery(subquery2),
        }

        return subqueries

    def distribution_mains_to_geojson(self, properties=None):
        return self.mains_to_geojson(properties)

    def distribution_mains_to_geojson2(self, properties=None):
        return self.mains_to_geojson2(properties)

    def distribution_mains_to_geodataframe(self, properties=None):
        return self.mains_to_geodataframe(properties)
