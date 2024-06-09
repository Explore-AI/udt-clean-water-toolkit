from multiprocessing.pool import ThreadPool
from django.contrib.gis.geos import Point
from neomodel.contrib.spatial_properties import NeomodelPoint
from neomodel import db
from neomodel.exceptions import UniqueProperty
from cleanwater.transform import GisToGraph
from cwageodjango.core.constants import (
    PIPE_JUNCTION__NAME,
    PIPE_END__NAME,
    POINT_ASSET__NAME,
)
from cwageodjango.config.settings import sqids


MIXED_NODE_TYPES_SORTED = [
    sorted([PIPE_JUNCTION__NAME, POINT_ASSET__NAME]),
    sorted([PIPE_END__NAME, POINT_ASSET__NAME]),
]


def flatten_concatenation(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list


class GisToNeo4jCalculator2(GisToGraph):
    """Create a Neo4J graph of assets from a geospatial network of assets"""

    def __init__(self, config):
        self.config = config

        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []

        super().__init__(
            self.config.srid,
            sqids,
            processor_count=config.processor_count,
            chunk_size=config.chunk_size,
            neoj4_point=self.config.neoj4_point,
        )

    def _connect_nodes(self, edge_by_pipe, start_node, end_node):
        asset_label = edge_by_pipe["asset_label"]

        match_query = f"""match (n:NetworkNode {{node_key:'{start_node['node_key']}'}})-
        [r:{asset_label}]-
        (m:NetworkNode {{node_key:'{end_node['node_key']}'}}) return count(r)
        """

        if db.cypher_query(match_query)[0][0][0] == 0:
            query = f"""match (n:NetworkNode {{node_key:'{start_node['node_key']}'}}),
            (m:NetworkNode {{node_key:'{end_node['node_key']}'}})
            create (n)-[:{asset_label} {{
            gid: {edge_by_pipe["gid"]},
            material: '{edge_by_pipe["material"]}',
            diameter: '{edge_by_pipe["diameter"]}',
            segment_wkt: '{edge_by_pipe["segment_wkt"]}',
            segment_length: {edge_by_pipe["segment_length"]}
            }}]->(m)"""

            db.cypher_query(query)

    @staticmethod
    def _get_node_by_key(node_key):
        network_node = db.cypher_query(
            f"""match (n:NetworkNode {{node_key:'{node_key}'}})
        return n"""
        )[0]

        if network_node:
            return network_node[0][0]

        return None

    @staticmethod
    def create_node_asset_query(node_properties):
        props = f"""
        coords_27700: {node_properties['coords_27700']},
        node_key:'{node_properties['node_key']}',
        node_types: {node_properties['node_types']},
        asset_names: {node_properties['point_asset_names']},
        asset_gids: {node_properties['point_asset_gids']}
        """

        asset_gids = [
            f"{key}: {val}"
            for key, val in node_properties["point_assets_with_gids"].items()
        ]

        acoustic_logger = node_properties.get("acoustic_logger")
        subtype = node_properties.get("subtype")

        query = f"CREATE (n:{('&').join(node_properties['node_labels'])} {{"
        query += props

        query += f",{(', ').join(asset_gids)}"

        if acoustic_logger:
            query += f", acoustic_logger: '{acoustic_logger}'"

        if subtype:
            query += f", subtype: '{subtype}'"

        query += f"}}) return n"

        return query

    @staticmethod
    def create_pipe_node_query(node_properties):
        query = f"""CREATE (
        n:{('&').join(node_properties['node_labels'])}
        {{utility:'{node_properties['utility']}',
        coords_27700: {node_properties['coords_27700']},
        node_key:'{node_properties['node_key']}'
        }}) return n
        """
        return query

    def _get_or_create_dma_node(self, dma_code, dma_name):
        """Create or get a DMA node."""

        query = f"""MERGE (d:DMA {{code: '{dma_code}'}})
                    ON CREATE SET d.name = '{dma_name}'
                    RETURN d"""

        result = db.cypher_query(query)
        return result[0][0][0]

    def _get_or_create_utility_node(self, utility_name):
        """Create or get a Utility node."""
        query = f"""MERGE (u:Utility {{name: '{utility_name}'}})
                    RETURN u"""

        result = db.cypher_query(query)
        return result[0][0][0]

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

    def set_dynamic_node_properties(self):

        subquery = """
        n.node_types = CASE WHEN node.node_types IS NOT NULL THEN node.node_types ELSE NULL END,
        n.asset_names = CASE WHEN node.point_asset_names IS NOT NULL THEN node.point_asset_names ELSE NULL END,
        n.asset_gids = CASE WHEN node.point_asset_gids IS NOT NULL THEN node.point_asset_gids ELSE NULL END,
        """
        for point_asset in self.point_asset_gid_names:
            subquery += f"""n.{point_asset} = CASE WHEN node.{point_asset}
            IS NOT NULL THEN node.{point_asset}
            ELSE NULL END,\n"""

        # TODO: Fix this string slice. Highly likely this could cause a bug
        return subquery[:-2]

    @staticmethod
    def set_static_node_properties():
        return """
        n.node_key = node.node_key,
        n.coords_27700 = node.coords_27700,
        """

    def set_node_labels(self):

        subquery = ""
        for node_label in self.network_node_labels:
            subquery += f"""FOREACH (ignoreMe IN CASE
            WHEN '{node_label}' IN node.node_labels
            THEN [1] ELSE [] END |
            SET n:{node_label})\n"""

        return subquery

    def _create_nodes(self, all_unique_nodes):

        query = f"""UNWIND $all_unique_nodes AS node
         MERGE (n:NetworkNode {{node_key: node.node_key}})
         ON CREATE
             SET n.createdAt = timestamp()
             {self.set_node_labels()}
         SET
         {self.set_static_node_properties()}
         {self.set_dynamic_node_properties()}
         RETURN n
         """

        db.cypher_query(query, {"all_unique_nodes": all_unique_nodes})

        return

    def _get_or_create_utility_node_rel(self, node, utility_name):
        utility_node = self._get_or_create_utility_node(utility_name)
        self._create_utility_relationship(node, utility_node)

    def _get_or_create_dma_node_rel(self, node, dma_codes, dma_names):

        for dma_code, dma_name in zip(dma_codes, dma_names):
            dma_node = self._get_or_create_dma_node(dma_code, dma_name)
            self._create_dma_relationship(node, dma_node)

    def _create_relations(self, edges_by_pipe, all_nodes):
        current_node = all_nodes[0]

        for next_node, edge_by_pipe in zip(all_nodes[1:], edges_by_pipe):
            sorted_nodes = sorted(
                [current_node, next_node], key=lambda node: node["node_key"]
            )

            self._connect_nodes(edge_by_pipe, sorted_nodes[0], sorted_nodes[1])
            current_node = next_node

    def _create_dma_relationship(self, node, dma_node):
        query = f"""MATCH (n:NetworkNode {{node_key: '{node["node_key"]}'}}), (d:DMA {{code: '{dma_node["code"]}'}})
                    CREATE (n)-[:HAS_DMA]->(d)"""
        db.cypher_query(query)

    def _create_utility_relationship(self, node, utility_node):
        query = f"""MATCH (n:NetworkNode {{node_key: '{node["node_key"]}'}}), (u:Utility {{name: '{utility_node["name"]}'}})
                    CREATE (n)-[:HAS_UTILITY]->(u)"""
        db.cypher_query(query)

    def _map_pipe_connected_asset_relations(
        self, all_unique_nodes: list, all_unique_edges: list
    ):
        all_nodes = self._create_nodes(all_unique_nodes)
        self._create_relations(edges_by_pipe, all_nodes)

    def _get_unique_nodes_and_edges(self):
        all_nodes = flatten_concatenation(self.all_nodes_by_pipe)
        all_edges = flatten_concatenation(self.all_edges_by_pipe)

        unique_node_keys = []
        all_unique_nodes = []
        for node in all_nodes:
            node_key = node["node_key"]
            if node_key not in unique_node_keys:
                all_unique_nodes.append(node)
                unique_node_keys.append(node)

        unique_edge_keys = []
        all_unique_edges = []
        for edge in all_edges:
            edge_key = edge["edge_key"]
            if edge_key not in unique_edge_keys:
                all_unique_edges.append(edge)
                unique_edge_keys.append(edge_key)

        return all_unique_nodes, all_unique_edges

    def _reset_pipe_asset_data(self):
        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []

    def create_neo4j_graph(self) -> None:

        all_unique_nodes, all_unique_edges = self._get_unique_nodes_and_edges()

        self._map_pipe_connected_asset_relations(
            all_unique_nodes,
            all_unique_edges,
        )
        self._reset_pipe_asset_data()

    def _create_neo4j_graph_parallel(self) -> None:
        with ThreadPool(self.config.thread_count) as p:
            p.starmap(
                self._map_pipe_connected_asset_relations,
                zip(self.all_edges_by_pipe, self.all_nodes_by_pipe),
            )
        self._reset_pipe_asset_data()
