from django.db.models.query import QuerySet
from . import GisToGraph
from cwa_geod.core.constants import DEFAULT_SRID
from ..models import TrunkMain, Hydrant, Logger, NetworkMeter


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

    def _set_pipe_connected_asset_relations(self) -> None:
        """Connect pipes with related pipe and point assets.
        Uses a map method to operate on the pipe and asset
        data.

        Params:
              None
        Returns:
              None
        """

        def _map_pipe_connected_asset_relations(pipe_data: dict, assets_data: list):
            import pdb

            pdb.set_trace()
            self.G.add_node(
                node_id,
                coords=pipe_data["geometry"].coords[0][0],
                **pipe_data,
            )

            self._set_connected_asset_relations(pipe_data, assets_data)

        list(
            map(
                _map_pipe_connected_asset_relations,
                self.all_pipe_data,
                self.all_asset_positions,
            )
        )

    def _create_neo4j_graph(self) -> None:
        self._set_pipe_connected_asset_relations()
