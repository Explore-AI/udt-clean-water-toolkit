from networkx import Graph
import networkx as nx
from cleanwater.calculators import GisToGraphCalculator
from cwageodjango.config.settings import sqids
import matplotlib.pyplot as plt


class GisToNxCalculator(GisToGraphCalculator):
    """Create a NetworkX graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        self.G: Graph = Graph()

        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []

        super().__init__(
            self.config.srid,
            sqids,
            processor_count=config.processor_count,
            chunk_size=config.chunk_size,
            neoj4_point=self.config.neoj4_point,
        )

    def create_nx_graph(self) -> None:
        """Iterate over pipes and connect related pipe interactions
        and point assets. Uses a map method to operate on the pipe
        and asset data.

        Params:
              None
        Returns:
              None
        """
        edges = self._gather_edges()
        nodes = self._gather_nodes()
        self.G = nx.Graph()
        self._add_nodes_to_graph(nodes)
        self._add_edges_to_graph(edges)
        self._remove_unconnected_nodes()
        self._connected_components()
        self._plot_graph()

    def _gather_edges(self):
        edges = []
        for sublist in self.all_edges_by_pipe:
            for edge in sublist:
                edges.append(edge)

        return edges

    def _gather_nodes(self):
        nodes = []
        for sublist in self.all_nodes_by_pipe:
            for node in sublist:
                nodes.append(node)

        return nodes

    def _add_nodes_to_graph(self, nodes):
        unique_nodes = []
        unique_node_keys = []
        for node in nodes:
            if node["node_key"] not in unique_node_keys:
                unique_nodes.append(node)
                unique_node_keys.append(node["node_key"])

        for node in unique_nodes:
            node_id = node["node_key"]
            attributes = {
                key: value for key, value in node.items() if key != "node_key"
            }
            self.G.add_node(node_id, **attributes)

    def _add_edges_to_graph(self, edges):
        # Add edges to the graph with attributes
        for edge in edges:
            from_node = edge["from_node_key"]
            to_node = edge["to_node_key"]
            attributes = {
                key: value
                for key, value in edge.items()
                if key not in ["from_node_key", "to_node_key"]
            }
            self.G.add_edge(from_node, to_node, **attributes)

    def _remove_unconnected_nodes(self):
        # Get a list of isolated nodes
        isolated_nodes = list(nx.isolates(self.G))

        # Remove isolated nodes from the graph
        self.G.remove_nodes_from(isolated_nodes)
        num_isolated_nodes = len(isolated_nodes)
        print("Number of isolated nodes removed:", num_isolated_nodes)

    def _connected_components(self):
        connected = len(list(nx.connected_components(self.G)))
        print('Connected components:', connected)

    def _plot_graph(self):
        # Output name
        filename = "Graph.svg"

        # Define edge positions
        pos = nx.spring_layout(self.G, scale=10)

        # Extracting node and edge labels from the graph
        node_labels = nx.get_node_attributes(self.G, "node_labels").values()
        edge_labels = nx.get_edge_attributes(self.G, "asset_name").values()

        # Define colour map based on node and edge labels
        nodes_colour_map = ['blue' if 'Hydrant' in labels
                            else 'yellow' if 'NetworkOptValve' in labels
                            else 'red' for labels in node_labels]

        edges_colour_map = ['black' if 'TrunkMain' in labels
                            else 'orange' for labels in edge_labels]

        # Draw the graph nodes and edges
        plt.figure(figsize=(30, 30))
        nx.draw(
            self.G, pos, with_labels=False, node_color=nodes_colour_map, node_size=15, font_size=2
        )
        nx.draw_networkx_edges(self.G, pos, edge_color=edges_colour_map, width=1)

        # Draw edge labels using the gid attribute
        edge_labels = nx.get_edge_attributes(self.G, "gid")
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.savefig(filename, format="svg")
        plt.close()
        print("file 'Graph.svg' successfully saved")
