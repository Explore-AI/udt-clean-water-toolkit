import networkx as nx
from networkx import Graph
from cleanwater.calculators import GisToGraphCalculator
import bdb

class GisToNxCalculator(GisToGraphCalculator):
    """Create a NetworkX graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        self.G: Graph = Graph()
        self.all_base_pipes = []
        self.all_nodes_ordered = []
        super().__init__(self.config)

    def extract_assets_and_junctions(self):
        """Extract assets and junctions from the input data"""
        asset_keys = ['point_asset_names', 'node_id', 'pipe_gids']

        nodes_with_assets = [node for nodes in self.all_nodes_ordered
                             for node in nodes if asset_keys[0] in node]

        nodes_with_pipes = [node for nodes in self.all_nodes_ordered
                            for node in nodes if asset_keys[0] not in node]

        asset_dict = {}
        junctions_dict = {}

        for idx, src_dict in enumerate(nodes_with_assets, start=1):
            node_dict = {}

            for key in asset_keys[1:]:
                node_dict[key] = src_dict.get(key)

            asset_dict[f"feature_{idx}"] = node_dict

        for idx, src_dict in enumerate(nodes_with_pipes, start=1):
            node_dict = {}

            for key in asset_keys[1:]:
                node_dict[key] = src_dict.get(key)

            junctions_dict[f"feature_{idx}"] = node_dict

        return asset_dict, junctions_dict

    def build_adjacency_dict(self, junctions_dict):
        """Build an adjacency dictionary based on junctions"""
        adjacency_dict = {}

        for feature, info in junctions_dict.items():
            node_id = info['node_id']
            pipe_gids = info['pipe_gids']

            if pipe_gids:
                for pipe_gid in pipe_gids:
                    if pipe_gid not in adjacency_dict:
                        adjacency_dict[pipe_gid] = []

                    if node_id not in adjacency_dict[pipe_gid]:
                        adjacency_dict[pipe_gid].append(node_id)
            else:
                print(f"No pipe_gids found for node_id: {node_id}. Skipping...")

        return adjacency_dict

    def build_graph_from_adjacency(self, adjacency_dict):
        """Build a NetworkX graph from the adjacency dictionary"""
        for pipe_gid, node_ids in adjacency_dict.items():
            for node_id in node_ids:
                if node_id not in self.G.nodes:
                    self.G.add_node(node_id)

                for next_node_id in node_ids[node_ids.index(node_id) + 1:]:
                    self.G.add_edge(node_id, next_node_id, pipe_gid=pipe_gid)

        # Print nodes and edges to verify
        print("Nodes:", self.G.nodes())
        print("Edges:", self.G.edges(data=True))

    def integrate_coincident_nodes(self, asset_dict, junctions_dict):
        """Integrate coincident nodes from asset_dict into the graph"""
        for feature, asset_info in asset_dict.items():
            asset_pipe_gids = asset_info['pipe_gids']
            asset_node_id = asset_info['node_id']

            for junction_info in junctions_dict.values():
                junction_pipe_gids = junction_info['pipe_gids']
                junction_node_id = junction_info['node_id']

                matching_pipe_gids = set(asset_pipe_gids) & set(junction_pipe_gids)

                if matching_pipe_gids:
                    if asset_node_id not in self.G.nodes:
                        self.G.add_node(asset_node_id)

                    for neighbor_pipe_gid in matching_pipe_gids:
                        if neighbor_pipe_gid in self.G:
                            neighbor_node_id = self.G.nodes[neighbor_pipe_gid]['node_id']
                            self.G.add_edge(asset_node_id, neighbor_node_id, pipe_gid=neighbor_pipe_gid)

        # Remove duplicate edges to ensure the graph is consistent
        self.G = nx.Graph(self.G)

    def create_nx_graph(self):
        """Create the NetworkX graph from the geospatial network"""
        asset_dict, junctions_dict = self.extract_assets_and_junctions()
        adjacency_dict = self.build_adjacency_dict(junctions_dict)

        self.build_graph_from_adjacency(adjacency_dict)
        self.integrate_coincident_nodes(asset_dict, junctions_dict)

