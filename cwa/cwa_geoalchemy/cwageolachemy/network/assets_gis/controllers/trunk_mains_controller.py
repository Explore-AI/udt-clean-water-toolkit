from .mains_controller import MainsController
from ..models import TrunkMain, DistributionMain, trunkmain_dmas, distributionmain_dmas
from sqlalchemy.dialects.postgresql import array as ARRAY
from sqlalchemy import func


class TrunkMainsController(MainsController):
    model = TrunkMain

    def _generate_mains_subqueries(self):
        subquery_tm_junctions = self.generate_touches_subquery(
            TrunkMain, trunkmain_dmas
        )
        subquery_dm_junctions = self.generate_touches_subquery(
            DistributionMain, distributionmain_dmas
        )
        
        return {
            "trunkmain_junctions": ARRAY(subquery_tm_junctions).label("trunkmain_junctions"), 
            "distmain_junctions": ARRAY(subquery_dm_junctions).label("distmain_junctions"),
        }
        

    def trunk_mains_to_geojson(self, properties=None):
        pass

    def trunk_mains_to_geojson2(self, properties=None):
        pass

    def trunk_mains_to_geodataframe(self, properties=None):
        pass
