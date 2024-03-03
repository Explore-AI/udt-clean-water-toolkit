import json
from django.db.models.query import QuerySet
from neomodel.contrib.spatial_properties import NeomodelPoint
from . import GisToGraph
from cwa_geod.core.constants import DEFAULT_SRID
from ..models import *
from ..models.point_node import PointNode

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
    def asset_name_model_mapping(asset_name):
        for model in ASSET_MODELS:
            if model.AssetMeta.asset_name == asset_name:
                return model

        return None

    @staticmethod
    def build_dma_data_as_json(dma_codes, dma_names):
        dma_data = [
            {"code": dma_code, "name": dma_name}
            for dma_code, dma_name in zip(dma_codes, dma_names)
        ]

        return json.dumps(dma_data)

    def check_node_exists(self, asset_name, gid):
        node_type: str = self._get_node_type(asset_name)

        if node_type == "pipe_end":
            node = PipeEnd.nodes.get_or_none(pipe_type=asset_name, gid=gid)
            return node
        elif node_type == "point_asset":
            asset_model = self.asset_name_model_mapping(asset_name)
            import pdb

            pdb.set_trace()

            node = asset_model.nodes.get_or_none(gid=gid).all(lazy=True)
            return node

    def _set_connected_asset_relations(
        self, pipe_data: dict, assets_data: list
    ) -> None:
        for asset in assets_data:
            asset_name: str = asset["data"]["asset_name"]

            gid: int = asset["data"]["gid"]

            node = self.check_node_exists(asset_name, gid)
            import pdb

            pdb.set_trace()
            if not node:
                dma_data = self.build_dma_data_as_json(
                    asset["dma_codes"], asset["dma_names"]
                )
                PipeEnd.create({"gid": gid, "dmas": dma_data, "pipe_type": pipe_type})

                # self.G.add_node(
                #     new_node_id,
                #     position=asset["position"],
                #     node_type=node_type,
                #     coords=asset["intersection_point_geometry"].coords,
                #     **asset["data"],
                # )

            edge_length: float = node_point_geometries[-1].distance(
                asset["intersection_point_geometry"]
            )

            self.G.add_edge(
                new_node_ids[-1],
                new_node_id,
                weight=edge_length,
                id=pipe_data["id"],
                gid=pipe_data["gid"],
                normalised_position_on_pipe=asset["position"],
            )
            node_point_geometries.append(asset["intersection_point_geometry"])
            new_node_ids.append(new_node_id)

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
            pipe_end_ids = PipeEnd.nodes.filter(pipe_type=pipe_type, gid=pipe_gid).all(
                lazy=True
            )

            if not pipe_end_ids:
                dma_data = self.build_dma_data_as_json(
                    pipe_data["dma_codes"], pipe_data["dma_names"]
                )
                coords = NeomodelPoint(pipe_data["geometry"].coords[0][0], crs="wgs-84")

                PipeEnd.create(
                    {"gid": pipe_gid, "dmas": dma_data, "pipe_type": pipe_type}
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
        # for asset_positions in self.all_asset_positions:
        #     for asset_data in asset_positions:
        #         if (
        #             asset_data["data"]["id"]
        #             in [21, 53, 60, 62, 81, 85, 87, 201, 213, 241, 252, 277, 538]
        #             and asset_data["data"]["asset_name"] == "trunk_main"
        #         ):
        #             import pdb

        #             pdb.set_trace()
        self._set_pipe_connected_asset_relations()
