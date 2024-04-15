from multiprocessing.pool import ThreadPool
from django.db.models.query import QuerySet
from django.contrib.gis.geos import Point
from neomodel.contrib.spatial_properties import NeomodelPoint
from neomodel import db
from neomodel.exceptions import UniqueProperty
from cleanwater.exceptions import (
    InvalidPipeException,
)
from cleanwater.calculators import GisToGraphCalculator
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

        self.all_base_pipes = []
        self.all_nodes_ordered = []

        super().__init__(config)

    def _connect_nodes(self, base_pipe, start_node, end_node):

        if not start_node.trunk_main.relationship(
            end_node
        ) and not start_node.distribution_main.relationship(end_node):

            relation_data = {
                # "relation_id": relation_id,
                "dmas": base_pipe["dmas"],
                "gid": base_pipe["gid"],
                "utility": base_pipe["utility_name"],
            }
            pipe_name = base_pipe["asset_name"]

            if pipe_name == TRUNK_MAIN__NAME:
                start_node.trunk_main.connect(end_node, relation_data)
            elif pipe_name == DISTRIBUTION_MAIN__NAME:
                start_node.distribution_main.connect(end_node, relation_data)
            else:
                InvalidPipeException(f"Invalid pipe detected: {pipe_name}.")

        # end_neo_point = NeomodelPoint(
        #     (end_geom_latlong.x, end_geom_latlong.y), crs="wgs-84"
        # )

    def _get_or_create_pipe_junctions_node(self, base_pipe, node_properties):

        node_id = node_properties.get("node_id")
        gids = node_properties.get("gids")
        dmas = node_properties.get("dmas")
        geom = node_properties.get("intersection_point_geometry")
        # pipe_type = node_properties.get("asset_name") #TODO: re-add pipe types.
        utility = base_pipe.get("utility_name")

        try:
            # TODO: would neomodel get_or_create work better here?
            return PipeJunction.create(
                {
                    "node_id": node_id,
                    "dmas": dmas,
                    "gids": gids,
                    "utility": utility,
                    # TODO: why does geom.x return a numpy array
                    "x_coord": geom.coords[0],
                    "y_coord": geom.coords[1],
                }
            )[0]
        except UniqueProperty:
            return PipeJunction.nodes.get_or_none(node_id=node_id)

    def _get_or_create_pipe_end_node(self, base_pipe, node_properties):
        node_id = node_properties.get("node_id")
        gid = node_properties.get("gid")
        dmas = node_properties.get("dmas")
        geom = node_properties.get("intersection_point_geometry")
        # pipe_type = node_properties.get("asset_name") #TODO: re-add pipe types.
        utility = base_pipe.get("utility_name")

        try:
            # TODO: would neomodel get_or_create work better here?
            return PipeEnd.create(
                {
                    "node_id": node_id,
                    "dmas": dmas,
                    "gid": gid,
                    "utility": utility,
                    # TODO: why does geom.x return a numpy array
                    "x_coord": geom.coords[0],
                    "y_coord": geom.coords[1],
                }
            )[0]
        except UniqueProperty:
            return PipeEnd.nodes.get_or_none(node_id=node_id)

    def _get_or_create_point_asset_node(self, base_pipe, node_properties):

        asset_name = node_properties.get("asset_name")
        asset_model = PointAsset.asset_name_model_mapping(asset_name)

        node_id = node_properties.get("node_id")
        gid = node_properties.get("gid")
        dmas = node_properties.get("dmas")
        geom = node_properties.get("intersection_point_geometry")
        utility = base_pipe.get("utility_name")

        try:
            # TODO: would neomodel get_or_create work better here?
            return asset_model.create(
                {
                    "node_id": node_id,
                    "dmas": dmas,
                    "gid": gid,
                    "utility": utility,
                    # TODO: why does geom.x return a numpy array
                    "x_coord": geom.coords[0],
                    "y_coord": geom.coords[1],
                }
            )[0]
        except UniqueProperty:
            return asset_model.nodes.get_or_none(node_id=node_id)

    def _create_nodes(self, base_pipe, all_node_properties):

        all_nodes = []
        for node_properties in all_node_properties:

            node_key = node_properties.get("node_key")

            point_node = PointNode.nodes.get_or_none(node_key=node_key)

            if point_node:
                all_nodes.append(point_node)
                continue

            node_types = sorted(node_properties.get("node_types"))

            import pdb

            pdb.set_trace()
            if node_types == [PIPE_JUNCTION__NAME]:
                # node = self._get_or_create_pipe_junctions_node(
                #     base_pipe, node_properties
                # )

                pass
            # all_nodes.append(node)

            elif node_types == [PIPE_END__NAME]:
                node = self._get_or_create_pipe_end_node(base_pipe, node_properties)
                all_nodes.append(node)

            elif node_types == [POINT_ASSET__NAME]:
                node = self._get_or_create_pipe_end_node(base_pipe, node_properties)
                all_nodes.append(node)

            elif node_types == [PIPE_JUNCTION__NAME, POINT_ASSET__NAME]:
                # node = self._get_or_create_point_asset_node(base_pipe, node_properties)
                # query = f""
                query = f"CREATE (n:PipeJunction&PointAsset&PressureFitting {{utility='thames_water', coords_27700: {node_properties['coords_27700']}, node_key={node_properties['node_key']}, dmas:'{node_properties['dmas']}', node_types: {node_properties['node_types']}, pipe_gids: {node_properties['pipe_gids']}  }})"

                import pdb

                pdb.set_trace()
                node = db.cypher_query(query)
                all_nodes.append(node)

            elif node_types == [PIPE_END__NAME, POINT_ASSET__NAME]:
                node = self._get_or_create_point_asset_node(base_pipe, node_properties)
                all_nodes.append(node)

        # if self.base_pipe["gid"] == 838147:
        #     import pdb

        #     pdb.set_trace()

        return all_nodes

    def _create_relations(self, base_pipe, all_nodes):
        current_node = all_nodes[0]

        for next_node in all_nodes[1:]:
            # need to sort to ensure cardinality is maintained
            sorted_nodes = sorted([current_node, next_node], key=lambda x: x.node_id)

            self._connect_nodes(base_pipe, sorted_nodes[0], sorted_nodes[1])
            current_node = next_node

    def _map_pipe_connected_asset_relations(
        self, base_pipe: dict, all_node_properties: list
    ):

        all_nodes = self._create_nodes(base_pipe, all_node_properties)
        self._create_relations(base_pipe, all_nodes)

    def _reset_pipe_asset_data(self):
        # reset all_pipe_data and all_asset_positions to manage memory
        self.all_base_pipes = []
        self.all_nodes_ordered = []

    def create_neo4j_graph(self) -> None:
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
