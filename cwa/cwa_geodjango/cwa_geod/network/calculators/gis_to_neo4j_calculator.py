import json
from multiprocessing.pool import ThreadPool
from django.db.models.query import QuerySet
from django.contrib.gis.geos import Point
from neomodel.contrib.spatial_properties import NeomodelPoint
from neomodel.exceptions import UniqueProperty, ConstraintValidationFailed
from cleanwater.exceptions import (
    InvalidNodeException,
    InvalidPipeException,
)
from . import GisToGraphCalculator
from cwa_geod.core.constants import (
    TRUNK_MAIN__NAME,
    DISTRIBUTION_MAIN__NAME,
    PIPE_END__NAME,
    POINT_ASSET__NAME,
)
from ..models import PointAsset, PipeEnd


class GisToNeo4jCalculator(GisToGraphCalculator):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        super().__init__(config)

    def check_node_exists(self, asset_name, gid, utility_name, pipe_segment_id):
        node_type: str = self._get_node_type(asset_name)

        if node_type == PIPE_END__NAME:
            node = PipeEnd.nodes.get_or_none(
                pipe_type=asset_name,
                pipe_segment_id=f"{gid}-{pipe_segment_id}",
                gid=gid,
                utility=utility_name,
            )

            return node, node_type, None

        elif node_type == POINT_ASSET__NAME:
            asset_model = PointAsset.asset_name_model_mapping(asset_name)

            node = asset_model.nodes.get_or_none(gid=gid, utility=utility_name)
            return node, node_type, asset_model
        else:
            InvalidNodeException(
                f"Invalid node detected: {node_type}. Valid nodes are {PIPE_END__NAME} or {POINT_ASSET__NAME}"
            )

    @staticmethod
    def _connect_nodes(start_node, end_node, pipe_name, relation_data):
        try:
            if pipe_name == TRUNK_MAIN__NAME:
                start_node.trunk_main.connect(end_node, relation_data)
            elif pipe_name == DISTRIBUTION_MAIN__NAME:
                start_node.distribution_main.connect(end_node, relation_data)
            else:
                InvalidPipeException(f"Invalid pipe detected: {pipe_name}.")
        except ConstraintValidationFailed:
            pass

    def _create_and_connect_pipe_end_node(
        self,
        pipe_name,
        utility_name,
        pipe_segment_id,
        gid,
        asset_name,
        dma_data,
        start_node,
        coords,
    ):
        new_pipe_segment_id = pipe_segment_id + 1

        try:
            pipe_end = PipeEnd.create(
                {
                    "gid": gid,
                    "pipe_segment_id": f"{gid}-{new_pipe_segment_id}",
                    "dmas": dma_data,
                    "pipe_type": asset_name,
                    #            "location": coords,
                    "utility": utility_name,
                }
            )[0]
            pipe_segment_id = new_pipe_segment_id + 1
        except UniqueProperty:
            pipe_end = PipeEnd.nodes.get_or_none(
                pipe_type=asset_name,
                pipe_segment_id=f"{gid}-{pipe_segment_id}",
                gid=gid,
                utility=utility_name,
            )

        self._connect_nodes(
            start_node,
            pipe_end,
            pipe_name,
            {"dmas": dma_data, "gid": gid, "utility": utility_name},
        )

        return pipe_end, pipe_segment_id

    def _create_and_connect_point_asset_node(
        self, pipe_name, utility_name, gid, asset_model, dma_data, start_node, coords
    ):
        try:
            point_asset = asset_model.create(
                {
                    "gid": gid,
                    "dmas": dma_data,
                    # "location": coords,
                    "utility": utility_name,
                }
            )[0]
        except UniqueProperty:
            point_asset = asset_model.nodes.get_or_none(gid=gid, utility=utility_name)

        self._connect_nodes(
            start_node,
            point_asset,
            pipe_name,
            {"dmas": dma_data, "gid": gid, "utility": utility_name},
        )

        return point_asset

    def _set_connected_asset_relations(
        self, pipe_data: dict, assets_data: list, pipe_start_node, pipe_segment_id
    ) -> None:
        start_node = pipe_start_node

        for asset in assets_data:
            gid: int = asset["gid"]
            asset_name: str = asset["asset_name"]
            dma_data = self.build_dma_data_as_json(
                asset["dma_codes"], asset["dma_names"]
            )

            pipe_name = pipe_data["asset_name"]
            utility_name = pipe_data["utility_name"]

            # coords = NeomodelPoint(
            #     (
            #         asset["intersection_point_geom_latlong"].x,
            #         asset["intersection_point_geom_latlong"].y,
            #     ),
            #     crs="wgs-84",
            # )
            coords = None

            node, node_type, asset_model = self.check_node_exists(
                asset_name, gid, utility_name, pipe_segment_id
            )

            if not node and node_type == PIPE_END__NAME:
                start_node, pipe_segment_id = self._create_and_connect_pipe_end_node(
                    pipe_name,
                    utility_name,
                    pipe_segment_id,
                    gid,
                    asset_name,
                    dma_data,
                    start_node,
                    coords,
                )

            elif not node and node_type == POINT_ASSET__NAME:
                start_node = self._create_and_connect_point_asset_node(
                    pipe_name,
                    utility_name,
                    gid,
                    asset_model,
                    dma_data,
                    start_node,
                    coords,
                )

            elif node:
                start_node = node

            elif node_type not in [PIPE_END__NAME, POINT_ASSET__NAME]:
                raise InvalidNodeException(
                    f"Invalid node detected: {node_type}. Valid nodes are {PIPE_END__NAME} or {POINT_ASSET__NAME}"
                )

        return start_node, pipe_segment_id

    def _set_pipe_start_node(self, pipe_data, dma_data):
        pipe_gid = pipe_data.get("gid")
        pipe_type = pipe_data.get("asset_name")
        utility_name = pipe_data.get("utility_name")
        start_geom_4326 = pipe_data.get("start_geom_latlong")

        # start_neo_point = NeomodelPoint(
        #     (start_geom_4326.x, start_geom_4326.y), crs="wgs-84"
        # )
        pipe_segment_id = 0
        try:
            pipe_start_node = PipeEnd.create(
                {
                    "gid": pipe_gid,
                    "dmas": dma_data,
                    "pipe_type": pipe_type,
                    "pipe_segment_id": f"{pipe_gid}-{pipe_segment_id}",
                    # "location": start_neo_point,
                    "utility": utility_name,
                }
            )[0]
        except UniqueProperty:
            pipe_start_node = PipeEnd.nodes.get_or_none(
                pipe_type=pipe_type,
                pipe_segment_id=f"{pipe_gid}-{pipe_segment_id}",
                gid=pipe_gid,
                utility=utility_name,
            )

        return pipe_start_node, pipe_segment_id

    def _set_pipe_end_node(
        self, pipe_data, dma_data, pipe_second_last_node, pipe_segment_id
    ):
        pipe_gid = pipe_data.get("gid")
        pipe_type = pipe_data.get("asset_name")
        utility_name = pipe_data.get("utility_name")
        end_geom_latlong = pipe_data.get("end_geom_latlong")
        pipe_segment_id += 1  # increment segment_id

        # end_neo_point = NeomodelPoint(
        #     (end_geom_latlong.x, end_geom_latlong.y), crs="wgs-84"
        # )

        try:
            pipe_last_node = PipeEnd.create(
                {
                    "gid": pipe_gid,
                    "dmas": dma_data,
                    "pipe_type": pipe_type,
                    "pipe_segment_id": f"{pipe_gid}-{pipe_segment_id}",
                    #            "location": end_neo_point,
                    "utility": utility_name,
                }
            )[0]
        except UniqueProperty:
            pipe_last_node = PipeEnd.nodes.get_or_none(
                pipe_type=pipe_type,
                pipe_segment_id=f"{pipe_gid}-{pipe_segment_id}",
                gid=pipe_gid,
                utility=utility_name,
            )

        self._connect_nodes(
            pipe_second_last_node,
            pipe_last_node,
            pipe_type,
            {"dmas": dma_data, "gid": pipe_gid, "utility": utility_name},
        )

    def _map_pipe_connected_asset_relations(self, pipe_data: dict, assets_data: list):
        # pipe_end = PipeEnd.nodes.get_or_none(pipe_type=pipe_type, gid=pipe_gid)

        dma_data = self.build_dma_data_as_json(
            pipe_data["dma_codes"], pipe_data["dma_names"]
        )
        import pdb

        pdb.set_trace()

        pipe_start_node, pipe_segment_id = self._set_pipe_start_node(
            pipe_data, dma_data
        )

        pipe_second_last_node, pipe_segment_id = self._set_connected_asset_relations(
            pipe_data, assets_data, pipe_start_node, pipe_segment_id
        )

        self._set_pipe_end_node(
            pipe_data, dma_data, pipe_second_last_node, pipe_segment_id
        )

    def _reset_pipe_asset_data(self):
        # reset all_pipe_data and all_asset_positions to manage memory
        self.all_pipe_data = []
        self.all_asset_positions = []

    def _create_neo4j_graph(self) -> None:
        """Iterate over pipes and connect related pipe interactions
        and point assets. Uses a map method to operate on the pipe
        and asset data.

        Params:
              None
        Returns:
              None
        """

        list(
            map(
                self._map_pipe_connected_asset_relations,
                self.all_pipe_data,
                self.all_asset_positions,
            )
        )

        self._reset_pipe_asset_data()

    def _create_neo4j_graph_parallel(self) -> None:
        """Same as _create_neo4j_graph() except done in a multithreaded manner

        https://github.com/neo4j-contrib/neomodel/blob/master/test/test_multiprocessing.py

        Params:
              None
        Returns:
              None
        """

        with ThreadPool(self.config.thread_count) as p:
            p.starmap(
                self._map_pipe_connected_asset_relations,
                zip(self.all_pipe_data, self.all_asset_positions),
            )

        self._reset_pipe_asset_data()
