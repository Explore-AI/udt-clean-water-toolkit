from django.contrib.postgres.expressions import ArraySubquery
from cwageodjango.assets.models import TrunkMain, DistributionMain, ConnectionMain
from .mains_controller import MainsController


class TrunkMainsController(MainsController):
    """Convert trunk_mains data to Queryset or GeoJSON."""

    model = TrunkMain

    def __init__(self):
        super().__init__(self.model)

    def _generate_mains_subqueries(self):
        cm_qs = ConnectionMain.objects.all().order_by("pk")
        tm_qs = self.model.objects.all().order_by("pk")
        dm_qs = DistributionMain.objects.all().order_by("pk")
        json_fields = self.get_pipe_json_fields()

        subquery_cm_junctions = self.generate_touches_subquery(cm_qs, json_fields)

        subquery_tm_junctions = self.generate_touches_subquery(tm_qs, json_fields)

        subquery_dm_junctions = self.generate_touches_subquery(dm_qs, json_fields)

        termini_subqueries = self.generate_termini_subqueries([tm_qs, dm_qs])

        subqueries = {
            "connmain_junctions": ArraySubquery(subquery_cm_junctions),
            "trunkmain_junctions": ArraySubquery(subquery_tm_junctions),
            "distmain_junctions": ArraySubquery(subquery_dm_junctions),
            "line_start_intersections": ArraySubquery(termini_subqueries[0]),
            "line_end_intersections": ArraySubquery(termini_subqueries[1]),
        }

        return subqueries

    def generate_dwithin_subquery(
        self,
        qs,
        json_fields,
        geometry_field="geometry",
        inner_subqueries={},
        extra_json_fields={},
    ):

        cm_qs = ConnectionMain.objects.all()
        tm_qs = self.model.objects.all()
        dm_qs = DistributionMain.objects.all()

        tm_inner_subquery = self._generate_dwithin_inner_subquery(
            tm_qs, "gid", geometry_field=geometry_field
        )
        dm_inner_subquery = self._generate_dwithin_inner_subquery(
            dm_qs, "gid", geometry_field=geometry_field
        )
        cm_inner_subquery = self._generate_dwithin_inner_subquery(
            cm_qs, "gid", geometry_field=geometry_field
        )

        inner_subqueries = {
            "tm_touches_ids": tm_inner_subquery,
            "dm_touches_ids": dm_inner_subquery,
            "cm_touches_ids": cm_inner_subquery
        }

        subquery = super().generate_dwithin_subquery(
            qs,
            json_fields,
            geometry_field="geometry",
            inner_subqueries=inner_subqueries,
            extra_json_fields=extra_json_fields,
        )

        return subquery

    def trunk_mains_to_geojson(self, properties=None):
        return self.mains_to_geojson(properties)

    def trunk_mains_to_geojson2(self, properties=None):
        return self.mains_to_geojson2(properties)

    def trunk_mains_to_geodataframe(self, properties=None):
        return self.mains_to_geodataframe(properties)
