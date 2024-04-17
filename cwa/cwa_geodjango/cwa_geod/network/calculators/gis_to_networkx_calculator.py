import networkx as nx
from networkx import Graph
from cleanwater.calculators import GisToGraphCalculator
import matplotlib.pyplot as plt
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
        edges_dict = {}

        for feature, info in junctions_dict.items():
            node_id = info['node_id']
            pipe_gids = info['pipe_gids']

            if pipe_gids:
                for pipe_gid in pipe_gids:
                    if pipe_gid not in edges_dict:
                        edges_dict[pipe_gid] = []

                    if node_id not in edges_dict[pipe_gid]:
                        edges_dict[pipe_gid].append(node_id)
            else:
                # print(f"No pipe_gids found for node_id: {node_id}. Skipping...")
                continue

        # transform edge dictionary into useful format
        adjacency_dict = {}
        skip_count = 0

        for edge, vertices in edges_dict.items():

            if len(vertices) != 2:
                skip_count += 1
                continue

            src, dst = vertices

            # Check if either src or dst is missing and add a placeholder
            if src is None:
                src = 'None'
            if dst is None:
                dst = 'None'

            adjacency_dict[edge] = {'src': src, 'dst': dst}
        print("skipped ", skip_count, " edges")
        return adjacency_dict

    def build_graph_from_adjacency(self, adjacency_dict):
        """Build a NetworkX graph from the adjacency dictionary"""
        # Iterate through the edge dictionary and add nodes and edges to the graph
        for edge_id, edge_info in adjacency_dict.items():
            src = edge_info['src']
            dst = edge_info['dst']

            # Add nodes and edges to the graph
            self.G.add_edge(src, dst, edge_id=edge_id)



    def integrate_coincident_nodes(self, asset_dict, junctions_dict):
        """Integrate coincident nodes from asset_dict into the graph"""
        int_count = 0
        non_count = 0
        for feature, asset_info in asset_dict.items():
            asset_pipe_gids = asset_info['pipe_gids']
            asset_node_id = asset_info['node_id']

            for junction_info in junctions_dict.values():
                junction_pipe_gids = junction_info['pipe_gids']
                # junction_node_id = junction_info['node_id']

                if asset_pipe_gids is not None and junction_pipe_gids is not None:
                    matching_pipe_gids = set(asset_pipe_gids) & set(junction_pipe_gids)
                    int_count += 1
                else:
                    non_count += 1
                    continue

                if matching_pipe_gids:
                    if asset_node_id not in self.G.nodes:
                        self.G.add_node(asset_node_id)

                    for neighbour_pipe_gid in matching_pipe_gids:
                        if neighbour_pipe_gid in self.G:
                            neighbor_node_id = self.G.nodes[neighbour_pipe_gid]['node_id']
                            self.G.add_edge(asset_node_id, neighbor_node_id, pipe_gid=neighbour_pipe_gid)
        print("nodes merged: ", int_count)
        print("nodes skipped: ", non_count)
        # Remove duplicate edges to ensure the graph is consistent
        self.G = nx.Graph(self.G)

    def remove_isolated_nodes_and_plot(self):
        filename = 'Graph.png'
        components = list(nx.connected_components(self.G))
        isolated_nodes = [node for component in components for node in component if len(component) == 1]

        self.G.remove_nodes_from(isolated_nodes)

        # Plot and save the graph
        nx.draw(self.G, with_labels=False, node_color='black', node_size=20, edge_color='red', linewidths=1,
                font_size=15)
        plt.savefig(filename)
        plt.close()

        print(f"Graph saved as {filename} in the current directory.")

    def create_nx_graph(self):
        """Create the NetworkX graph from the geospatial network"""
        asset_dict, junctions_dict = self.extract_assets_and_junctions()
        adjacency_dict = self.build_adjacency_dict(junctions_dict)

        self.build_graph_from_adjacency(adjacency_dict)
        self.integrate_coincident_nodes(asset_dict, junctions_dict)
        self.remove_isolated_nodes_and_plot()

        # Print nodes and edges to verify
        print("Nodes:", len(self.G.nodes()))
        print("Edges:", len(self.G.edges(data=True)))