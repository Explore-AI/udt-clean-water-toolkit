import json
from django.db.models.query import QuerySet
from neomodel.contrib.spatial_properties import NeomodelPoint
from . import GisToGraph
from cwa_geod.core.constants import DEFAULT_SRID
from ..models import *
from ..models.point_node import PointNode

PIPE_MODELS = [
    TrunkMain,
    DistributionMain,
]

ASSET_MODELS = [
    Logger,
    Hydrant,
    PressureFitting,
    PressureControlValve,
    OperationalSite,
    Chamber,
    NetworkMeter,
    NetworkOptValve,
]


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

    @staticmethod
    def pipe_name_model_mapping(asset_name):
        for model in PIPE_MODELS:
            if model.AssetMeta.asset_name == asset_name:
                return model

        return None

    @staticmethod
    def asset_name_model_mapping(asset_name):
        for model in ASSET_MODELS:
            if model.AssetMeta.asset_name == asset_name:
                return model

        return None

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
            pipe_gid = pipe_data.get("gid")
            pipe_end_gid = PointNode.nodes.filter(gid=pipe_gid).all(lazy=True)

            if not pipe_end_gid:
                dma_data = [
                    {"code": dma_code, "name": dma_name}
                    for dma_code, dma_name in zip(
                        pipe_data["dma_codes"], pipe_data["dma_names"]
                    )
                ]

                dma_json = json.dumps(dma_data)
                coords = NeomodelPoint(pipe_data["geometry"].coords[0][0], crs="wgs-84")
                import pdb

                pdb.set_trace()
                PipeEnd.create({"gid": pipe_gid, "dmas": dma_json, "coords": coords})
                import pdb

                pdb.set_trace()

            # self.G.add_node(
            #     node_id,
            #     coords=pipe_data["geometry"].coords[0][0],
            #     **pipe_data,
            # )

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
