from networkx import Graph
from cleanwater.calculators import GisToGraphCalculator


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

        print("start here to create a networkx graph")

        # these two vaiables should have everything you need to create a graph
        # ony printing out the first element as it will be too much otherwise.
        print(self.all_nodes_by_pipe)
        print(self.all_edges_by_pipe)
        import pdb

        pdb.set_trace()
