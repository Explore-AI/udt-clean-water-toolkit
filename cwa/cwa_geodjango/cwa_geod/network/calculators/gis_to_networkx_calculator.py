from networkx import Graph
from . import GisToGraphCalculator


class GisToNxCalculator(GisToGraphCalculator):
    """Create a NetworkX graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        self.G: Graph = Graph()
        self.all_base_pipes = []
        self.all_nodes_ordered = []
        super().__init__(self.config)

    def create_nx_graph(self) -> None:
        """Iterate over pipes and connect related pipe interactions
        and point assets. Uses a map method to operate on the pipe
        and asset data.

        Params:
              None
        Returns:
              None
        """

        print("start here to create a networkx graph")

        # these two variables should have everything you need to create a graph
        # ony printing out the first element as it will be too much otherwise.
        print(self.all_base_pipes[0])
        print(self.all_nodes_ordered[0])
