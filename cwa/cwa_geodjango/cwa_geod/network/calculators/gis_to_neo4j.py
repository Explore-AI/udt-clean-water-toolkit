import json
from django.db.models.query import QuerySet
from neomodel.contrib.spatial_properties import NeomodelPoint
from cleanwater.exceptions import InvalidNodeException, InvalidPipeException
from . import GisToGraph
from cwa_geod.core.constants import (
    DEFAULT_SRID,
    TRUNK_MAIN__NAME,
    DISTRIBUTION_MAIN__NAME,
    PIPE_END__NAME,
    POINT_ASSET__NAME,
)
from ..models import PointAsset, PipeEnd


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
    def build_dma_data_as_json(dma_codes, dma_names):
        dma_data = [
            {"code": dma_code, "name": dma_name}
            for dma_code, dma_name in zip(dma_codes, dma_names)
        ]

        return json.dumps(dma_data)

    def check_node_exists(self, asset_name, gid):
        node_type: str = self._get_node_type(asset_name)

        if node_type == PIPE_END__NAME:
            node = PipeEnd.nodes.get_or_none(pipe_type=asset_name, gid=gid)
            return node, node_type, None
        elif node_type == POINT_ASSET__NAME:
            asset_model = PointAsset.asset_name_model_mapping(asset_name)

            node = asset_model.nodes.get_or_none(gid=gid)
            return node, node_type, asset_model
        else:
            InvalidNodeException(
                f"Invalid node detected: {node_type}. Valid nodes are {PIPE_END__NAME} or {POINT_ASSET__NAME}"
            )

    @staticmethod
    def _connect_nodes(start_node, end_node, pipe_name, relation_data):
        if pipe_name == TRUNK_MAIN__NAME:
            start_node.trunk_main.connect(end_node, relation_data)
        elif pipe_name == DISTRIBUTION_MAIN__NAME:
            start_node.distrbution_main.connect(end_node, relation_data)
        else:
            InvalidPipeException(f"Invalid pipe detected: {pipe_name}.")

    def _set_connected_asset_relations(
        self, pipe_data: dict, assets_data: list, pipe_end
    ) -> None:
        start_node = pipe_end

        for asset in assets_data:
            gid: int = asset["data"]["gid"]
            asset_name: str = asset["data"]["asset_name"]
            dma_data = self.build_dma_data_as_json(
                asset["data"]["dma_codes"], asset["data"]["dma_names"]
            )

            node, node_type, asset_model = self.check_node_exists(asset_name, gid)

            if not node and node_type == PIPE_END__NAME:
                new_pipe_end = PipeEnd.create(
                    {"gid": gid, "dmas": dma_data, "pipe_type": asset_name}
                )[0]
                self._connect_nodes(
                    start_node,
                    new_pipe_end,
                    pipe_data["asset_name"],
                    {"dmas": dma_data, "gid": gid, "weight": 1},
                )
            elif not node and node_type == POINT_ASSET__NAME:
                new_point_asset = asset_model.create({"gid": gid, "dmas": dma_data})[0]

                # edge_length: float = node_point_geometries[-1].distance(
                #     asset["intersection_point_geometry"]
                # )

                # TODO: add wieght to relation based on edge length
                self._connect_nodes(
                    start_node,
                    new_point_asset,
                    pipe_data["asset_name"],
                    {"dmas": dma_data, "gid": gid, "weight": 1},
                )

                start_node = new_point_asset

            elif node_type not in [PIPE_END__NAME, POINT_ASSET__NAME]:
                raise InvalidNodeException(
                    f"Invalid node detected: {node_type}. Valid nodes are 'pipe_end' or 'point_asset'"
                )

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
            pipe_type = pipe_data.get("asset_name")

            #
            pipe_end = PipeEnd.nodes.get_or_none(pipe_type=pipe_type, gid=pipe_gid)

            if not pipe_end:
                dma_data = self.build_dma_data_as_json(
                    pipe_data["dma_codes"], pipe_data["dma_names"]
                )
                coords = NeomodelPoint(pipe_data["geometry"].coords[0][0], crs="wgs-84")

                pipe_end = PipeEnd.create(
                    {"gid": pipe_gid, "dmas": dma_data, "pipe_type": pipe_type}
                )[0]

            self._set_connected_asset_relations(pipe_data, assets_data, pipe_end)

        list(
            map(
                _map_pipe_connected_asset_relations,
                self.all_pipe_data,
                self.all_asset_positions,
            )
        )

    def _create_neo4j_graph(self) -> None:
        self._set_pipe_connected_asset_relations()
