import pdb
from multiprocessing.pool import ThreadPool
from neomodel import db
from collections import defaultdict
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


class GisToNeo4jCalculator3(GisToGraph):
    """Create a Neo4J graph of assets from a geospatial network of assets"""

    def __init__(self, config):
        self.config = config
        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []
        self.dma_nodes = set()
        self.utility_nodes = set()
        self.dma_relationships = []
        self.utility_relationships = []
        self.point_assets = []  # To store point assets information

        super().__init__(
            self.config.srid,
            sqids,
            processor_count=config.processor_count,
            chunk_size=config.chunk_size,
            neoj4_point=self.config.neoj4_point,
        )

    def _get_unique_nodes_and_edges(self):
        all_nodes = flatten_concatenation(self.all_nodes_by_pipe)
        all_edges = flatten_concatenation(self.all_edges_by_pipe)

        unique_node_keys = set()
        all_unique_nodes = []
        for node in all_nodes:
            node_key = node["node_key"]
            if node_key not in unique_node_keys:
                all_unique_nodes.append(node)
                unique_node_keys.add(node_key)

        unique_edge_keys = set()
        all_unique_edges = []
        for edge in all_edges:
            edge_key = edge["edge_key"]
            if edge_key not in unique_edge_keys:
                all_unique_edges.append(edge)
                unique_edge_keys.add(edge_key)

        return all_unique_nodes, all_unique_edges

    def _batch_create_network_nodes(self, all_unique_nodes):
        pipe_nodes = []
        for node in all_unique_nodes:
            # Identify pipe nodes and separate point assets
            for label in node['node_labels']:
                if label in self.network_node_labels:
                    pipe_nodes.append(node)

                # Check if the node has point assets
                if label in self.network_node_asset_labels:
                    self.point_assets.append(node)

        # Create pipe nodes only with relevant pipe labels
        query = f"""UNWIND $pipe_nodes AS node
            MERGE (n:NetworkNode {{node_key: node.node_key}})
            ON CREATE
                SET n.createdAt = timestamp()
                {self.set_pipe_node_labels()}
            SET
            {self.set_static_node_properties()}
            RETURN n
            """
        db.cypher_query(query, {"pipe_nodes": pipe_nodes})
        self._collect_dma_and_utility_data(pipe_nodes)
        self._create_asset_nodes_and_relationships()

    def _create_asset_nodes_and_relationships(self):
        for node in self.point_assets:
            node_key = node['node_key']
            point_assets = node.get('point_asset_names', [])
            point_gids = node.get('point_asset_gids', [])
            has_logger = 'Logger' in node.get('node_labels', [])

            for asset_name, gid in zip(point_assets, point_gids):
                asset_node = {
                    'node_key': f"{node_key}_{gid}",
                    'gid': gid,
                    'node_label': asset_name,
                    'AcousticLogger': has_logger  # Set AcousticLogger attribute
                }

                # Create the asset node
                query = f"""MERGE (a:AssetNode:{asset_name} {{node_key: $node_key}})
                    ON CREATE 
                    SET
                    a.createdAt = timestamp(),
                    a.gid = $gid,
                    a.AcousticLogger = $AcousticLogger
                    RETURN a
                """
                db.cypher_query(query, asset_node)

                # Create a relationship from the pipe node to the asset node
                rel_query = f"""
                     MATCH (n:NetworkNode {{node_key: $pipe_node_key}}), (a:AssetNode {{node_key: $asset_node_key}})
                     MERGE (n)-[:HAS_ASSET]->(a)
                 """
                db.cypher_query(rel_query, {"pipe_node_key": node_key, "asset_node_key": asset_node['node_key']})

    def set_pipe_node_labels(self):
        subquery = ""
        for node_label in self.network_node_labels:
            subquery += f"""FOREACH (ignoreMe IN CASE
            WHEN '{node_label}' IN node.node_labels 
            AND NOT '{node_label}' IN {self.network_node_asset_labels}
            AND NOT '{node_label}' = 'Logger'
            THEN [1] ELSE [] END |
            SET n:{node_label})\n"""
        return subquery

    @staticmethod
    def set_static_node_properties():
        return """
        n.node_key = node.node_key,
        n.coords_27700 = node.coords_27700
        """

    def _batch_create_pipe_relations(self, all_unique_edges):
        grouped_edges = defaultdict(list)
        for edge in all_unique_edges:
            grouped_edges[edge['asset_label']].append(edge)

        for asset_label, edges in grouped_edges.items():
            query = f"""
            UNWIND $edges AS edge
            MATCH (n:NetworkNode {{node_key: edge.from_node_key}}),
                  (m:NetworkNode {{node_key: edge.to_node_key}})
            MERGE (n)-[r:{asset_label} {{
                gid: edge.gid,
                material: edge.material,
                diameter: edge.diameter,
                segment_wkt: edge.segment_wkt,
                segment_length: edge.segment_length
                }}]-(m)
            ON CREATE
                SET r.createdAt = timestamp()
            RETURN r
            """
            db.cypher_query(query, {"edges": edges})

    def _collect_dma_and_utility_data(self, all_unique_nodes):
        """Collects unique DMA and Utility nodes and relationships for batching."""
        for node in all_unique_nodes:
            # Collect DMA nodes and relationships
            if 'dma_codes' in node and 'dma_names' in node:
                for dma_code, dma_name in zip(node['dma_codes'], node['dma_names']):
                    self.dma_nodes.add((dma_code, dma_name))
                    self.dma_relationships.append((node['node_key'], dma_code))

            # Collect Utility nodes and relationships
            if 'utility_name' in node:
                self.utility_nodes.add(node['utility_name'])
                self.utility_relationships.append((node['node_key'], node['utility_name']))

    def _batch_create_dma_nodes(self):
        """Batch creates DMA nodes."""
        query = f"""
        UNWIND $dma_nodes AS dma
        MERGE (d:DMA {{code: dma.code}})
        ON CREATE SET d.name = dma.name
        RETURN d
        """
        db.cypher_query(query, {"dma_nodes": [{"code": code, "name": name} for code, name in self.dma_nodes]})

    def _batch_create_utility_nodes(self):
        """Batch creates Utility nodes."""
        query = f"""
        UNWIND $utility_nodes AS utility
        MERGE (u:Utility {{name: utility}})
        RETURN u
        """
        db.cypher_query(query, {"utility_nodes": list(self.utility_nodes)})

    def _batch_create_dma_relationships(self):
        """Batch creates relationships between NetworkNodes and DMA nodes."""
        query = f"""
        UNWIND $dma_rels AS rel
        MATCH (n:NetworkNode {{node_key: rel.node_key}}), (d:DMA {{code: rel.dma_code}})
        MERGE (n)-[:HAS_DMA]->(d)
        """
        db.cypher_query(query, {"dma_rels": [{"node_key": node_key, "dma_code": dma_code} for node_key, dma_code in self.dma_relationships]})

    def _batch_create_utility_relationships(self):
        """Batch creates relationships between NetworkNodes and Utility nodes."""
        query = f"""
        UNWIND $utility_rels AS rel
        MATCH (n:NetworkNode {{node_key: rel.node_key}}), (u:Utility {{name: rel.utility_name}})
        MERGE (n)-[:HAS_UTILITY]->(u)
        """
        db.cypher_query(query, {"utility_rels": [{"node_key": node_key, "utility_name": utility_name} for node_key, utility_name in self.utility_relationships]})

    def _map_pipe_connected_asset_relations(self, all_unique_nodes, all_unique_edges):
        self._batch_create_network_nodes(all_unique_nodes)
        self._batch_create_pipe_relations(all_unique_edges)

        # Batch create DMA and Utility nodes
        self._batch_create_dma_nodes()
        self._batch_create_utility_nodes()

        # Batch create relationships between network nodes and DMA/Utility nodes
        self._batch_create_dma_relationships()
        self._batch_create_utility_relationships()

    def _reset_pipe_asset_data(self):
        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []
        self.point_assets = []  # Reset point assets data as well

    def create_neo4j_graph(self) -> None:
        all_unique_nodes, all_unique_edges = self._get_unique_nodes_and_edges()
        self._map_pipe_connected_asset_relations(all_unique_nodes, all_unique_edges)
        self._reset_pipe_asset_data()

    def _create_neo4j_graph_parallel(self) -> None:
        with ThreadPool(self.config.thread_count) as p:
            p.starmap(
                self._map_pipe_connected_asset_relations,
                zip(self.all_edges_by_pipe, self.all_nodes_by_pipe),
            )
        self._reset_pipe_asset_data()
