from django.contrib.postgres.expressions import ArraySubquery
from cwa_geod.assets.models import TrunkMain, DistributionMain
from .mains_controller import MainsController


class DistributionMainsController(MainsController):
    """Convert distribution mains data to a Queryset or GeoJSON."""

    model = DistributionMain

    def __init__(self):
        super().__init__(self.model)


    def _generate_mains_subqueries(self):
        tm_qs = TrunkMain.objects.all()
        dm_qs = self.model.objects.all()
        json_fields = self.get_pipe_json_fields()

        subquery_tm_intersections = self.generate_touches_line_subquery(
            tm_qs, json_fields
        )

        subquery_dm_intersections = self.generate_touches_line_subquery(
            dm_qs, json_fields
        )

        termini_subqueries = self.generate_termini_subqueries([tm_qs, dm_qs])

        subqueries = {
            "tm_intersections": ArraySubquery(subquery_tm_intersections),
            "dm_intersections": ArraySubquery(subquery_dm_intersections),
            "line_start_intersections": ArraySubquery(termini_subqueries[0]),
            "line_end_intersections": ArraySubquery(termini_subqueries[1]),
        }

        return subqueries

    def distribution_mains_to_geojson(self, properties=None):
        return self.mains_to_geojson(properties)

    def distribution_mains_to_geojson2(self, properties=None):
        return self.mains_to_geojson2(properties)

    def distribution_mains_to_geodataframe(self, properties=None):
        return self.mains_to_geodataframe(properties)
