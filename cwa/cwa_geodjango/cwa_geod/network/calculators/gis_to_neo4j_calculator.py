from multiprocessing.pool import ThreadPool
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
    PIPE_END__NAME,
    POINT_ASSET__NAME,
)


MIXED_NODE_TYPES_SORTED = [
    sorted([PIPE_JUNCTION__NAME, POINT_ASSET__NAME]),
    sorted([PIPE_END__NAME, POINT_ASSET__NAME]),
]


class GisToNeo4jCalculator(GisToGraphCalculator):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config

        self.all_base_pipes = []
        self.all_nodes_ordered = []

        super().__init__(
            self.config.srid,
            processor_count=config.processor_count,
            chunk_size=config.chunk_size,
        )

    def _connect_nodes(self, base_pipe, start_node, end_node):

        match_query = f"""match (n {{node_key:'{start_node['node_key']}'}})-
        [r:TrunkMain]-
        (m {{node_key:'{end_node['node_key']}'}}) return count(r)
        """

        if db.cypher_query(match_query)[0][0][0] == 0:
            query = f"""match (n {{node_key:'{start_node['node_key']}'}}),
            (m {{node_key:'{end_node['node_key']}'}})
            create (n)-[:{base_pipe['asset_label']} {{
            gid: {base_pipe["gid"]},
            utility: '{start_node['utility']}'
            }}]->(m)"""
            # "pipe_type": base_pipe["asset_name"],

            db.cypher_query(query)

    @staticmethod
    def _get_node_by_key(node_key):
        point_node = db.cypher_query(
            f"""match (n {{node_key:'{node_key}'}})
        return n"""
        )[0]

        if point_node:
            return point_node[0][0]

        return None

    @staticmethod
    def create_node_asset_query(node_properties):
        props = f"""
        utility:'{node_properties['utility']}',
        coords_27700: {node_properties['coords_27700']},
        node_key:'{node_properties['node_key']}',
        dmas:'{node_properties['dmas']}',
        node_types: {node_properties['node_types']},
        asset_names: {node_properties['point_asset_names']},
        asset_gids: {node_properties['point_asset_gids']},
        """

        asset_gids = [
            f"{key}: {val}"
            for key, val in node_properties["point_assets_with_gids"].items()
        ]

        acoustic_logger = node_properties.get("acoustic_logger")
        subtype = node_properties.get("subtype")

        point = f"""location: point(
        {{latitude: {node_properties['coords_4326'][0]},
         longitude: {node_properties['coords_4326'][1]}}}
        )"""

        query = f"CREATE (n:{('&').join(node_properties['node_labels'])} {{"
        query += props

        query += f"{(', ').join(asset_gids)},"

        if acoustic_logger:
            query += f"acoustic_logger: '{acoustic_logger}',"

        if subtype:
            query += f"subtype: '{subtype}',"

        query += point
        query += f"}}) return n"

        return query

    @staticmethod
    def create_pipe_node_query(node_properties):

        query = f"""CREATE (
        n:{('&').join(node_properties['node_labels'])}
        {{utility:'{node_properties['utility']}',
        coords_27700: {node_properties['coords_27700']},
        node_key:'{node_properties['node_key']}',
        dmas:'{node_properties['dmas']}',
        location: point(
        {{latitude: {node_properties['coords_4326'][0]},
        longitude: {node_properties['coords_4326'][1]}}}
        )
        }}) return n
        """
        return query

    def _get_or_create_pipe_and_asset_node(self, node_properties):

        try:
            query = self.create_node_asset_query(node_properties)
            return db.cypher_query(query)[0][0][0]

        except UniqueProperty:
            return self._get_node_by_key(node_properties["node_key"])

    def _get_or_create_point_asset_node(self, node_properties):

        try:
            query = self.create_node_asset_query(node_properties)
            return db.cypher_query(query)[0][0][0]

        except UniqueProperty:
            return self._get_node_by_key(node_properties["node_key"])

    def _create_pipe_junction_or_end_node(self, node_properties):

        try:
            query = self.create_pipe_node_query(node_properties)
            return db.cypher_query(query)[0][0][0]

        except UniqueProperty:
            return self._get_node_by_key(node_properties["node_key"])

    def _create_nodes(self, all_node_properties):

        all_nodes = []
        for node_properties in all_node_properties:

            node_key = node_properties.get("node_key")

            point_node = self._get_node_by_key(node_key)

            if point_node:
                all_nodes.append(point_node)
                continue

            node_types = sorted(node_properties.get("node_types"))

            if node_types == [PIPE_JUNCTION__NAME] or node_types == [PIPE_END__NAME]:
                node = self._create_pipe_junction_or_end_node(node_properties)
                all_nodes.append(node)

            elif node_types == [POINT_ASSET__NAME]:
                node = self._get_or_create_point_asset_node(node_properties)
                all_nodes.append(node)

            elif node_types in MIXED_NODE_TYPES_SORTED:
                node = self._get_or_create_pipe_and_asset_node(node_properties)
                all_nodes.append(node)

        return all_nodes

    def _create_relations(self, base_pipe, all_nodes):
        current_node = all_nodes[0]

        for next_node in all_nodes[1:]:
            # need to sort to ensure cardinality is maintained
            sorted_nodes = sorted(
                [current_node, next_node], key=lambda node: node["node_key"]
            )

            self._connect_nodes(base_pipe, sorted_nodes[0], sorted_nodes[1])
            current_node = next_node

    def _map_pipe_connected_asset_relations(
        self, base_pipe: dict, all_node_properties: list
    ):

        all_nodes = self._create_nodes(all_node_properties)
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
