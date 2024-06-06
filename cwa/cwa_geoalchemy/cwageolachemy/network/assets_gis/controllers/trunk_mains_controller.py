from . import MainsController
from ..models import TrunkMain, DistributionMain, ConnectionMain, trunkmain_dmas, distributionmain_dmas, connection_main_dmas


class TrunkMainsController(MainsController):
    model = TrunkMain

    def _generate_mains_subqueries(self):
        subquery_tm_junctions = self.generate_touches_subquery(
            TrunkMain, trunkmain_dmas
        )
        subquery_dm_junctions = self.generate_touches_subquery(
            DistributionMain, distributionmain_dmas
        )
        subquery_cm_junctions = self.generate_touches_subquery(
            ConnectionMain, connection_main_dmas
        )

        termini_subqueries = self.generate_termini_subqueries(
            {"distribution_main": distributionmain_dmas, "trunk_main": trunkmain_dmas, "connection_main": connection_main_dmas}
        )
        return {
            "trunkmain_junctions": subquery_tm_junctions.label("trunkmain_junctions"),
            "distmain_junctions": subquery_dm_junctions.label("distmain_junctions"),
            "connmain_junctions": subquery_cm_junctions.label("connmain_junctions"),
            "line_start_intersection_gids": termini_subqueries[0],
            "line_end_intersection_gids": termini_subqueries[1],
        }

    def trunk_mains_to_geojson(self, properties=None):
        pass

    def trunk_mains_to_geojson2(self, properties=None):
        pass

    def trunk_mains_to_geodataframe(self, properties=None):
        pass
