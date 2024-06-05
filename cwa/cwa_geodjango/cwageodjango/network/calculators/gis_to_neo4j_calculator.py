from multiprocessing.pool import ThreadPool
from django.contrib.gis.geos import Point
from neomodel.contrib.spatial_properties import NeomodelPoint
import json
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


class GisToNeo4jCalculator(GisToGraph):
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

    @staticmethod
    def _get_dma_by_code(dma_code):
        dma_node = db.cypher_query(
            f"""match (n:DMA {{code:'{dma_code}'}})
            return n"""
        )[0]

        if dma_node:
            return dma_node[0][0]

        import pdb

        pdb.set_trace()
        return None

    # def _get_or_create_dma_node(self, dma_code, dma_name):
    #     """Create or get a DMA node."""

    #     try:
    #         query = f"""CREATE (
    #         d:DMA {{code: '{dma_code}',
    #         name: '{dma_name}'
    #         }}) RETURN d
    #         """

    #         result = db.cypher_query(query)
    #         return result[0][0][0]

    #     except UniqueProperty:
    #         return self._get_dma_by_code(dma_code)

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

    def _create_nodes(self, all_node_properties):
        all_nodes = []
        for node_properties in all_node_properties:
            node_key = node_properties.get("node_key")
            network_node = self._get_node_by_key(node_key)

            if network_node:
                all_nodes.append(network_node)
                continue

            node_types = sorted(node_properties.get("node_types"))

            if node_types == [PIPE_JUNCTION__NAME] or node_types == [PIPE_END__NAME]:
                node = self._create_pipe_junction_or_end_node(node_properties)
            elif node_types == [POINT_ASSET__NAME]:
                node = self._get_or_create_point_asset_node(node_properties)
            elif node_types in MIXED_NODE_TYPES_SORTED:
                node = self._get_or_create_pipe_and_asset_node(node_properties)

            all_nodes.append(node)

            # Handle DMA relationship
            dma_codes = node_properties.get("dma_codes")
            dma_names = node_properties.get("dma_names")
            self._get_or_create_dma_node_rel(node, dma_codes, dma_names)

            # # Handle Utility relationship
            utility_name = node_properties.get("utility")
            self._get_or_create_utility_node_rel(node, utility_name)

        return all_nodes

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
        self, edges_by_pipe: dict, all_node_properties: list
    ):
        all_nodes = self._create_nodes(all_node_properties)
        self._create_relations(edges_by_pipe, all_nodes)

    def _reset_pipe_asset_data(self):
        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []

    def create_neo4j_graph(self) -> None:
        list(
            map(
                self._map_pipe_connected_asset_relations,
                self.all_edges_by_pipe,
                self.all_nodes_by_pipe,
            )
        )
        self._reset_pipe_asset_data()

    def _create_neo4j_graph_parallel(self) -> None:
        with ThreadPool(self.config.thread_count) as p:
            p.starmap(
                self._map_pipe_connected_asset_relations,
                zip(self.all_edges_by_pipe, self.all_nodes_by_pipe),
            )
        self._reset_pipe_asset_data()
