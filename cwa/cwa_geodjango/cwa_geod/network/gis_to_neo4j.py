from django.db.models.query import QuerySet
from . import GisToGraph
from cwa_geod.core.constants import DEFAULT_SRID


class GisToNeo4J(GisToGraph):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, srid: int):
        self.srid: int = srid or DEFAULT_SRID
        super().__init__(self.srid)

    def create_network(self):
        trunk_mains_qs: QuerySet = self.get_trunk_mains_data()
        distribution_mains_qs: QuerySet = self.get_distribution_mains_data()

        pipes_qs: QuerySet = trunk_mains_qs.union(distribution_mains_qs, all=True)

        self.calc_pipe_point_relative_positions(pipes_qs)

        self._create_neo4j_graph()

    def _create_neo4j_graph(self) -> None:
        self._set_pipe_connected_asset_relations()
        import pdb

        pdb.set_trace()
