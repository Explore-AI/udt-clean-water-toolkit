import networkx as nx
from networkx import Graph
from cleanwater.calculators import GisToGraphCalculator
import matplotlib.pyplot as plt
import pdb


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
        nodes_with_pipes = []
        for sublist in self.all_nodes_ordered:
            for subdict in sublist:
                nodes_with_pipes.append(subdict)

        junctions_dict = {}

        for idx, src_dict in enumerate(nodes_with_pipes, start=1):
            node_id = src_dict.get('node_id')
            pipe_gids = src_dict.get('pipe_gids', [])

            junctions_dict[node_id] = pipe_gids

        return junctions_dict

    def create_adjacency_dict(self, junctions_dict):
        # Initialize an empty adjacency list dictionary
        adjacency_list = {}

        # Iterate through each junction in the dictionary
        for node, pipes in junctions_dict.items():
            # Initialize the list for the current node
            adjacency_list[node] = []

            # Iterate through each pipe that meets at the junction
            for pipe in pipes:
                # Extract the other end of the pipe
                other_node = [key for key, value in junctions_dict.items() if pipe in value and key != node]

                # Add the other end to the adjacency list
                if other_node:
                    adjacency_list[node].append(other_node[0])

        # Create a graph from the adjacency list
        print(adjacency_list)
        self.G = nx.Graph(adjacency_list)

        # Plot and save the graph
        filename = 'Graph.png'
        nx.draw(self.G, with_labels=False, node_color='black', node_size=2, edge_color='red', linewidths=1,
                font_size=15)
        plt.savefig(filename)
        plt.close()

    def create_nx_graph(self):
        """Create the NetworkX graph from the geospatial network"""
        junctions_dict = self.extract_assets_and_junctions()
        self.create_adjacency_dict(junctions_dict)

        connected = len(list(nx.connected_components(self.G)))

        # Print nodes and edges to verify
        print("Nodes:", len(self.G.nodes()))
        print("Edges:", len(self.G.edges(data=True)))
        print("Components:", connected)
