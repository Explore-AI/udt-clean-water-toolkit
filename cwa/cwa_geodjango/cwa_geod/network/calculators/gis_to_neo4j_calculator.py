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
    PIPE_JUNCTION__NAME,
    TRUNK_MAIN__NAME,
    DISTRIBUTION_MAIN__NAME,
    PIPE_END__NAME,
    POINT_ASSET__NAME,
)
from ..models import PointAsset, PipeEnd, PointNode, PipeJunction


class GisToNeo4jCalculator(GisToGraphCalculator):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        super().__init__(config)

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

        # end_neo_point = NeomodelPoint(
        #     (end_geom_latlong.x, end_geom_latlong.y), crs="wgs-84"
        # )

    @staticmethod
    def _get_or_create_pipe_junctions_node(base_pipe, node_properties):

        node_id = node_properties.get("node_id")
        gids = node_properties.get("gids")
        dmas = node_properties.get("dmas")
        # pipe_type = node_properties.get("asset_name") #TODO: re-add pipe types.
        utility = base_pipe.get("utility_name")

        try:
            # TODO: would neomodel get_or_create work better here?
            return PipeJunction.create(
                {"node_id": node_id, "dmas": dmas, "gids": gids, "utility": utility}
            )[0]
        except UniqueProperty:
            return PipeJunction.nodes.get_or_none(node_id=node_id)

    @staticmethod
    def _get_or_create_pipe_end_node(base_pipe, node_properties):

        node_id = node_properties.get("node_id")
        gid = node_properties.get("gid")
        dmas = node_properties.get("dmas")
        # pipe_type = node_properties.get("asset_name") #TODO: re-add pipe types.
        utility = base_pipe.get("utility_name")

        try:
            # TODO: would neomodel get_or_create work better here?
            return PipeEnd.create(
                {"node_id": node_id, "dmas": dmas, "gid": gid, "utility": utility}
            )[0]
        except UniqueProperty:
            return PipeEnd.nodes.get_or_none(node_id=node_id)

    @staticmethod
    def _get_or_create_point_asset_node(base_pipe, node_properties):

        asset_name = node_properties.get("asset_name")
        asset_model = PointAsset.asset_name_model_mapping(asset_name)

        node_id = node_properties.get("node_id")
        gid = node_properties.get("gid")
        dmas = node_properties.get("dmas")
        utility = base_pipe.get("utility_name")

        try:
            # TODO: would neomodel get_or_create work better here?
            return asset_model.create(
                {"node_id": node_id, "dmas": dmas, "gid": gid, "utility": utility}
            )[0]
        except UniqueProperty:
            return asset_model.nodes.get_or_none(node_id=node_id)

    def _create_nodes(self, base_pipe, all_node_properties):

        created_nodes = []
        for node_properties in all_node_properties:

            node_id = node_properties.get("node_id")

            point_node = PointNode.nodes.get_or_none(node_id=node_id)

            if point_node:
                created_nodes.append(point_node)
                continue

            node_type = node_properties.get("node_type")

            if node_type == PIPE_JUNCTION__NAME:
                node = self._get_or_create_pipe_junctions_node(
                    base_pipe, node_properties
                )
                created_nodes.append(node)

            elif node_type == PIPE_END__NAME:
                node = self._get_or_create_pipe_end_node(base_pipe, node_properties)
                created_nodes.append(node)

            elif node_type == POINT_ASSET__NAME:
                node = self._get_or_create_point_asset_node(base_pipe, node_properties)
                created_nodes.append(node)

        start_node = created_nodes[0]
        for node in created_nodes[1:]:
            self._connect_nodes(
                start_node,
                node,
                base_pipe["asset_name"],
                {
                    "dmas": base_pipe["dmas"],
                    "gid": base_pipe["gid"],
                    "utility": base_pipe["utility_name"],
                },
            )
            start_node = node

    def _map_pipe_connected_asset_relations(
        self, base_pipe: dict, all_node_properties: list
    ):
        # pipe_end = PipeEnd.nodes.get_or_none(pipe_type=pipe_type, gid=pipe_gid)

        # dma_data = self.build_dma_data_as_json(
        #     pipe_data["dma_codes"], pipe_data["dma_names"]
        # )

        self._create_nodes(base_pipe, all_node_properties)

        # pipe_start_node, pipe_segment_id = self._set_pipe_start_node(
        #     pipe_data, dma_data
        # )

        # pipe_second_last_node, pipe_segment_id = self._set_connected_asset_relations(
        #     pipe_data, assets_data, pipe_start_node, pipe_segment_id
        # )

        # self._set_pipe_end_node(
        #     pipe_data, dma_data, pipe_second_last_node, pipe_segment_id
        # )

    def _reset_pipe_asset_data(self):
        # reset all_pipe_data and all_asset_positions to manage memory
        self.all_base_pipes = []
        self.all_nodes_ordered = []

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
                self.all_base_pipes,
                self.all_nodes_ordered,
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
                zip(self.all_base_pipes, self.all_nodes_ordered),
            )

        self._reset_pipe_asset_data()
